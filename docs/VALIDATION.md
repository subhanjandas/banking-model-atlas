# Validation evidence

Application 0.4.0 / model 0.3.0. The repository includes 18 metadata tests, 30 executable SQL tests, 20 explorer unit tests and nine browser scenarios.

The SQL replay creates 56 tables, loads 175 synthetic records across 49 tables, checks 95 relationships and executes 19 selected business queries. Ten posted journals balance. Expected closing account balances are checked independently. See generated/demo-report.json and VALIDATION_COVERAGE.md for exact scope.

Run `python3 -m pip install -r requirements-demo.txt`, then `python3 replay.py`, `npm ci`, `npm test` and `npm run build`. GitHub Actions runs these commands and the Chromium browser suite before deploying. Browser artifacts include overview, mobile and accounting-journey screenshots.

The previous explorer release deployed successfully in Actions run 38963395559. For the current commit's observed result, open the repository Actions tab: a configured workflow is not itself proof that a run passed. The deployment job runs only after the build and browser checks succeed.

These examples do not establish complete banking correctness, regulatory compliance or production readiness. Rules with partial query coverage still retain their specification status.
