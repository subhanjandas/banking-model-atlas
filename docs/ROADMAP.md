# Release scope and next work

Application 1.0.0 is the portfolio reference release: 80 entities, 16 domains, ten journeys, light/Dusk themes, typed metadata panels, downloads and a repeatable tested financial scenario.

## Complete in this release

All 80 tables are validated and created by the DuckDB replay. The original 49 populated tables carry 175 synthetic records. Nineteen SQL checks and independent ledger reconciliation exercise the supplied financial scenario. Fraud, collections, rewards and customer-service additions are schema-only and clearly labeled. Ten journeys explain the relationships; they do not imply ten fully executed operational workflows.

## Highest-value next work

1. Add independently specified fixtures and negative tests for the four schema-only domains.
2. Handle partial payment returns, late-arriving corrections and idempotent source ingestion.
3. Add effective-time ownership checks, source completeness and model migration/version comparisons.
4. Add an analytical layer with declared fact-table grain and measured join correctness.
5. Review accessibility with screen-reader users and optimize large graphs if coverage grows beyond readable domain views.

## Not part of the portfolio finish

A production bank platform, regulatory certification, real customer integrations, multicurrency consolidation, production credit decisions and complete accounting close orchestration. These require separate engineering and domain review.
