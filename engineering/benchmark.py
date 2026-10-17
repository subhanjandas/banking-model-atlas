"""Measured SQLite covering-index experiment; this is not a bank-scale SLA."""
import argparse
import hashlib
import json
import platform
import random
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path

QUERY = 'SELECT channel,SUM(amount),COUNT(*) FROM activity WHERE day=? GROUP BY channel ORDER BY channel'

def measure(db, repetitions):
    result = db.execute(QUERY,(180,)).fetchall()  # Warm cache before timed repetitions.
    elapsed=[]
    for _ in range(repetitions):
        start=time.perf_counter(); current=db.execute(QUERY,(180,)).fetchall()
        elapsed.append((time.perf_counter()-start)*1000)
        assert current==result
    return {'median_ms':round(statistics.median(elapsed),4),'samples_ms':[round(t,4) for t in elapsed],
            'plan':[r[3] for r in db.execute('EXPLAIN QUERY PLAN '+QUERY,(180,))],
            'result_sha256':hashlib.sha256(json.dumps(result).encode()).hexdigest()}

def benchmark(size, repetitions=5):
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'benchmark.sqlite';db=sqlite3.connect(path)
        db.execute('CREATE TABLE activity(id INTEGER PRIMARY KEY,day INTEGER,channel TEXT,amount INTEGER)')
        rng=random.Random(42)
        start=time.perf_counter()
        db.executemany('INSERT INTO activity VALUES (?,?,?,?)',
                       ((i,rng.randrange(365),('WEB','APP','BRANCH')[rng.randrange(3)],rng.randrange(1,100000)) for i in range(size)))
        db.commit();load=time.perf_counter()-start
        before_bytes=path.stat().st_size
        before=measure(db,repetitions)
        start=time.perf_counter();db.execute('CREATE INDEX activity_cover ON activity(day,channel,amount)');db.commit()
        index_seconds=time.perf_counter()-start
        after=measure(db,repetitions)
        assert before['result_sha256']==after['result_sha256']
        result={'rows':size,'seed':42,'repetitions':repetitions,'load_seconds':round(load,3),
                'index_build_seconds':round(index_seconds,3),'table_bytes':before_bytes,'indexed_bytes':path.stat().st_size,
                'before':before,'after':after,'result_match':True}
        db.close();return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--sizes',type=int,nargs='+',default=[100000,1000000]);parser.add_argument('--output',default='generated/benchmark-report.json');args=parser.parse_args()
    result={'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,'system':platform.system(),'machine':platform.machine()},
            'method':'Seed 42, uniform 365-day distribution, 3 channels, integer cents; 1 warm-up and 5 measured executions per plan. Index is built between experiments. Shared-host wall-clock timings; no concurrency or cold-cache claim.',
            'query':QUERY,'runs':[benchmark(n) for n in args.sizes]}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
