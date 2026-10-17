# Senior engineering evidence: implementation status

All five priorities below now have bounded local implementations in application 1.2.0. See [the lab, tests and explicit limitations](ENGINEERING_LAB.md). The original acceptance targets are retained below for context; peak-memory measurements, hosted alert delivery, SCD2 dimensions and production authentication remain outside this release.

| Priority | Deliverable | Evidence of completion |
|---|---|---|
| 1. Persistent incremental processing | A batch registry, checkpoint/offset state, transactional publish and bounded backfill command | Repeat a batch with no duplicate effects; crash between stages; resume with identical final checksums; demonstrate a targeted correction without rebuilding all history |
| 2. Analytical data product | A small daily payment/return fact and dimensions, with explicit grain and an SCD history decision | Source-to-fact reconciliation, fan-out tests, late-change recomputation and documented metric definitions |
| 3. Operational observability | Freshness/completeness thresholds, run-level metrics, a durable rejection queue and recovery runbook | Inject a missing file or failed stage; show detection, triage and restoration of the last good result |
| 4. Performance and cost | Seeded 100K/1M-row workloads, query plans and one measured optimization | Reproducible hardware/runtime notes, repeated timings, memory/scan sizes and unchanged result checksums; no invented savings |
| 5. Evolution and governance | A breaking-change check, migration example, source ownership and implemented access/masking policy in a chosen target | A deliberately incompatible schema fails CI; a versioned consumer survives the approved migration; restricted fields cannot be read by the test role |

## Original planning rationale

The implementation builds priorities 1 and 2 around **daily payment and return reconciliation**. Keep the current no-server DuckDB demo as the fast reference. Use a separate implementation path for persistent state rather than claiming the existing in-memory replay is incremental.

A small dbt project could provide model contracts, dependency-aware transformations and data tests for the analytical product. It is optional; choose it for those specific needs. A contract checks output shape, while business-data tests check row-level or aggregate assertions. They are complementary.

Primary references:
- https://docs.getdbt.com/guides/mesh-qs
- https://docs.getdbt.com/docs/build/data-tests

## A strong interview sequence

1. Explain a banking distinction in the graph.
2. Run a valid financial reconciliation.
3. Break a source record without changing the row count; show the fingerprint mismatch.
4. Replay duplicate and out-of-order deliveries; show the same curated financial result.
5. Reject an incomplete batch; show that the last published dataset is unchanged.
6. Explain the remaining gap: durable state, concurrent writers and post-close corrections.

That sequence demonstrates domain understanding, correctness, failure handling and judgment. It is stronger evidence than claiming enterprise scale based on schema size.
