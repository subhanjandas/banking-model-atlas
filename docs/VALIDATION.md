# Validation evidence

Portfolio application 1.0.0 / model 0.4.0.

- 18 metadata regression tests: keys, types, references, cardinalities and connected journeys.
- 30 executable SQL/demo tests: valid records, 19 bad-data mutations, referential integrity and ledger checks.
- 24 explorer unit tests: filtering, search, links, journey subgraphs and graph construction.
- 10 browser scenarios: navigation, downloads, mobile layout, theme persistence, system theme and schema-only extension journeys.
- A separate post-deploy capture opens the public GitHub Pages URL and saves real screenshots with commit/time provenance.

The demo creates 80 tables and loads 175 synthetic records in 49 tables. Nineteen SQL business checks and opening-to-closing reconciliation pass for the supplied CAD scenario. The new four domains have no data fixtures; their DDL and metadata are checked, not their operational behavior.

Run python3 replay.py, npm test and npm run build. Actions runs the Chromium suite before deployment. The Actions result for a commit is the authoritative evidence of its execution. See generated/demo-report.json for reproducible data results and docs/assets/provenance.json for published screenshot provenance.

Remaining limits: complete rule enforcement, external source completeness, production concurrency, legal compliance and operational bank certification are not claimed.
