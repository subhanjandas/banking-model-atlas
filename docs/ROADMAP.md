# Roadmap

## Delivered

Application 0.3.0 / model 0.2.0 adds 24 entities to the original 30. Twelve domains and six connected journeys cover cards, onboarding, deposit payments, term lending and selected accounting. The graph retains filters, search, metadata panels, links and downloads. The DuckDB schema and synthetic demonstration are executable.

## Next meaningful extensions

1. Extend the implemented lifecycle checks to ownership overlaps, replacement cycles and late-arriving correction events.
2. Opening and closing trial balances and control-account reconciliation are implemented for the supplied period. Next: external-source completeness and close exception handling.
3. Full payment returns and reversals are implemented. Next: partial returns and idempotent ingestion with late-arriving settlement observations.
4. Introduce a clearly scoped analytical layer, such as daily card balances and payment reconciliation exceptions, with grain-safe queries.
5. Add migration/version comparison before changing stable identifiers or column semantics.

More entities should answer a new business question. The project is an original fictional reference model, not an entire core-banking system or a claim of industry-standard compliance.

Application 0.4.0 adds the Dusk theme, 56 entities, 19 SQL checks and complete sample-period ledger reconciliation.
