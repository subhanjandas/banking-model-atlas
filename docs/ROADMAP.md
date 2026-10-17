# Release scope and next work

Application 1.1.0 / model 0.5.0 adds fixtures across all 16 domains, partial return installments and a deterministic batch-ingestion boundary. The model has 81 entities, 130 relationships and 459 columns; 207 records populate 74 tables. Seven tables remain schema-only.

The engineering examples cover selected domain checks, producer-manifest completeness, source revisions, duplicate suppression and failed-batch publication safety. These are local reference implementations, not distributed production guarantees.

Application 1.2.0 implements a local persistent pipeline, daily activity mart, operational signals, measured 100K/1M benchmarks, migration and access tests. See ENGINEERING_LAB.md. The next application is intentionally a separate repository; see PLATFORM_HANDOFF.md.
