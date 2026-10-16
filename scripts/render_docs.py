"""Generate human-readable references from the same JSON used by the future viewer."""
import argparse
import json
from pathlib import Path
from validate_model import validate
ROOT=Path(__file__).resolve().parents[1]

def outputs(m):
    files={}
    lines=['# Entity catalogue','','Generated from `model/banking.model.json`. Edit the model and regenerate.','']
    for d in m['domains']:
        lines += ['## '+d['label'],'',d['description'],'','| Entity | Meaning | Grain |','|---|---|---|']
        for e in m['entities']:
            if e['domain']==d['id']:lines.append(f'| `{e["id"]}` | {e["description"]} | {e["grain"]} |')
        lines+=['']
    files['ENTITY_CATALOGUE.md']='\n'.join(lines)+'\n'
    lines=['# Data dictionary','','Logical types are intentionally engine-neutral. Dates are calendar dates; timestamps are UTC instants.','']
    for e in m['entities']:
        lines+=['## '+e['id'],'',e['description'],'','**Grain:** '+e['grain'],'','**Primary key:** '+', '.join(e['primary_key']),'','| Column | Type | Nullable | Classification | Definition |','|---|---|---|---|---|']
        for c in e['columns']:
            desc=c['description']+(' Allowed: '+', '.join(c['allowed_values'])+'.' if 'allowed_values' in c else '')
            lines.append(f'| `{c["id"]}` | `{c["type"]}` | {str(c["nullable"]).lower()} | {c["classification"]} | {desc} |')
        lines+=['','**Unique keys:** '+('; '.join(', '.join(k) for k in e['unique_keys']) or 'Primary key only.'),'','**Notes:** '+' '.join(e['notes']),'','**Rules:** '+', '.join(e['rule_ids']),'']
    files['DATA_DICTIONARY.md']='\n'.join(lines)+'\n'
    lines=['# Relationships','','Read each row from the referencing table to the referenced table. Reverse cardinality describes the maximum number of children; conditional minimums live in business rules.','','| Relationship | From | To | Referenced rows per source | Source rows per target | Meaning |','|---|---|---|---|---|---|']
    for r in m['relationships']:lines.append(f'| `{r["id"]}` | `{r["source_entity"]}.{r["source_column"]}` | `{r["target_entity"]}.{r["target_column"]}` | {r["source_to_target"]} | {r["target_to_source"]} | {r["description"]} |')
    files['RELATIONSHIPS.md']='\n'.join(lines)+'\n'
    lines=['# Business rules','','These are specifications, not implemented data-quality checks. The metadata validator verifies their references only.','']
    for r in m['rules']:lines += ['## '+r['id']+' — '+r['category'],'',r['statement'],'','Applies to: '+', '.join('`'+e+'`' for e in r['entities'])+'.','']
    files['BUSINESS_RULES.md']='\n'.join(lines)+'\n'
    lines=['# Business journeys','','These presets are metadata for the future explorer; this checkpoint does not include an interactive UI.','']
    for j in m['journeys']:
        lines+=['## '+j['title'],'',j['question'],'']
        lines += [f'{i}. **{s["entity"]}** — {s["text"]}' for i,s in enumerate(j['steps'],1)]
        lines+=['',j['caveat'],'','Highlighted relationships: '+', '.join('`'+r+'`' for r in j['relationship_ids'])+'.','']
    files['JOURNEYS.md']='\n'.join(lines)+'\n'
    return files

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    m=json.loads((ROOT/'model/banking.model.json').read_text()); errors=validate(m)
    if errors:raise SystemExit('\n'.join(errors))
    stale=[]
    for name,content in outputs(m).items():
        path=ROOT/'docs'/name
        if args.check:
            if not path.exists() or path.read_text()!=content:stale.append(name)
        else:path.write_text(content)
    if stale:raise SystemExit('Generated docs are stale: '+', '.join(stale))
    print('Generated documentation is current.' if args.check else 'Generated five model reference documents.')
if __name__=='__main__':main()
