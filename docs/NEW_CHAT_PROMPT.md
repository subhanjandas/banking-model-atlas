# Paste this into the new chat

I am Subhanjan Das. Help me build and deploy a separate, substantial banking data platform portfolio project. I want you to implement it, not just propose a roadmap.

Our existing project is https://github.com/subhanjandas/banking-model-atlas and its live explorer is https://subhanjandas.github.io/banking-model-atlas/. Leave that repository and deployment intact.

First read these files from the existing repo:
- docs/PLATFORM_HANDOFF.md
- docs/ENGINEERING_LAB.md
- docs/VALIDATION_COVERAGE.md
- docs/INTERVIEW_GUIDE.md
- README.md and model/banking.model.json

Inspect the actual code and latest CI results. Do not assume you remember the previous chat. Record the exact Atlas commit you use. Reuse selected definitions, synthetic fixtures, invariants and tests with provenance; implement the new platform in a separate repo.

My goal is a polished, live fictional banking web application backed by a real persistent API and an end-to-end data engineering pipeline. It should eventually serve customers, employees, businesses and a non-resident/NRI persona, with accounts, simulated transactions, partial returns, loans, approvals, analytics and an engineering control room. All identities and funds must be synthetic. It must show real persistence, authorization, processing, reconciliation and measured evidence—not dashboards backed only by static mock arrays.

I like the breadth of https://github.com/ShrutiMokhashi34/Banking_Data_Platform and https://bankingdataplatform.web.app/. Use them as inspiration, not unlicensed code to copy. The Atlas visual style—clean light mode and muted Dusk—should carry through, with clear explanations and a small professional credit to Subhanjan Das.

Start by resolving only the decisions that materially affect the architecture: bank geography (Atlas is Canadian, while NRI suggests India), repository name, deployment provider and spending ceiling. Propose sensible defaults. Do not provision paid infrastructure before the budget is agreed.

Then build release 0 and the first end-to-end payment slice from the handoff: customer session → owned account → idempotent simulated payment → balanced ledger → transactional outbox → durable worker → validated analytical data → reconciled dashboard. Include an operations view and pipeline run history. Expand into loans, business approvals and non-resident journeys in later tested releases.

Enforce authorization server-side and test cross-customer/organization denial. Include replay, duplicate requests, worker crashes, late corrections, schema compatibility and source completeness tests. Show refresh timestamps and distinguish activity metrics from settled cash. Keep a complete local startup path, CI, migration/rollback guidance, seeded demo users, screenshots and honest limitations. Use natural, concise documentation suitable for interviews.

Work autonomously on authorized reversible steps, test meaningful risks, and publish working checkpoints through my connected GitHub when available. Keep docs/PROJECT_STATE.md current so another chat can continue without relying on memory. Begin by inspecting the source and producing a concrete first implementation checkpoint.
