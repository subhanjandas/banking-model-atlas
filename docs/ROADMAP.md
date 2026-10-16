# Roadmap and checkpoint status

## Hour 1 — foundation

Completed locally: fictional scenario, 30-entity model, 161 column definitions, 45 relationships, 21 rule specifications, two connected journey definitions, metadata validator, 18 tests, generated reference documents, explorer specification and CI configuration.

Foundation published to `subhanjandas/banking-model-atlas` in commit `55e19d4`. The foundation GitHub Actions run passed.

## Application 0.2.0 — explorer implemented

Implemented the application shell, all 30 tables, domain overview, graph navigation, entity and relationship inspectors, search and responsive drawers.

Implemented both journeys, neighbourhood focus, URL state, and JSON/dictionary/PNG downloads. Browser tests target the production repository subpath. Publication depends on GitHub Pages configuration; see VALIDATION.md for the actual verification state.

## Following — evidence and export

Build one tested SQL dialect exporter. Generate synthetic data only after the business rules have executable tests. Turn the worked scenario into a reconciliation fixture. Add bad-data fixtures for refunds, ownership intervals, replacements and statement membership.

## Longer term

Statement reissues, fuller lifecycle transition rules, product migrations, provisional credits and a broader deposit-activity model. AI-assisted drafting is optional and must not replace deterministic structural checks or domain review.

## Scope rule

The one-day target is a polished educational explorer. Increasing entity count further should require a new business question, not a desire to make the graph larger. Public claims must distinguish specified, locally tested, and actually deployed features.
