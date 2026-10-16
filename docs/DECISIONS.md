# Design decisions

These are initial project decisions, open to review. They are not statements of universal banking practice.

| Decision | Why we chose it | Cost or limitation |
|---|---|---|
| One fictional Canadian retail bank | Makes terminology and rules consistent. | Does not represent every bank or jurisdiction. |
| 30 entities across eight domains | Enough breadth for useful graph navigation and two complete stories. | More modeling review than the original five-table idea. |
| Credit-card servicing is the deepest slice | Supports meaningful statements, refunds, repayments and disputes. | Deposit operations have limited coverage. |
| Original model and viewer implementation | Gives the portfolio clear authorship and avoids depending on upstream restricted materials. | We must implement and test the interactions ourselves. |
| JSON is the source of truth | Powers the graph, inspector, references and future exports consistently. | Manual semantic review is still needed. |
| Accounts separate from cards | Handles replacements and supplementary users. | Requires more joins than a single customer/card table. |
| Ownership separate from card assignment | Avoids treating every card user as an owner. | Role eligibility and interval checks are cross-entity rules. |
| Product version fixed at account opening | Preserves the originally booked offering. | Product migrations require a later contract-history extension. |
| Positive amounts plus explicit kind/direction | Makes purchases, refunds, debits and credits unambiguous. | Analytics must apply the documented sign convention. |
| No complete general ledger | Keeps the reference model within an explainable scope. | No double-entry or financial-reporting completeness claim. |
| External repayments only | Avoids half-modeling internal transfers. | Cannot trace repayment funding to a modeled deposit account. |
| Immutable issued statements | Supports stable historical explanations. | Reissues and corrections need future versioning. |
| Selected temporal history | Supports ownership and lifecycle questions. | Current-state descriptive attributes are not fully historical. |
| CAD only and explicit time semantics | Removes hidden FX and date-boundary ambiguity. | Multi-currency and cross-zone operations need extension. |
| Static browser-based viewer planned | Public metadata can be explored without credentials or a database. | No transactional editing, access controls or shared user state. |
| No AI generation in initial viewer | Keeps the model reviewable and the demonstration reproducible. | Natural-language model creation remains a separate project. |

## Questions deliberately left for later

- How should reopened accounts, corrected events and backdated ownership be represented?
- What is the complete lifecycle transition matrix for each event stream?
- How should statement reissues preserve the original document and corrections?
- How do provisional credits and chargeback recoveries link to account entries?
- How should an account migrate to new product terms without losing history?
- What entity and relationship detail level is most readable at different zoom levels?

The first five questions limit production use. They do not prevent a clearly labeled educational explorer from showing the current model.
