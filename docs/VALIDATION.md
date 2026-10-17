# Validation evidence

Application 1.1.0 / model 0.5.0.

| Layer | Automated tests |
|---|---:|
| Metadata | 18 |
| SQL, domain fixtures, partial returns and ledger reconciliation | 43 |
| Source ingestion, completeness and publication safety | 16 |
| Explorer unit tests | 24 |
| Browser scenarios | 10 |
| Total | 111 |

The replay creates all 81 tables, loads 207 synthetic records across 74 tables, checks 130 relationships and executes 27 business queries. Eleven posted journals balance. Customer and ledger balances reconcile independently. The ingestion replay checks four deliveries against a separate manifest: three source versions become two curated return facts totaling CAD 75.

The query tests include deliberate excessive returns, invalid partial states, wrong reward balances and inconsistent case dates. Ingestion tests include same-count content corruption, missing versions, repeat deliveries, out-of-order input, unsupported contracts and preservation of the last good file after rejection.

Run python3 replay.py, npm test and npm run build. Actions runs Chromium before deployment and captures the public website afterward. Current Actions status is the authoritative evidence for the committed version. Generated reports reproduce the dataset results. README gallery captures retain their explicit 1.0.0 provenance until refreshed; the latest public-site captures are available in Actions artifacts.

Not claimed: full business policy coverage, completeness beyond the synthetic producer manifest, distributed exactly-once processing, persistent streaming state, post-close accounting restatements or production bank certification.
