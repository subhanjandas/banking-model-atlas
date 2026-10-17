"""Transactional local return processing. Money is stored as integer minor units."""
import argparse
from datetime import date, timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sqlite3
from scripts.ingest_returns import process, fingerprint, BatchRejected, timestamp

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 2

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def minor(value):
    return int(Decimal(value) * 100)

def connect(path):
    db = sqlite3.connect(path, timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('PRAGMA synchronous=FULL')
    migrate(db)
    return db

def migrate(db):
    """Versioned migrations are atomic; unknown future schemas fail closed."""
    db.execute('BEGIN IMMEDIATE')
    try:
        version = db.execute('PRAGMA user_version').fetchone()[0]
        if version > SCHEMA_VERSION:
            raise ValueError('Database schema is newer than this reader')
        if version == 0:
            statements = [
                'CREATE TABLE payments (id TEXT PRIMARY KEY, day TEXT NOT NULL, channel TEXT NOT NULL, currency TEXT NOT NULL, amount INTEGER NOT NULL CHECK(amount>0))',
                'CREATE TABLE versions (key TEXT, version INTEGER, hash TEXT NOT NULL, payload TEXT NOT NULL, received_at TEXT NOT NULL, PRIMARY KEY(key,version))',
                'CREATE TABLE deliveries (id TEXT PRIMARY KEY, hash TEXT NOT NULL)',
                'CREATE TABLE current_returns (key TEXT PRIMARY KEY, version INTEGER NOT NULL, payment_id TEXT NOT NULL REFERENCES payments(id), day TEXT NOT NULL, amount INTEGER NOT NULL CHECK(amount>0))',
                'CREATE TABLE batches (id TEXT PRIMARY KEY, hash TEXT NOT NULL, checkpoint INTEGER UNIQUE NOT NULL)',
                'CREATE TABLE daily (day TEXT, channel TEXT, currency TEXT, payment_count INTEGER NOT NULL, payment_amount INTEGER NOT NULL, return_count INTEGER NOT NULL, return_amount INTEGER NOT NULL, PRIMARY KEY(day,channel,currency))',
                'CREATE TABLE runs (id INTEGER PRIMARY KEY, batch_id TEXT NOT NULL, status TEXT NOT NULL, metrics TEXT NOT NULL)',
                'CREATE TABLE quarantine (run_id INTEGER NOT NULL REFERENCES runs(id), code TEXT NOT NULL)',
                'CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)',
            ]
            for sql in statements:
                db.execute(sql)
        if version < 2:
            db.execute('ALTER TABLE runs ADD COLUMN operator_note TEXT')
            db.execute('CREATE INDEX current_return_day ON current_returns(day)')
            db.execute('PRAGMA user_version=2')
        db.commit()
    except BaseException:
        db.rollback()
        raise

def refresh(db, days):
    """Aggregate each source separately, then union, avoiding payment/return fan-out."""
    for day in sorted(days):
        db.execute('DELETE FROM daily WHERE day=?', (day,))
        db.execute('''INSERT INTO daily
          SELECT day,channel,currency,SUM(pc),SUM(pa),SUM(rc),SUM(ra) FROM (
            SELECT day,channel,currency,1 pc,amount pa,0 rc,0 ra FROM payments WHERE day=?
            UNION ALL
            SELECT r.day,p.channel,p.currency,0,0,1,r.amount
            FROM current_returns r JOIN payments p ON p.id=r.payment_id WHERE r.day=?
          ) GROUP BY day,channel,currency''', (day, day))

def initialize(db, payments):
    """Payments are a frozen source snapshot in this lab, never silently overwritten."""
    rows = sorted([{'id': p['payment_order_id'], 'day': p['requested_execution_on'],
                    'channel': p['channel_id'], 'currency': p['currency_id'], 'amount': minor(p['amount'])}
                   for p in payments if p['kind'] == 'OUTBOUND'], key=lambda p: p['id'])
    db.execute('BEGIN IMMEDIATE')
    try:
        prior = db.execute("SELECT value FROM settings WHERE key='payment_snapshot'").fetchone()
        if prior and prior[0] != digest(rows):
            raise ValueError('Payment snapshot changed; explicit rebuild required')
        if not prior:
            db.executemany('INSERT INTO payments VALUES (:id,:day,:channel,:currency,:amount)', rows)
            db.execute('INSERT INTO settings VALUES (?,?)', ('payment_snapshot', digest(rows)))
            refresh(db, {p['day'] for p in rows})
        db.commit()
    except BaseException:
        db.rollback()
        raise

def reject(code):
    raise BatchRejected([{'code': code}])

def apply_batch(db, records, manifest, failpoint=None):
    """Single writer transaction: versions, projection, mart and checkpoint commit together.

    The producer's control manifest is independent input, not derived from this batch.
    Failed attempts store only error codes; a killed process leaves no partial publication.
    """
    batch_id = manifest.get('batch_id', 'unknown')
    batch_hash = digest({'records': sorted(records, key=lambda x: json.dumps(x, sort_keys=True)), 'manifest': manifest})
    db.execute('BEGIN IMMEDIATE')
    try:
        result = process(records, manifest)
        prior = db.execute('SELECT hash FROM batches WHERE id=?', (batch_id,)).fetchone()
        if prior:
            if prior[0] != batch_hash:
                reject('BATCH_ID_CONFLICT')
            db.rollback()
            return {'status': 'replayed', 'affected_days': [], 'new_versions': 0}
        if not db.execute("SELECT 1 FROM settings WHERE key='payment_snapshot'").fetchone():
            reject('PAYMENTS_NOT_INITIALIZED')
        days, new = set(), 0
        for row in sorted(records, key=lambda r: (r['key'], r['version'], r['received_at'])):
            h = fingerprint(row)
            delivery = db.execute('SELECT hash FROM deliveries WHERE id=?', (row['delivery_id'],)).fetchone()
            if delivery and delivery[0] != h:
                reject('DELIVERY_ID_CONFLICT')
            db.execute('INSERT OR IGNORE INTO deliveries VALUES (?,?)', (row['delivery_id'], h))
            old = db.execute('SELECT hash FROM versions WHERE key=? AND version=?', (row['key'], row['version'])).fetchone()
            if old:
                if old[0] != h:
                    reject('REVISION_CONFLICT')
                continue
            p = row['payload']
            if not db.execute('SELECT 1 FROM payments WHERE id=?', (p['payment_order_id'],)).fetchone():
                reject('UNKNOWN_OUTBOUND_PAYMENT')
            db.execute('INSERT INTO versions VALUES (?,?,?,?,?)', (row['key'], row['version'], h, json.dumps(p, sort_keys=True), row['received_at']))
            new += 1
            current = db.execute('SELECT * FROM current_returns WHERE key=?', (row['key'],)).fetchone()
            if current and current['payment_id'] != p['payment_order_id']:
                reject('IMMUTABLE_PAYMENT_PARENT')
            if not current or row['version'] > current['version']:
                if current:
                    days.add(current['day'])
                days.add(p['returned_on'])
                db.execute('INSERT OR REPLACE INTO current_returns VALUES (?,?,?,?,?)',
                           (row['key'], row['version'], p['payment_order_id'], p['returned_on'], minor(p['amount'])))
        if db.execute('''SELECT p.id FROM payments p JOIN current_returns r ON p.id=r.payment_id
                         GROUP BY p.id,p.amount HAVING SUM(r.amount)>p.amount''').fetchone():
            reject('OVER_RETURN')
        if failpoint:
            failpoint()  # Test-only injection; includes abrupt process exit in crash test.
        refresh(db, days)
        checkpoint = db.execute('SELECT COALESCE(MAX(checkpoint),0)+1 FROM batches').fetchone()[0]
        db.execute('INSERT INTO batches VALUES (?,?,?)', (batch_id, batch_hash, checkpoint))
        metrics = {'status': 'committed', 'checkpoint': checkpoint, 'new_versions': new,
                   'affected_days': sorted(days), 'deliveries': result['deliveries'],
                   'late_versions': result['late_versions'], 'completeness': 'passed'}
        db.execute('INSERT INTO runs(batch_id,status,metrics) VALUES (?,?,?)', (batch_id, 'committed', json.dumps(metrics)))
        db.commit()
        return metrics
    except Exception as exc:
        db.rollback()
        codes = [x['code'] for x in exc.issues] if isinstance(exc, BatchRejected) else ['PROCESSING_ERROR']
        db.execute('BEGIN IMMEDIATE')
        try:
            run = db.execute('INSERT INTO runs(batch_id,status,metrics) VALUES (?,?,?)', (batch_id, 'rejected', json.dumps({'codes': codes}))).lastrowid
            db.executemany('INSERT INTO quarantine VALUES (?,?)', [(run, code) for code in codes])
            db.commit()
        except BaseException:
            db.rollback()
            raise
        raise

def backfill(db, start, end):
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    count = (last - first).days + 1
    if not 1 <= count <= 31:
        raise ValueError('Backfills must span 1 to 31 days')
    days = {(first + timedelta(days=i)).isoformat() for i in range(count)}
    db.execute('BEGIN IMMEDIATE')
    try:
        refresh(db, days)
        db.execute('INSERT INTO runs(batch_id,status,metrics) VALUES (?,?,?)',
                   ('backfill', 'committed', json.dumps({'start': start, 'end': end, 'days': count})))
        db.commit()
    except BaseException:
        db.rollback()
        raise

def snapshot(db, observed_at):
    now = timestamp(observed_at)
    received = db.execute('SELECT MAX(received_at) FROM versions').fetchone()[0]
    lag = (now - timestamp(received)).total_seconds() if received else None
    daily = [dict(r) for r in db.execute('SELECT * FROM daily ORDER BY day,channel,currency')]
    expected = db.execute('SELECT COALESCE(SUM(amount),0) FROM current_returns').fetchone()[0]
    payment = db.execute('SELECT COALESCE(SUM(amount),0) FROM payments').fetchone()[0]
    reconciled = sum(r['return_amount'] for r in daily) == expected and sum(r['payment_amount'] for r in daily) == payment
    last = db.execute('SELECT status FROM runs ORDER BY id DESC LIMIT 1').fetchone()
    return {'observed_at': observed_at, 'freshness_threshold_seconds': 86400,
            'latest_received_at': received, 'freshness_lag_seconds': lag,
            'freshness': 'healthy' if lag is not None and 0 <= lag <= 86400 else 'alert',
            'latest_attempt': last[0] if last else 'none', 'reconciled': reconciled,
            'checkpoint': db.execute('SELECT COALESCE(MAX(checkpoint),0) FROM batches').fetchone()[0],
            'rejected_runs': db.execute("SELECT COUNT(*) FROM runs WHERE status='rejected'").fetchone()[0],
            'source_versions': db.execute('SELECT COUNT(*) FROM versions').fetchone()[0],
            'daily': daily, 'daily_sha256': digest(daily)}

def reader(path, role):
    """Local query guard, not an authentication boundary against the filesystem owner."""
    if role not in {'analyst', 'auditor'}:
        raise ValueError('Unknown role')
    db = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
    allowed = {'daily'} if role == 'analyst' else {'daily', 'payments', 'versions', 'deliveries', 'current_returns', 'batches', 'runs', 'quarantine', 'settings'}
    def authorize(action, arg1, arg2, database, trigger):
        if action == sqlite3.SQLITE_SELECT:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ and database in {'main', None} and arg1 in allowed:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_FUNCTION and arg2.lower() in {'sum', 'count', 'min', 'max', 'avg', 'coalesce', 'round'}:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    db.set_authorizer(authorize)
    return db

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    ingest = sub.add_parser('ingest'); ingest.add_argument('records'); ingest.add_argument('manifest')
    status = sub.add_parser('status'); status.add_argument('--at', required=True)
    repair = sub.add_parser('backfill'); repair.add_argument('start'); repair.add_argument('end')
    args = parser.parse_args()
    db = connect(args.db)
    try:
        if args.command == 'init':
            initialize(db, json.loads((ROOT/'fixtures/banking_scenarios.json').read_text())['tables']['payment_order'])
        elif args.command == 'ingest':
            print(json.dumps(apply_batch(db, json.loads(Path(args.records).read_text()), json.loads(Path(args.manifest).read_text())), indent=2))
        elif args.command == 'status':
            print(json.dumps(snapshot(db, args.at), indent=2))
        else:
            backfill(db, args.start, args.end)
    finally:
        db.close()

if __name__ == '__main__':
    main()
