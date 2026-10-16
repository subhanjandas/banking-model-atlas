# Banking Model Atlas

**An interactive map of how a fictional retail bank's data fits together.**

Imagine a customer calls about a purchase they do not recognize. The service team needs to connect a person, an account, a particular card, a merchant, a posted transaction, and a dispute case. Those are different things, often recorded by different systems. A good data model makes the connections explicit.

Banking Model Atlas is being built to make those connections visible. The planned explorer will let you browse domains, search tables and columns, follow relationships, and read the business meaning behind each field. Two guided journeys will show how the model helps answer everyday questions.

**Current release: `0.1.0` — Hour 1 foundation.** The model, definitions, journey specifications, structural validator, and documentation are here. The interactive website, SQL exports, synthetic records, and database execution are not built yet. This repository does not currently run a banking system or display a graph in a browser.

## What is in this checkpoint?

| Item | Included |
|---|---:|
| Business domains | 8 |
| Entities | 30 |
| Documented columns | 161 |
| Explicit relationships | 45 |
| Specified business rules | 21 |
| Guided journey definitions | 2 |
| Automated metadata tests | 18 |

The JSON model is the source of truth. The catalogue, dictionary, relationship register, business-rule reference, and journey guide are generated from it. That means a description shown in the future website can come from exactly the same place as the downloadable documentation.

## Meet the bank

Maple Harbour Bank is fictional. It serves individual customers in Canada and offers deposit accounts and credit cards. Customers can open accounts, share a deposit account with another owner, receive a primary or supplementary credit card, make purchases, repay a credit-card account, receive monthly statements, and raise a dispute.

We use realistic situations without claiming to reproduce any actual bank's architecture. No employer schemas, customer records, internal documents, or private business rules are included. The definitions are original design choices for this project. All future examples must be synthetic.

The strongest coverage is credit-card servicing. Deposit accounts are included to explain shared account concepts and joint ownership, but deposit payment rails and debit-card processing are outside this release. Calling that boundary out matters: a small model can be useful without pretending to cover every part of a bank.

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

`account_entry` explains a debit or credit visible on a customer's account. It is useful for statements and reconciliation. It does not include balancing journal legs, a chart of accounts, or the bank's general ledger.

For deposit accounts, credits increase funds and debits reduce them. For credit-card accounts, debits increase the amount owed and credits reduce it. Keeping the account kind explicit avoids presenting one sign convention as correct for every balance.

### We keep selected history without inventing an enterprise temporal framework

Account and card status changes are events. Ownership and card assignments have validity intervals. Product terms have versions. These choices support the questions the explorer needs to explain.

Other attributes, including customer segment and merchant category, are current-state values in this release. We do not claim that every attribute can be reconstructed at every historical moment. Event transition matrices and corrections to late-arriving events need more work before a production implementation.

## Two journeys through the graph

**Investigate a disputed purchase.** Start with the person, identify the card they could use at the purchase time, find the posted purchase and merchant, then examine the dispute and its history. The model keeps the financial event and case lifecycle distinct.

**Explain a monthly statement.** Start with an account and statement, inspect its lines and booked entries, then branch into purchases, repayments, and fees. This is a set of related paths, not an instruction to join every table into one giant query. Joining several one-to-many tables without controlling the grain can multiply amounts.

The exact highlighted entities and edges are stored in the model and documented in [JOURNEYS.md](docs/JOURNEYS.md).

## What the interactive release will feel like

The left panel will contain domains and search. The centre will show the graph. Selecting an entity or relationship will open a right-hand inspector with definitions, grain, columns, keys, and business rules.

At a wide zoom, the graph will emphasize domains. At a closer view, it will emphasize tables and key fields. Full column lists belong in the inspector, so the canvas remains readable. Search will find both entity and column names. A table focus mode will show its immediate neighbours, and journey presets will highlight a meaningful subset of the model.

The planned stack is React, TypeScript, Vite, and Cytoscape.js. The first viewer will run entirely in the browser from versioned model metadata. Database access and AI generation are not required to explore the model. See the [explorer specification](docs/EXPLORER_SPEC.md) for interaction and acceptance criteria.

## Run the foundation checks

Use Python 3.10 or newer. No third-party Python packages, database, cloud account, or credentials are required.

From the repository root:

```bash
python3 scripts/validate_model.py
python3 -m unittest discover -s tests -v
python3 scripts/render_docs.py --check
```

After editing `model/banking.model.json`, regenerate the reference documents:

```bash
python3 scripts/render_docs.py
```

The validator checks metadata: identifiers, references, key types, cardinality consistency, rule links, and connected journey subgraphs. The tests deliberately break the model to verify that common errors are rejected.

**These checks do not validate transaction records.** All 21 banking rules are currently marked `specified_not_implemented`. A structurally valid model is not evidence of regulatory compliance, correct balances, or production readiness.

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
| `scripts/` | Metadata validation and documentation generation. |
| `tests/` | Mutation tests for the metadata contract. |
| `.github/workflows/validate.yml` | The same checks for GitHub Actions. |

## What we are leaving out

This release excludes corporate customers, mortgages, installment loans, investments, treasury, a complete general ledger, payment clearing networks, foreign exchange, interest calculation, fraud scoring, regulatory reporting, and a compliance implementation. Authentication and access control are also outside the public metadata viewer.

CAD is the only supported currency. UTC timestamps represent instants; America/Toronto determines business dates. Monetary columns use a logical decimal type. Future JSON sample amounts will be decimal strings rather than binary floating-point numbers.

Descriptions of personal fields are included to explain data classification, but actual personal data must never enter this repository. Classification labels are descriptive metadata, not masking policies or access controls.

## Inspiration and authorship

The [Databricks Lakehouse Industry Data Models project](https://github.com/databricks-industry-solutions/lakehouse-industry-data-models) inspired the idea of browsing a model visually. Its source and banking model have not been copied into this project. This is an independent educational implementation, with no affiliation or endorsement.

The foundation was built for Subhanjan Das with AI assistance. Definitions and trade-offs are explicit so they can be reviewed, questioned, and improved. The goal is a model that can be explained, not a large diagram whose assumptions are hidden.

Original project files are released under the MIT license. Upstream projects retain their own licenses.
