# Banking Model Atlas

**An interactive map of how a fictional retail bank's data fits together.**

Imagine a customer calls about a purchase they do not recognize. The service team needs to connect a person, an account, a particular card, a merchant, a posted transaction, and a dispute case. Those are different things, often recorded by different systems. A good data model makes the connections explicit.

Banking Model Atlas is being built to make those connections visible. The explorer lets you browse domains, search tables and columns, follow relationships, and read the business meaning behind each field. Six guided journeys show how the model helps answer everyday questions.

**Application 0.4.0 · model 0.3.0.** Explore 56 entities across 12 domains, with six guided journeys and JSON, dictionary, PNG and executable DuckDB schema downloads. The repository includes synthetic banking records and checks that reconcile selected account activity and journals.

**[Open the live explorer](https://subhanjandas.github.io/banking-model-atlas/)** · [Run the banking demo](docs/SQL_AND_DEMO.md) · [Read the coverage boundaries](docs/VALIDATION_COVERAGE.md)

Run the viewer with `npm ci` and `npm run dev` (Node.js 22.12+). GitHub Actions tests and publishes the site on pushes to `main`.

## What is in this project?

| Item | Included |
|---|---:|
| Business domains | 12 |
| Entities | 56 |
| Documented columns | 324 |
| Explicit relationships | 95 |
| Specified business rules | 42 |
| Guided journey definitions | 6 |
| Automated metadata tests | 18 |
| Executable SQL tests | 30 |
| Synthetic records | 175 |
| Explorer unit tests | 20 |
| Browser interaction scenarios | 9 |

The JSON model is the source of truth. The catalogue, dictionary, relationship register, business-rule reference, and journey guide are generated from it. That means a description shown in the website comes from exactly the same place as the downloadable documentation.

## Meet the bank

Maple Harbour Bank is fictional. It serves individual customers in Canada and offers deposit accounts, credit cards and fixed-term loans. Customers can open accounts, share a deposit account with another owner, receive a primary or supplementary credit card, make purchases, repay a credit-card account, receive monthly statements, and raise a dispute.

We use realistic situations without claiming to reproduce any actual bank's architecture. No employer schemas, customer records, internal documents, or private business rules are included. The definitions are original design choices for this project. All future examples must be synthetic.

The model now follows onboarding, deposit transfers, lending and selected accounting entries alongside card servicing. These are deliberately connected: a loan application leads to a contract, funding affects customer accounts, and booked entries can be traced to journal lines. Each connection answers a business question.

## A few terms before the diagram

An **entity** represents a business thing, such as a customer or statement. A **table** is one way to store records of that thing. The **grain** tells you exactly what one record means. For example, a statement line is one booked entry displayed on one statement, not an entire month's spending.

A **primary key** identifies a record. A **foreign key** points to a record elsewhere. **Cardinality** describes how many records can be connected: an account can have many cards, while each card belongs to one account. A **domain** groups related ideas to make the model easier to navigate; it does not necessarily represent a separate database or software team.

A foreign-key arrow cannot express every rule. It can say that a refund points to a transaction. It cannot, by itself, prove that the transaction is a purchase, that the currencies match, or that several refunds do not exceed the purchase. Those conditions are specified separately.

## Explore the domains

| Domain | Entities | Why it exists |
|---|---|---|
| Customers | customer, customer_address, customer_contact, customer_consent | Identify people and explain their contact information and recorded choices. |
| Bank and reference data | branch, channel, currency | Give shared concepts one consistent meaning. |
| Products | product, product_version, fee_type | Separate an offering from the version of its terms an account was opened under. |
| Accounts and credit | account, account_holder, account_status_event, credit_facility, credit_limit_event | Describe the account, its owners, its lifecycle, and its approved credit. |
| Cards | card, card_assignment, card_status_event | Separate the account from the instrument and the person allowed to use it. |
| Merchants and activity | merchant_category, merchant, card_authorization, card_transaction, account_entry | Follow an attempted purchase through posting and its effect on an account. |
| Payments and statements | payment, statement, statement_line, account_balance_snapshot | Explain repayments, issued billing documents, and supplied daily balances. |
| Disputes | dispute_reason, dispute, dispute_event | Record a claim and follow the case without confusing it with a refund. |

| Onboarding | onboarding_case, identity_check, kyc_review, screening_review, customer_risk_assessment, product_application | Preserve decisions and evidence references without pretending to implement a compliance engine. |
| Deposit payments | beneficiary, standing_order, payment_order, payment_event, payment_settlement, account_hold | Separate a request to move money from its lifecycle and settlement observation. |
| Lending | loan_application, credit_decision, loan_contract, loan_schedule_item, loan_disbursement, loan_repayment | Keep an application, approved contract, funding and principal repayment distinct. |
| Accounting and reconciliation | gl_account, journal, journal_line, posting_link, reconciliation_run, reconciliation_item, gl_balance_snapshot, account_gl_mapping | Explain balanced journals and trace selected customer entries to the ledger. |

Read the [entity catalogue](docs/ENTITY_CATALOGUE.md) for every entity's definition and grain, or the [data dictionary](docs/DATA_DICTIONARY.md) for every column.

## The decisions behind the model

### An account is not a card

The account is the customer-facing financial relationship. A card is an instrument used against a credit-card account. If a card is replaced, the account continues. Purchases made with the old card stay linked to the old card, which is important when investigating historical activity.

We keep replacement links but require them to point to an older card on the same account, without cycles. We do not store card numbers, security codes, PINs, or digital wallet tokens.

### Ownership is not permission to use a card

Two people may jointly own a deposit account. In this scenario, a credit-card account has one primary owner, and additional people can be assigned supplementary cards. A supplementary user does not automatically become an account owner.

That is why `account_holder` and `card_assignment` are separate entities. Combining them would make it difficult to answer who owns the account versus who used a card. These are the rules of this fictional bank, not a universal statement about every issuer's products.

### Approval is not posting

An authorization is a request to approve spending. A posted transaction is a purchase or refund that reached the account activity model. Some authorizations never become purchases, and some posted activity may not have a matching authorization in the available data.

The authorization link is therefore optional. Several presentments can refer to one authorization. We deliberately avoid the tempting but inaccurate assumption that every authorization maps to exactly one transaction for exactly the same amount.

### A refund is not a dispute

A refund is posted financial activity that references a purchase. A dispute is a customer's claim about a purchase. Opening a case does not mean the merchant refunded anything, and resolving a case does not automatically create a financial entry in this model.

Partial refunds are allowed, but their total cannot exceed the original purchase. Provisional credits and chargeback-network messages will need a separate extension.

### A statement is a document with a fixed history

An issued statement captures one billing period. Its lines point to immutable account entries, so a later change in customer details or merchant naming does not rewrite the financial history. Periods use a clear boundary: the start date is included, and the end date is excluded.

For a credit-card account, the statement closes at opening balance plus debits minus credits. A negative balance means the customer is in credit. Minimum payment is a supplied value here; we do not pretend to implement an issuer's interest or payment-allocation engine.

### Account entries are not a complete general ledger

`account_entry` explains a debit or credit visible on a customer's account. It is useful for statements and reconciliation. A separate accounting domain supplies a small chart of accounts, balanced journal legs and explicit posting links. Customer activity and accounting keep separate grains; the demo checks their selected mappings. Independent opening and closing trial balances now reconcile every supplied ledger account. Customer-account balances reconcile to deposit, card and loan control accounts. A production period-close platform remains outside scope.

For deposit accounts, credits increase funds and debits reduce them. For credit-card and term-loan accounts, debits increase the amount owed and credits reduce it. Keeping the account kind explicit avoids presenting one sign convention as correct for every balance.

### We keep selected history without inventing an enterprise temporal framework

Account and card status changes are events. Ownership and card assignments have validity intervals. Product terms have versions. These choices support the questions the explorer needs to explain.

Other attributes, including customer segment and merchant category, are current-state values in this release. We do not claim that every attribute can be reconstructed at every historical moment. Explicit transition matrices now validate complete payment, account and card histories. Late-arriving corrections and production event ingestion remain outside scope.

## Six journeys through the graph

**Investigate a disputed purchase.** Start with the person, identify the card they could use at the purchase time, find the posted purchase and merchant, then examine the dispute and its history. The model keeps the financial event and case lifecycle distinct.

**Explain a monthly statement.** Start with an account and statement, inspect its lines and booked entries, then branch into purchases, repayments, and fees. This is a set of related paths, not an instruction to join every table into one giant query. Joining several one-to-many tables without controlling the grain can multiply amounts.

**Onboard a customer.** Follow an application through recorded identity, KYC and screening outcomes. The model stores outcomes; it does not decide whether a real customer meets legal requirements.

**Trace a deposit payment.** Follow a payment instruction, its events, its destination and a settlement observation. A request being accepted is different from money being settled.

**Fund a term loan.** Connect an application and decision to a contract, principal account, repayment schedule and disbursement.

**Reconcile to the ledger.** Trace a customer entry through its allocation to journal lines and a reconciliation observation. Aggregating at the right grain prevents counting the same money twice.

The exact highlighted entities and edges are stored in the model and documented in [JOURNEYS.md](docs/JOURNEYS.md).

## Explore the interactive model

Use the moon/sun button in the header to switch between the original light theme and Dusk: slate surfaces, warm text and muted sage accents. Your choice is saved locally; a first visit follows your device preference. Graphs and PNG exports follow the selected theme.

The left panel contains domains and search. The centre shows the graph. Selecting an entity or relationship opens a right-hand inspector with definitions, grain, columns, keys, and business rules.

The Domains view emphasizes the twelve business areas; the Tables view shows grouped entities and key fields. These are explicit view controls, rather than automatic zoom transitions. Full column lists live in the inspector so the canvas remains readable. Search finds entity and column names and column descriptions. Table focus shows immediate neighbours, and journey presets highlight a meaningful subset of the model.

The stack is React, TypeScript, Vite, and Cytoscape.js. The viewer runs entirely in the browser from versioned model metadata. Database access and AI generation are not required to explore the model. See the [explorer specification](docs/EXPLORER_SPEC.md) for interaction and acceptance criteria.

## Run the foundation checks

Use Python 3.10 or newer. Metadata validation uses the standard library. The full replay also installs DuckDB; no database server, cloud account or credentials are required.

From the repository root:

```bash
python3 -m pip install -r requirements-demo.txt
python3 replay.py
```

After editing `model/banking.model.json`, regenerate the reference documents:

```bash
python3 scripts/render_docs.py
python3 scripts/export_sql.py
python3 scripts/run_demo.py --write-report
```

The validator checks metadata: identifiers, references, key types, cardinality consistency, rule links, and connected journey subgraphs. The tests deliberately break the model to verify that common errors are rejected.

The operational examples preserve original payment entries and append full internal reversals or settled outbound returns. Payment, card and account histories follow documented transition matrices. See [the operational guide](docs/OPERATIONS.md) for exact semantics and limitations.

The full replay also executes all 56 tables, loads 175 synthetic records across 49 tables, checks all 95 relationships and runs 19 business-data checks. Negative tests deliberately introduce financial errors. See [the exact coverage and limits](docs/VALIDATION_COVERAGE.md).

All 42 rules retain `specified_not_implemented` because their complete enforcement plans are not implemented. Selected executable checks cover parts of those specifications; they do not establish compliance or production readiness. The browser labels this distinction explicitly.

## Where to find things

| Path | Purpose |
|---|---|
| `model/banking.model.json` | Authoritative model and explorer content. |
| `docs/SCENARIO.md` | Scenario boundaries and a worked fictional example. |
| `docs/MODEL_CONTRACT.md` | Metadata structure and interpretation rules. |
| `docs/ENTITY_CATALOGUE.md` | Generated entity definitions and grains. |
| `docs/DATA_DICTIONARY.md` | Generated column definitions and classifications. |
| `docs/RELATIONSHIPS.md` | Generated relationship endpoints and cardinalities. |
| `docs/BUSINESS_RULES.md` | Generated rule specifications. |
| `docs/JOURNEYS.md` | Generated guided-journey definitions. |
| `docs/DECISIONS.md` | Design decisions, benefits, and trade-offs. |
| `docs/EXPLORER_SPEC.md` | Planned interface behavior and acceptance criteria. |
| `docs/ROADMAP.md` | Checkpoint status and next implementation steps. |
| `docs/PUBLISHING.md` | Repository creation and future site publication. |
| `src/` | React interface, graph adapter and model navigation. |
| `docs/EXPLORER_IMPLEMENTATION.md` | How to run, test and understand the viewer. |
| `scripts/` | Metadata validation, documentation generation and CI serving. |
| `tests/` | Metadata, SQL negative-data, graph and browser tests. |
| `fixtures/banking_scenarios.json` | Synthetic records with independently specified expected balances. |
| `model/validation_checks.json` | Executable queries and explicit coverage limits. |
| `generated/` | Reproducible DuckDB schema and observed demo report. |
| `.github/workflows/validate.yml` | The same checks for GitHub Actions. |

## What we are leaving out

This release excludes corporate customers, mortgages, variable-rate loan engines, investments, treasury, a complete general ledger, payment clearing networks, foreign exchange, interest calculation, fraud scoring, regulatory reporting, and a compliance implementation. Authentication and access control are also outside the public metadata viewer.

CAD is the only supported currency. UTC timestamps represent instants; America/Toronto determines business dates. Monetary columns use a logical decimal type. JSON sample amounts are decimal strings rather than binary floating-point numbers.

Descriptions of personal fields are included to explain data classification, but actual personal data must never enter this repository. Classification labels are descriptive metadata, not masking policies or access controls.

## Inspiration and authorship

The [Databricks Lakehouse Industry Data Models project](https://github.com/databricks-industry-solutions/lakehouse-industry-data-models) inspired the idea of browsing a model visually. Its source and banking model have not been copied into this project. This is an independent educational implementation, with no affiliation or endorsement.

The foundation was built for Subhanjan Das with AI assistance. Definitions and trade-offs are explicit so they can be reviewed, questioned, and improved. The goal is a model that can be explained, not a large diagram whose assumptions are hidden.

Original project files are released under the MIT license. Upstream projects retain their own licenses.
