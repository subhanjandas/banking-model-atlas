# Roadmap

## Delivered

Application 0.3.0 / model 0.2.0 adds 24 entities to the original 30. Twelve domains and six connected journeys cover cards, onboarding, deposit payments, term lending and selected accounting. The graph retains filters, search, metadata panels, links and downloads. The DuckDB schema and synthetic demonstration are executable.

## Next meaningful extensions

1. Strengthen lifecycle checks: valid event transitions, ownership overlaps, replacement cycles and correction events.
2. Add a bank opening trial balance and reconcile ledger account balances end to end. Current checks cover transaction journals and selected customer-entry mappings.
3. Model payment returns and reversals with idempotent ingestion and late-arriving settlement observations.
4. Introduce a clearly scoped analytical layer, such as daily card balances and payment reconciliation exceptions, with grain-safe queries.
5. Add migration/version comparison before changing stable identifiers or column semantics.

More entities should answer a new business question. The project is an original fictional reference model, not an entire core-banking system or a claim of industry-standard compliance.
