"""Deterministic batch ingestion with independent producer controls and atomic publication.

This is a local reference pipeline, not a distributed exactly-once service.
"""
import argparse
from datetime import datetime
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

ROOT=Path(__file__).resolve().parents[1]
CONTRACT='payment-return-v1'
ENVELOPE={'delivery_id','source','contract','key','version','event_at','received_at','payload'}
PAYLOAD={'payment_return_id','payment_order_id','amount','returned_on','external_reference'}
class BatchRejected(ValueError):
    def __init__(self,issues):
        self.issues=issues
        super().__init__('Batch rejected: '+', '.join(i['code'] for i in issues))
def timestamp(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',value):raise ValueError('UTC Z timestamp required')
    return datetime.fromisoformat(value.replace('Z','+00:00'))
def fingerprint(row):
    value={k:row[k] for k in ['source','contract','key','version','event_at','payload']}
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate(row):
    if set(row)!=ENVELOPE:raise ValueError('ENVELOPE_SCHEMA')
    if row['contract']!=CONTRACT or row['source']!='synthetic-payments':raise ValueError('CONTRACT_VERSION')
    if type(row['version']) is not int or row['version']<1:raise ValueError('REVISION')
    if not all(isinstance(row[k],str) and row[k] for k in ['delivery_id','key']):raise ValueError('IDENTIFIER')
    if timestamp(row['received_at'])<timestamp(row['event_at']):raise ValueError('TIMESTAMP_ORDER')
    p=row['payload']
    if not isinstance(p,dict) or set(p)!=PAYLOAD:raise ValueError('PAYLOAD_SCHEMA')
    if not all(isinstance(v,str) and v for v in p.values()):raise ValueError('PAYLOAD_TYPE')
    if p['payment_return_id']!=row['key']:raise ValueError('KEY_MISMATCH')
    if not re.fullmatch(r'\d{1,16}\.\d{2}',p['amount']) or Decimal(p['amount'])<=0:raise ValueError('AMOUNT')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',p['returned_on']):raise ValueError('BUSINESS_DATE')
    datetime.strptime(p['returned_on'],'%Y-%m-%d')
    if p['returned_on']!=row['event_at'][:10]:raise ValueError('EVENT_DATE')
def process(records,manifest,as_of=None):
    """Validate the complete batch first; then derive a reproducible knowledge-time view."""
    if manifest.get('contract')!=CONTRACT:raise BatchRejected([{'code':'MANIFEST_CONTRACT'}])
    issues=[];versions={};deliveries={}
    for row in records:
        try:validate(row)
        except (ValueError,TypeError,KeyError) as exc:
            issues.append({'delivery_id':row.get('delivery_id','unknown') if isinstance(row,dict) else 'unknown','code':'INVALID_RECORD','detail':str(exc)})
            continue
        digest=fingerprint(row);key=(row['key'],row['version'])
        if row['delivery_id'] in deliveries and deliveries[row['delivery_id']]!=digest:issues.append({'code':'DELIVERY_ID_CONFLICT','delivery_id':row['delivery_id']})
        deliveries[row['delivery_id']]=digest
        prior=versions.get(key)
        if prior and fingerprint(prior)!=digest:issues.append({'code':'REVISION_CONFLICT','key':row['key'],'version':row['version']})
        elif not prior or timestamp(row['received_at'])<timestamp(prior['received_at']):versions[key]=row
    expected={(x['key'],x['version']):x['sha256'] for x in manifest['expected_versions']}
    actual={k:fingerprint(v) for k,v in versions.items()}
    if len(expected)!=len(manifest['expected_versions']) or len(expected)!=manifest['expected_distinct_versions']:issues.append({'code':'INVALID_MANIFEST'})
    if set(expected)-set(actual):issues.append({'code':'MISSING_SOURCE_RECORDS','keys':[list(x) for x in sorted(set(expected)-set(actual))]})
    if set(actual)-set(expected):issues.append({'code':'UNEXPECTED_SOURCE_RECORDS'})
    if any(actual[k]!=v for k,v in expected.items() if k in actual):issues.append({'code':'SOURCE_HASH_MISMATCH'})
    control=sum((Decimal(v['payload']['amount']) for v in versions.values()),Decimal(0))
    if control!=Decimal(manifest['expected_revision_amount_total']):issues.append({'code':'SOURCE_CONTROL_TOTAL'})
    if issues:raise BatchRejected(issues)
    cutoff=timestamp(as_of) if as_of else None
    known=[v for v in versions.values() if cutoff is None or timestamp(v['received_at'])<=cutoff]
    latest={}
    for row in known:
        if row['key'] not in latest or row['version']>latest[row['key']]['version']:latest[row['key']]=row
    selected=[latest[k] for k in sorted(latest)]
    return {'batch_id':manifest['batch_id'],'contract':CONTRACT,'as_of':as_of,'deliveries':len(records),'distinct_source_versions':len(versions),'duplicate_deliveries':len(records)-len(versions),'late_versions':sum(v['received_at'][:10]>v['event_at'][:10] for v in versions.values()),'revision_control_total':str(control.quantize(Decimal('0.01'))),'curated_total':str(sum((Decimal(v['payload']['amount']) for v in selected),Decimal(0)).quantize(Decimal('0.01'))),'selected_versions':{v['key']:v['version'] for v in selected},'curated_rows':[v['payload'] for v in selected],'lineage':[{'key':v['key'],'version':v['version'],'source_sha256':fingerprint(v),'event_at':v['event_at'],'received_at':v['received_at']} for v in selected]}
def publish(records,manifest,destination):
    # No write occurs until ALL completeness and contract gates pass.
    result=process(records,manifest);destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',dir=destination.parent,delete=False,encoding='utf-8') as out:
            temporary=out.name;out.write(json.dumps(result,indent=2)+'\n');out.flush();os.fsync(out.fileno())
        os.replace(temporary,destination)
    finally:
        if temporary and os.path.exists(temporary):os.unlink(temporary)
    return result

def inputs():
    return (json.loads((ROOT/'fixtures/ingestion/return_deliveries.json').read_text()),json.loads((ROOT/'fixtures/ingestion/producer_manifest.json').read_text()))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-report',action='store_true');ap.add_argument('--check-report',action='store_true');a=ap.parse_args()
    rows,manifest=inputs();result=process(rows,manifest)
    # Independent curated model fixture is an integration expectation, not the source of controls.
    expected=json.loads((ROOT/'fixtures/banking_scenarios.json').read_text())['tables']['payment_return']
    if result['curated_rows']!=expected:raise AssertionError('Source projection differs from banking fixture')
    path=ROOT/'generated/ingestion-report.json';body=json.dumps(result,indent=2)+'\n'
    if a.write_report:publish(rows,manifest,path)
    if a.check_report and (not path.exists() or path.read_text()!=body):raise SystemExit('Ingestion report is stale')
    print(json.dumps({k:v for k,v in result.items() if k not in ['curated_rows','lineage']},indent=2))
if __name__=='__main__':main()
