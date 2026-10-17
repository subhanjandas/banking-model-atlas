# Engineering checkpoint: trustworthy inputs and richer scenarios

For the newer durable pipeline, daily analytics and governance examples, read [Engineering lab](ENGINEERING_LAB.md). This page documents the earlier source-ingestion checkpoint.

Application 1.1.0 / model 0.5.0. This release adds synthetic records for fraud, collections, rewards and customer service; partial payment returns; and a small, executable source-ingestion boundary.

## What actually runs

| Area | Demonstration | What remains outside it |
|---|---|---|
| Fraud | Case-alert association to a card user/account holder; decision chronology | Detection models, investigator correctness, action execution |
| Collections | Supplied arrears, a promise, contact and proposed support; amount/date/ownership checks | Calculating delinquency, fulfilling promises, eligibility policy |
| Rewards | 120 earned − 40 redeemed − 20 adjusted = 60 points | Earning-rate engine, expiration, household pooling |
| Service | Request, complaint, response and evidence references; ownership/date checks | SLA automation, regulatory complaint rules, transport verification |
| Returns | CAD 30 then CAD 45 against a settled CAD 75 payment | Fees, FX, intraday installment ordering, post-close restatement |
| Source ingestion | Duplicate suppression, source revisions, retrospective as-of views, manifest checks and atomic local publication | Distributed transactions, concurrent writers, durable offsets, stream watermarks |

Collections examples extend into November and service examples into October. They are separate supplied operational observations, not additional movements in September's financial period. Days past due is an input, not a value derived from the sample statement schedule.

## Partial returns preserve the original payment

The outbound payment remains at CAD 75, with its original debit and settlement. Return RET1 adds a CAD 30 customer credit and a balanced journal on September 26. RET2 adds another CAD 45 on September 28. The payment passes through PARTIALLY_RETURNED before RETURNED. The original source-account balance ends at the same value as the earlier full-return example.

Checks reject nonpositive installments, returns before settlement, over-returning, missing/wrong customer credits and return states inconsistent with cumulative amounts. A valid intermediate CAD 30 state is tested separately. Generic equal-and-opposite reversals remain the mechanism for full internal transfer corrections; outbound returns now have their own entity.

## Source deliveries are not curated facts

`fixtures/ingestion/return_deliveries.json` preserves four delivery envelopes:

| Source fact | Revision | Amount | Event date | First received |
|---|---:|---:|---|---|
| RET2 | 1 | 40.00 | September 28 | September 28 |
| RET1 | 1 | 30.00 | September 26 | September 29 |
| RET2 | 2 | 45.00 | September 28 | September 30 |
| RET1, repeated delivery | 1 | 30.00 | September 26 | September 30 |

The producer manifest is a separate, committed expectation. It declares three distinct source versions, their SHA-256 fingerprints and a revision control total of 115.00. That total includes the superseded 40.00 version; it is deliberately different from the current financial total of 75.00.

After validation, the highest known source revision wins for each business key. An identical repeat does not duplicate the financial amount. Different contents under the same key/version are a conflict and reject the batch. Unknown fields, float money, unsupported contract versions, missing records, unexpected records and changed fingerprints also block publication.

**Completeness is relative to the supplied producer manifest.** Hashes establish content agreement, not producer authenticity or completeness of the whole real world. The manifest is not cryptographically signed. Receipt timestamps are trusted collector metadata in this demonstration.

## What was known before the correction?

```python
import sys
sys.path.insert(0, "scripts")
from ingest_returns import inputs, process

records, manifest = inputs()
before = process(records, manifest, "2026-09-29T23:59:59Z")
after = process(records, manifest, "2026-09-30T23:59:59Z")
assert before["curated_total"] == "70.00"
assert after["curated_total"] == "75.00"
```

The entire archived batch is validated first; the cutoff then reconstructs a knowledge-time view. This is retrospective replay, not an assertion that the producer's future manifest was available on September 29. A revision wins by source version, not by whichever duplicate arrived last.

The correction is resolved **before the period's curated snapshot is published**. We do not rewrite posted journals when a source changes. A correction received after ledger close would require explicit adjusting postings and restatement policy, which are not implemented here.

## Failure and replay

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from ingest_returns import inputs, publish, BatchRejected

records, manifest = inputs()
with TemporaryDirectory() as directory:
    target = Path(directory) / "returns.json"
    publish(records, manifest, target)
    previous = target.read_bytes()
    try:
        publish(records[:1], manifest, target)  # intentionally incomplete
    except BatchRejected as error:
        print(error.issues)  # structured rejection reasons
    assert target.read_bytes() == previous
```

The publisher validates before writing, writes a temporary file in the destination directory, then uses `os.replace`. On the tested local POSIX filesystem, a successful replacement is atomic. This is not a cloud-object-store or distributed exactly-once guarantee, and there is no concurrent-writer lock or crash-recovery catalogue. Rejected rows are reported in structured exceptions; a durable quarantine store is future work.

Run the full checkpoint with:

```bash
python3 -m pip install -r requirements-demo.txt
python3 replay.py
```

Inspect `generated/ingestion-report.json` for lineage, selected source revisions, late/duplicate counts and control totals. The final projection is compared with the separately committed banking fixture. `generated/demo-report.json` records the financial reconciliation.

## What a senior engineer should explain

- Why source identity, delivery identity and business identity are different.
- Why a schema contract is not enough to establish data completeness.
- Why version totals and current financial totals must not be mixed.
- Why a late event and a correction are different conditions.
- What happens to the last good dataset when validation fails.
- Which guarantees are local to this implementation and which require transactional infrastructure.

Python publication semantics: https://docs.python.org/3/library/os.html#os.replace
