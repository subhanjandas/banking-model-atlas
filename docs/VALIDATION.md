# Validation evidence

Application 0.3.0 / model 0.2.0. The repository includes 18 metadata tests, 16 executable SQL tests, 20 explorer unit tests and seven browser scenarios.

The SQL replay creates 54 tables, loads 137 synthetic records across 47 tables, checks 92 relationships and executes 13 selected business queries. Eight posted journals balance. Expected closing account balances are checked independently. See generated/demo-report.json and VALIDATION_COVERAGE.md for exact scope.

Run `python3 -m pip install -r requirements-demo.txt`, then `python3 replay.py`, `npm ci`, `npm test` and `npm run build`. GitHub Actions runs these commands and the Chromium browser suite before deploying. Browser artifacts include overview, mobile and accounting-journey screenshots.

The previous explorer release deployed successfully in Actions run 38963392559. For the current commit's observed result, open the repository Actions tab: a configured workflow is not itself proof that a run passed. The deployment job runs only after the build and browser checks succeed.

These examples do not establish complete banking correctness, regulatory compliance or production readiness. Rules with partial query coverage still retain their specification status.
