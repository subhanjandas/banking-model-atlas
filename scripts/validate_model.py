"""Check the explorer's metadata contract. Does not validate banking records."""
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'model/banking.model.json'


def validate(m):
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    def text(value): return isinstance(value, str) and bool(value.strip())
    def index(items, label):
        result = {}
        for item in items:
            key = item.get('id')
            check(isinstance(key,str) and bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',key)), f'{label}: invalid ID {key}')
            check(key not in result, f'{label}: duplicate ID {key}')
            result[key] = item
        return result
    if not isinstance(m,dict):return ['Model must be an object']
    for field in ('schema_version','model_version','id','title','status','scenario','description','business_timezone'):
        check(text(m.get(field)),f'Missing model field: {field}')
    check(m.get('schema_version')=='1.0.0','Unsupported metadata schema version')
    for field in ('domains','entities','relationships','rules','journeys'):
        if not isinstance(m.get(field),list) or not all(isinstance(v,dict) for v in m.get(field,[])):
            return errors+[f'{field} must be a list of objects']
        check(bool(m[field]),f'{field} must not be empty')
    ds=index(m['domains'],'domain'); es=index(m['entities'],'entity'); rs=index(m['relationships'],'relationship'); bs=index(m['rules'],'rule'); js=index(m['journeys'],'journey')
    for d in ds.values():
        for f in ('label','description'):check(text(d.get(f)),f'{d["id"]}: missing {f}')
        check(bool(re.fullmatch(r'#[0-9a-fA-F]{6}',d.get('color',''))),f'{d["id"]}: invalid color')
    cols={}
    for e in es.values():
        eid=e['id']; check(e.get('domain') in ds,f'{eid}: unknown domain')
        for f in ('label','description','grain'):check(text(e.get(f)),f'{eid}: missing {f}')
        if not isinstance(e.get('columns'),list) or not all(isinstance(c,dict) for c in e['columns']):
            errors.append(f'{eid}: columns must be objects');cols[eid]={};continue
        cs=index(e['columns'],eid+' column');cols[eid]=cs
        check(bool(cs),f'{eid}: no columns')
        for c in cs.values():
            check(c.get('type') in {'string','date','timestamp','integer','boolean','decimal(18,2)'},f'{eid}.{c["id"]}: unsupported type')
            check(type(c.get('nullable')) is bool,f'{eid}.{c["id"]}: nullable must be boolean')
            check(text(c.get('description')),f'{eid}.{c["id"]}: missing description')
            check(c.get('classification') in {'identifier','personal','financial','internal'},f'{eid}.{c["id"]}: invalid classification')
            if 'allowed_values' in c:
                av=c['allowed_values'];check(isinstance(av,list) and bool(av) and all(isinstance(v,str) for v in av) and len(av)==len(set(av)),f'{eid}.{c["id"]}: invalid allowed values')
        pk=e.get('primary_key',[])
        check(isinstance(pk,list) and len(pk)==1,f'{eid}: version 1 requires a single-column primary key')
        for key in pk:
            check(key in cs and cs[key].get('nullable') is False,f'{eid}: missing or nullable primary key {key}')
        for uk in e.get('unique_keys',[]):
            check(isinstance(uk,list) and bool(uk) and len(set(uk))==len(uk) and all(k in cs for k in uk),f'{eid}: invalid unique key')
        check(isinstance(e.get('notes'),list) and bool(e['notes']) and all(text(n) for n in e['notes']),f'{eid}: missing notes')
        for bid in e.get('rule_ids',[]):check(bid in bs,f'{eid}: unknown business rule {bid}')
    seen=set()
    for r in rs.values():
        rid=r['id']; src=r.get('source_entity');dst=r.get('target_entity'); sc=r.get('source_column');tc=r.get('target_column')
        check(text(r.get('description')),f'{rid}: missing relationship description')
        check(r.get('source_to_target') in {'zero_or_one','exactly_one'},f'{rid}: invalid source cardinality')
        check(r.get('target_to_source') in {'zero_or_one','zero_or_many'},f'{rid}: invalid reverse cardinality')
        check((src,sc) not in seen,f'{rid}: repeated relationship source');seen.add((src,sc))
        if src not in cols or dst not in cols or sc not in cols.get(src,{}) or tc not in cols.get(dst,{}):
            errors.append(f'{rid}: broken relationship endpoint');continue
        a,b=cols[src][sc],cols[dst][tc]
        check(a['type']==b['type'],f'{rid}: mismatched key types')
        check(es[dst]['primary_key']==[tc] or [tc] in es[dst].get('unique_keys',[]),f'{rid}: target is not unique')
        check(r['source_to_target']==('zero_or_one' if a['nullable'] else 'exactly_one'),f'{rid}: nullability/cardinality mismatch')
        unique=[sc] in es[src].get('unique_keys',[]) or es[src]['primary_key']==[sc]
        check(r['target_to_source']==('zero_or_one' if unique else 'zero_or_many'),f'{rid}: reverse cardinality/uniqueness mismatch')
    for eid,cs in cols.items():
        for cid in cs:
            if cid.endswith('_id') and cid not in es[eid]['primary_key']:
                check((eid,cid) in seen,f'{eid}.{cid}: identifier has no relationship')
    for b in bs.values():
        check(text(b.get('statement')),f'{b["id"]}: missing statement')
        check(b.get('implementation_status')=='specified_not_implemented',f'{b["id"]}: Hour 1 must not claim data-rule enforcement')
        check(bool(b.get('entities')),f'{b["id"]}: missing entities')
        for eid in b.get('entities',[]):check(eid in es and b['id'] in es[eid].get('rule_ids',[]),f'{b["id"]}: invalid entity/rule backlink')
    for e in es.values():
        for bid in e.get('rule_ids',[]):
            if bid in bs:check(e['id'] in bs[bid]['entities'],f'{e["id"]}: inconsistent rule backlink')
    for j in js.values():
        for f in ('title','question','caveat'):check(text(j.get(f)),f'{j["id"]}: missing {f}')
        steps=j.get('steps',[]); check(bool(steps),f'{j["id"]}: no journey steps')
        nodes={s.get('entity') for s in steps}; check(len(nodes)==len(steps),f'{j["id"]}: repeated journey entity')
        for s in steps:check(s.get('entity') in es and text(s.get('text')),f'{j["id"]}: invalid journey step')
        adj={n:set() for n in nodes}
        for rid in j.get('relationship_ids',[]):
            if rid not in rs:errors.append(f'{j["id"]}: unknown journey relationship');continue
            a=rs[rid]['source_entity'];b=rs[rid]['target_entity']
            check(a in nodes and b in nodes,f'{j["id"]}: journey edge leaves selected entities')
            if a in adj and b in adj:adj[a].add(b);adj[b].add(a)
        if nodes:
            reached=set(); pending=[next(iter(nodes))]
            while pending:
                n=pending.pop()
                if n not in reached:reached.add(n);pending.extend(adj[n]-reached)
            check(reached==nodes,f'{j["id"]}: disconnected journey')
    return errors


def main():
    try:
        m=json.loads(MODEL.read_text());errors=validate(m)
    except (ValueError,TypeError,KeyError) as exc:
        print(f'Invalid model structure: {exc}',file=sys.stderr);return 1
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 1
    print(f'Metadata valid: {len(m["domains"])} domains, {len(m["entities"])} entities, {len(m["relationships"])} relationships, {sum(len(e["columns"]) for e in m["entities"])} columns, {len(m["rules"])} specified rules, {len(m["journeys"])} connected journeys.')
    print('This checks metadata integrity, not banking records or regulatory compliance.')
    return 0

if __name__=='__main__':sys.exit(main())
