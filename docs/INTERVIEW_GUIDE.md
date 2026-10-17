# Explain the project in an interview

## A 30-second introduction

“I built Banking Model Atlas to make banking data models easier to explore and explain. It connects 80 entities across 16 domains through a searchable graph, with definitions, relationships and ten business walkthroughs. I also built an executable DuckDB reference schema and a synthetic financial scenario that tests payment corrections, lifecycle transitions and opening-to-closing ledger reconciliation. The broader schema and the tested scenario have different coverage, and the interface makes that distinction visible.”

Use this wording only when you can explain the code and decisions yourself. The project was built with AI assistance; understanding and reviewing the result matters more than claiming every line was handwritten.

## A five-minute demo

| Time | Show | Explain |
|---|---|---|
| 0:00–0:40 | Domain overview and theme toggle | Who this tool helps: analysts, engineers and people learning banking models. |
| 0:40–1:30 | Investigate a disputed purchase | Account ownership, card usage, posted transactions and case handling are different concepts. |
| 1:30–2:20 | Entity inspector and relationships | Grain, keys, optional relationships and business rules prevent misleading joins. |
| 2:20–3:20 | generated/demo-report.json | Opening + movements = closing. A balanced journal can still be wrong; independent snapshots catch that. |
| 3:20–4:10 | tests/test_ledger.py and tests/test_demo.py | Show a balanced-but-wrong closing balance and an excessive refund being rejected. |
| 4:10–5:00 | Fraud journey and schema-only badge | State limits honestly. Describe the next fixture and check you would implement. |

## Questions worth preparing for

**What kind of model is this?** A normalized relational reference model with an executable DuckDB physical projection. It is operationally oriented, not a Kimball star schema, Data Vault, complete lakehouse or enterprise canonical model. No claim of formal normalization proof is made.

**Why separate accounts and cards?** Accounts hold financial relationships. Cards are replaceable instruments. A replacement must not rewrite historical transactions or account ownership.

**Why separate an authorization and a transaction?** Approval is not posting. An authorization may expire, and available posted data may lack an authorization. The link is optional, with multiple presentments possible.

**Why can a foreign key not enforce a refund policy?** The foreign key proves the original row exists. It does not prove that row is a purchase, its currency matches, or all refunds together stay within the purchase amount. Those need row and aggregate checks.

**Why separate customer entries and journal lines?** They have different grains. A loan repayment can split principal and interest, and ledger-side cash has no direct customer-entry counterpart. Posting links make selected allocations explicit.

**What does the reconciliation actually prove?** For the supplied period and complete small chart, both trial balances balance, each ledger account rolls forward, every customer account rolls forward and its totals reconcile to the control account. It does not prove completeness against an unseen source feed.

**Why DuckDB?** It makes the reference executable without a server or cloud bill. Production transaction processing would require a different operational design, concurrency controls and migration strategy.

**How would you scale the explorer?** Keep metadata separate from rendering, retain stable IDs and default to a domain or journey. For thousands of nodes, add query-driven subgraphs and lazy metadata loading rather than drawing everything at once.

**What did AI do?** Be direct: AI assisted implementation and documentation. Explain the validation process, assumptions you reviewed, bugs found and what you can independently defend. Do not present this as employer work or use internal bank schemas.

## Avoid these claims

Do not say “production banking platform,” “BIAN compliant,” “regulatory compliant,” “all rules enforced,” or “80 tables fully tested with data.” All 80 tables are created by the schema replay; 49 contain synthetic records. The four latest domains are modeled extensions with no operational fixtures yet.
