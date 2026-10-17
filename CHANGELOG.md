# Application 0.4.0 / model 0.3.0

- Add full internal reversals and outbound returns while preserving original postings.
- Validate explicit payment, account and card lifecycle transitions.
- Add ledger snapshots and account control mappings; reconcile opening, movements and closing across the complete sample chart.
- Correct the loan repayment explanation: its funding is external cash, not a D1 debit.
- Add a persistent Dusk theme, system preference support and themed graph exports.

# Application 0.3.0 / model 0.2.0

- Expand from 30 to 54 entities and eight to twelve domains.
- Add onboarding, deposit payments, term lending and accounting with four new journeys.
- Generate executable DuckDB DDL and synthetic reconciliation examples.
- Add 13 selected business checks, negative-data tests and rule coverage notes.
- Keep existing model IDs, interface navigation and original journeys stable.

# Changelog

## 0.2.0 — 2026-10-16

Added the React/TypeScript/Cytoscape explorer: domain overview, table graph, search, column and relationship inspectors, neighbourhood focus, two journeys, URL state, mobile drawers, and JSON/dictionary/PNG downloads. Added 16 unit tests, six Chromium interaction scenarios, bundled fonts, and a GitHub Pages workflow. The model remains 0.1.0; banking-rule execution and SQL exports remain pending.

## 0.1.0 — 2026-10-16

First foundation checkpoint. Added the original Maple Harbour Bank scenario, eight domains, 30 entities, 161 columns, 45 relationships, 21 specified business rules, and two explorer journey definitions. Added plain-language design documentation, generated model references, a dependency-free metadata validator, 18 mutation tests and GitHub Actions configuration.

The UI, SQL exporter, sample dataset, business-rule execution and public deployment remain pending.
