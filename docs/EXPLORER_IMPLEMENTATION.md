# Explorer implementation

Application release: 0.3.0. Banking model release: 0.2.0. These are separate versions: building a viewer does not silently change banking semantics.

## What works

The application opens on a domain overview. Selecting a domain reveals its tables. The full table view groups entities by domain. The graph supports dragging, zooming, fitting to the viewport, table selection, relationship selection and self-reference inspection.

Search includes entity names, column names and column descriptions. A search selection reveals an entity even if a previous filter hid it. The inspector shows definitions, grain, columns, key markers, allowed values, classifications, unique keys, relationships, notes and rule specifications. Rule descriptions remain explicitly marked as not enforced against data.

Both journeys select their declared nodes and edges. Focus mode includes a table and its immediate neighbours. Browser URLs carry view, domain, entity, column, relationship, journey and focus state. Unknown selections fall back with a message, and browser back/forward restores state.

Downloads include the full model JSON, a Markdown data dictionary and a PNG of the current graph. The DuckDB schema download is generated and executed in the synthetic-data checks.

## Files and responsibilities

| File | Responsibility |
|---|---|
| src/model.ts | Typed model access, search, URL parsing, filters, neighbours and dictionary export. |
| src/graph.ts | Deterministic graph elements and positions; aggregated domain connections. |
| src/Graph.tsx | Cytoscape lifecycle, graph interaction, selection and image export. |
| src/App.tsx | Navigation, inspector, journeys, downloads and browser state. |
| src/styles.css | Responsive layout, typography, visual hierarchy and focus styles. |
| tests/explorer.test.ts | Model-to-graph and view-state checks, including headless graph construction. |
| tests/browser/explorer.spec.ts | Real Chromium interaction checks in GitHub Actions. |
| scripts/serve_browser_test.py | CI-only production-build server at the repository subpath. |
| .github/workflows/explorer.yml | Build, tests, browser evidence and Pages deployment. |

## Run locally

Use Node.js 22.12 or newer and Python 3.10 or newer.

```bash
npm ci
npm run dev
```

Open the local URL printed by Vite. To verify the production bundle:

```bash
python3 replay.py
npm test
npm run build
npm run preview
```

The browser suite is set up for CI. To run it on your own machine after building, install the test browser with `npx playwright install chromium`, then run `npm run test:browser`. Its server intentionally uses `/banking-model-atlas/`, so a broken repository-subpath build is caught before publication.

## Design choices

The overview is the starting point because a full 54-table graph is dense at laptop size. Domain filters and the neighbour view provide readable detail. The layout is deterministic rather than a continuously moving force simulation. Compound graph nodes group tables by domain; arrows point from the foreign key to the referenced key.

All data and fonts are bundled locally. Browsing does not call an LLM, database or analytics service. External links lead only to the source repository and its documentation. The fictional model contains definitions, not customer records.

The graph has a keyboard-accessible navigation alternative through domain buttons, search, the entity directory, and relationship lists. Mobile navigation and inspector panels are non-modal drawers; Escape closes them. The graph itself is still primarily a pointer/touch interface, and this release is not an accessibility certification.

## Remaining work

SQL exports, synthetic data and selected banking-rule checks are implemented; see SQL_AND_DEMO.md for their limits. Position persistence, model editing, version comparison and broader bank coverage are not implemented. Local browser QA is unavailable in the managed build environment; GitHub Actions provides the real-browser test run and screenshots. See VALIDATION.md for observed results rather than assuming the workflow passed.
