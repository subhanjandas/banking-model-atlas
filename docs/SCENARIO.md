# Expanded executable scenario

The current model includes onboarding, deposit payments, term loans and selected journals. See [SQL_AND_DEMO.md](SQL_AND_DEMO.md) for the current 137-record scenario, account balances and explicit boundaries.

The original card-only worked example below documents the foundation release; its exclusions and amounts are historical, not the current coverage contract.

# Scenario: Maple Harbour Bank

Maple Harbour is a fictional Canadian retail bank. Its deposit products support individual and joint ownership. Its credit-card products have one primary account owner and can issue supplementary cards to other customers. All amounts are CAD. Only natural persons are modeled.

## Worked story

Alex owns a credit-card account. Sam has a supplementary card on that account but is not an owner. On September 10, Sam makes a $120 purchase at a fictional store. The bank records an approved authorization; a $120 purchase posts on September 11. An account entry records a $120 debit.

The merchant later refunds $20. That is a separate posted transaction referencing the original purchase and a separate $20 credit entry. Alex makes an external $50 repayment, which becomes a $50 credit entry when the payment reaches POSTED. Starting from zero, the account now owes $50: 120 - 20 - 50.

The September statement covers [September 1, October 1). It includes all three entries. Suppose Sam also raises a claim about the purchase. The dispute does not change the $50 balance by itself. Its outcome is tracked separately; a later financial adjustment would need an explicit entry.

This story is explanatory, not a sample dataset that the current scripts execute. It will become an independent reconciliation fixture in a later checkpoint.

## Operational assumptions

- Deposit accounts may have joint holders; credit-card accounts have one primary owner.
- Cards in this release are credit cards only. Every replacement gets a new synthetic ID.
- Each card has at most one assigned user at a time. Historical assignments use half-open intervals.
- Repayments originate outside the modeled bank. There is no implicit debit to a deposit account.
- Monthly issued statements apply only to credit-card accounts. There is one issued version per cycle.
- Status-event times are unique within their stream. This avoids ambiguous latest-event selection.
- Account status and card status are separate. Closing a card does not mean its account closes.
- Daily balance snapshots are supplied observations. Rebuilding a balance requires an opening position.
- Merchant and dispute codes are project-local, not complete industry reference sets.

## Boundaries to remember

A diagram can show a relationship without implementing the process behind it. The credit facility records that a credit agreement exists; it does not underwrite an applicant. Consent records a choice; it does not implement a privacy program. A dispute records a case; it does not speak a card network's chargeback protocol.

This is a deliberately simplified but internally explained scenario. Before adapting it to a real organization, the business rules, source systems, data retention, accounting semantics, security, and legal requirements would all need independent review.
