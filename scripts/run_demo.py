"""Execute the reference schema and independently specified synthetic scenarios."""
import argparse
import json
from pathlib import Path
from decimal import Decimal
import duckdb
from reconcile_ledger import reconcile
from export_sql import render, order_entities, ident
ROOT=Path(__file__).resolve().parents[1]
MODEL=json.loads((ROOT/'model/banking.model.json').read_text())
FIXTURE=json.loads((ROOT/'fixtures/banking_scenarios.json').read_text())
CHECKS=json.loads((ROOT/'model/validation_checks.json').read_text())['checks']

def database():
    db=duckdb.connect(':memory:');db.execute(render(MODEL))
    for e in order_entities(MODEL):
        columns=[c['id'] for c in e['columns']]
        for row in FIXTURE['tables'].get(e['id'],[]):
            unknown=set(row)-set(columns)
            if unknown:raise ValueError(f'Unknown fixture columns: {unknown}')
            db.execute('INSERT INTO '+ident(e['id'])+' ('+','.join(map(ident,columns))+') VALUES ('+','.join('?' for _ in columns)+')',[row.get(k) for k in columns])
    return db

def violations(db):
    results={c['id']:db.execute(c['sql']).fetchall() for c in CHECKS}
    for r in MODEL['relationships']:
        # Also covers self references deliberately omitted from the physical DDL.
        rows=db.execute(f'SELECT s.{ident(r["source_column"])} FROM {ident(r["source_entity"])} s LEFT JOIN {ident(r["target_entity"])} t ON s.{ident(r["source_column"])}=t.{ident(r["target_column"])} WHERE s.{ident(r["source_column"])} IS NOT NULL AND t.{ident(r["target_column"])} IS NULL').fetchall()
        if rows:results['FK:'+r['id']]=rows
    return results

def report(db):
    issues=violations(db)
    if any(issues.values()):raise AssertionError({k:v for k,v in issues.items() if v})
    balances={}
    for aid,opening in FIXTURE['opening_balances'].items():
        kind=db.execute('SELECT p.kind FROM account a JOIN product_version v USING(product_version_id) JOIN product p USING(product_id) WHERE a.account_id=?',[aid]).fetchone()[0]
        delta=db.execute("SELECT coalesce(sum(CASE WHEN direction='DEBIT' THEN amount ELSE -amount END),0) FROM account_entry WHERE account_id=? AND posted_on>? AND posted_on<=?",[aid,FIXTURE['period']['opening'],FIXTURE['period']['closing']]).fetchone()[0]
        value=Decimal(opening)+(-delta if kind=='DEPOSIT' else delta)
        assert value==Decimal(FIXTURE['expected_closing_balances'][aid]),(aid,value)
        snapshot=db.execute('SELECT balance_amount FROM account_balance_snapshot WHERE account_id=? AND as_of_date=?',[aid,FIXTURE['period']['closing']]).fetchone()[0]
        assert snapshot==value,(aid,'snapshot',snapshot,value)
        balances[aid]=str(value.quantize(Decimal('0.01')))
    reconciliation=reconcile(db,FIXTURE['period'])
    return dict(ledger_reconciliation=reconciliation,model_version=MODEL['model_version'],duckdb_version=duckdb.__version__,schema_tables=len(MODEL['entities']),populated_tables=len(FIXTURE['tables']),synthetic_records=sum(map(len,FIXTURE['tables'].values())),relationship_integrity_checks=len(MODEL['relationships']),business_checks=len(CHECKS),business_check_failures=0,posted_journals=db.execute("SELECT count(*) FROM journal WHERE status='POSTED'").fetchone()[0],closing_balances=balances,limitations='Only these fixtures and explicit checks were executed. Not all business rules or banking processes are implemented.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-report',action='store_true');ap.add_argument('--check-report',action='store_true');a=ap.parse_args()
    with database() as db:r=report(db)
    text=json.dumps(r,indent=2)+'\n';path=ROOT/'generated/demo-report.json'
    if a.write_report:path.write_text(text)
    if a.check_report and (not path.exists() or path.read_text()!=text):raise SystemExit('Demo report is stale.')
    print(text)
if __name__=='__main__':main()
