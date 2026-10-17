# Contributing

Start with the live explorer and docs/MODEL_CONTRACT.md. This is an original fictional model: do not submit employer schemas, actual customer data, credentials or proprietary documents.

For a model change, describe the business question, one-row grain, keys, relationships, rule implications and coverage limits. Keep existing IDs stable where possible. New domains need a coherent question and a connected journey, not just more tables.

```bash
npm ci
python3 -m pip install -r requirements-demo.txt
python3 scripts/render_docs.py
python3 scripts/export_sql.py
python3 scripts/run_demo.py --write-report
python3 replay.py
npm test
npm run build
python3 scripts/update_manifest.py
python3 verify_package.py
```

Browser tests run in GitHub Actions before Pages deployment. On a local machine with Playwright Chromium installed, use npm run test:browser. Explain which tests you ran and which you could not run in your pull request. New operational behavior needs both a valid fixture and a deliberately invalid example that the check rejects.

Reviewers check business meaning, model integrity, reproducibility, documented boundaries and interface readability. Screenshot evidence must come from the application; do not present generated mockups as live results.
