# Validation record

Date: 2026-10-16. Application: 0.2.0. Banking model: 0.1.0.

## Observed locally

- All 18 Python metadata tests passed.
- All 16 explorer unit tests passed, including URL-state normalization, search, domain filtering, exact journey edges, self-references, deterministic layout, and headless Cytoscape graph construction.
- TypeScript compilation and the Vite production build succeeded.
- Generated model documentation matched fresh generation.
- The original foundation GitHub Actions run passed at commit `55e19d4`.

## Browser and deployment status

Six Chromium interaction scenarios are configured in GitHub Actions against the production build under `/banking-model-atlas/`. They cover navigation, self-reference inspection, filtered search, bookmarks, journeys, focus/reset/history, three downloads and a mobile inspector. Screenshots and failure traces are retained as the `browser-evidence` artifact.

The managed local environment does not provide the required browser-control skill, so no local browser was launched. At commit `4a0bf35`, all six Chromium scenarios passed in run [38918446994](https://github.com/subhanjandas/banking-model-atlas/actions/runs/38918446994), along with the build, unit tests and Python checks. Desktop overview, journey and mobile-inspector screenshots were reviewed. That review led to a compact layout for journeys and neighbourhoods, preserving context when a table is selected; this refinement is covered by the next CI run.

Deployment failed specifically at `actions/configure-pages`: GitHub returned “Not Found” and asked for Pages to be enabled with GitHub Actions as the source. No public site is claimed. Enable the one-time setting described in PUBLISHING.md, then rerun deployment.

## Deliberate limits

No banking records were generated or validated. No SQL dialect was executed. Rule specifications are not transaction-level enforcement, and there is no production or compliance certification.

## Replay

Run `python3 replay.py`, `npm test`, and `npm run build`. The CI browser command is `npm run test:browser` after installing Chromium. Run `python3 verify_package.py` before editing to verify release files. After intentional changes, `python3 scripts/update_manifest.py` refreshes the manifest; it is not a test and should not be used to conceal unexpected edits.
