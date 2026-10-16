"""Generate a tested DuckDB reference schema from the logical model."""
import argparse
import json
from pathlib import Path
from validate_model import validate
ROOT=Path(__file__).resolve().parents[1]
TYPES={'string':'VARCHAR','integer':'INTEGER','boolean':'BOOLEAN','date':'DATE','timestamp':'TIMESTAMP','decimal(18,2)':'DECIMAL(18,2)'}
def ident(s):return '"'+s.replace('"','""')+'"'
def literal(s):return "'"+s.replace("'","''")+"'"
def order_entities(m):
    entities={e['id']:e for e in m['entities']};deps={e:set() for e in entities}
    for r in m['relationships']:
        if r['source_entity']!=r['target_entity']:deps[r['source_entity']].add(r['target_entity'])
    ordered=[]
    while deps:
        ready=sorted(e for e,d in deps.items() if not d)
        if not ready:raise ValueError('Cross-table dependency cycle; cannot create foreign keys in this exporter')
        for e in ready:ordered.append(entities[e]);del deps[e]
        for d in deps.values():d.difference_update(ready)
    return ordered

def render(m):
    errors=validate(m)
    if errors:raise ValueError('\n'.join(errors))
    out=['-- Banking Model Atlas | model '+m['model_version'],'-- Dialect: DuckDB. Run in a fresh database. No DROP or destructive reset.','-- PK, non-self FK, UNIQUE, NOT NULL and enumerations are enforced.','-- Self-reference integrity and selected business rules are checked by scripts/run_demo.py.','-- TIMESTAMP values represent UTC by convention; no automatic time-zone conversion.','-- This reference DDL is not a production bank deployment.','']
    for e in order_entities(m):
        definitions=[]
        for c in e['columns']:
            definition=ident(c['id'])+' '+TYPES[c['type']]+(' NOT NULL' if not c['nullable'] else '')
            if c.get('allowed_values'):definition+=' CHECK ('+ident(c['id'])+' IN ('+', '.join(literal(v) for v in c['allowed_values'])+'))'
            definitions.append(definition)
        definitions.append('PRIMARY KEY ('+', '.join(map(ident,e['primary_key']))+')')
        for k in e['unique_keys']:definitions.append('UNIQUE ('+', '.join(map(ident,k))+')')
        for r in m['relationships']:
            if r['source_entity']==e['id'] and r['target_entity']!=e['id']:
                definitions.append('FOREIGN KEY ('+ident(r['source_column'])+') REFERENCES '+ident(r['target_entity'])+' ('+ident(r['target_column'])+')')
        out+=['-- '+e['grain'],'CREATE TABLE '+ident(e['id'])+' (\n  '+',\n  '.join(definitions)+'\n);']
        out.append('COMMENT ON TABLE '+ident(e['id'])+' IS '+literal(e['description']+' Grain: '+e['grain'])+';')
        for c in e['columns']:out.append('COMMENT ON COLUMN '+ident(e['id'])+'.'+ident(c['id'])+' IS '+literal(c['description'])+';')
        out+=['']
    return '\n'.join(out)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    m=json.loads((ROOT/'model/banking.model.json').read_text());sql=render(m);path=ROOT/'generated/banking.duckdb.sql'
    if a.check:
        if not path.exists() or path.read_text()!=sql:raise SystemExit('DuckDB export is stale; run scripts/export_sql.py')
    else:path.parent.mkdir(exist_ok=True);path.write_text(sql)
    print(f'DuckDB schema {"checked" if a.check else "generated"}: {len(m["entities"])} tables.')
if __name__=='__main__':main()
