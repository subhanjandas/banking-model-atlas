"""Generate deterministic evidence by actually processing two batches and a rejection."""
import argparse
import json
import tempfile
from .pipeline import ROOT, connect, initialize, apply_batch, snapshot, backfill
from scripts.ingest_returns import BatchRejected

def batch(name):
    directory = ROOT/'fixtures/ingestion'
    return (json.loads((directory/f'{name}.json').read_text()), json.loads((directory/f'{name}-manifest.json').read_text()))

def generate():
    with tempfile.TemporaryDirectory() as directory:
        db = connect(directory+'/lab.sqlite')
        initialize(db, json.loads((ROOT/'fixtures/banking_scenarios.json').read_text())['tables']['payment_order'])
        initial = apply_batch(db, *batch('initial'))
        before = snapshot(db, '2026-09-29T23:59:59Z')
        correction = apply_batch(db, *batch('correction'))
        replay = apply_batch(db, *batch('correction'))
        rows, manifest = batch('correction')
        manifest = {**manifest, 'batch_id': 'INCOMPLETE_DEMONSTRATION'}
        try:
            apply_batch(db, [], manifest)
        except BatchRejected:
            pass
        after_rejection = snapshot(db, '2026-09-30T23:59:59Z')
        backfill(db, '2026-09-01', '2026-09-30')
        after = snapshot(db, '2026-09-30T23:59:59Z')
        assert after['daily_sha256'] == after_rejection['daily_sha256']
        result = {'scope': 'Synthetic local SQLite pipeline; static build-time evidence',
                  'schema_version': 2, 'currency': 'CAD', 'unit': 'minor units (cents)',
                  'initial_batch': initial, 'before_correction': before,
                  'correction_batch': correction, 'replay': replay,
                  'after_rejection': after_rejection, 'final': after,
                  'quarantine_codes': [r[0] for r in db.execute('SELECT code FROM quarantine ORDER BY code')],
                  'bounded_backfill_preserved_checksum': True}
        db.close()
        return result

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    path = ROOT/'generated/engineering-report.json'
    body = json.dumps(generate(), indent=2)+'\n'
    if args.check:
        if path.read_text() != body:
            raise SystemExit('Engineering evidence is stale')
    else:
        path.write_text(body)
    print('Engineering evidence verified' if args.check else 'Engineering evidence generated')

if __name__ == '__main__':
    main()
