# Business rules

These are specifications, not implemented data-quality checks. The metadata validator verifies their references only.

## R01 — cross_entity

An account opens within its product version offering interval and keeps that version; later product migration is deferred.

Applies to: `account`, `product_version`, `product`.

## R02 — temporal

Every open account has exactly one active PRIMARY owner. JOINT roles are allowed only for deposit products; identical customer/account/role intervals must not overlap.

Applies to: `account_holder`, `account`, `product`.

## R03 — temporal

All validity intervals are [valid_from, valid_to); a non-null end is after the start. Address intervals for one customer/purpose do not overlap; card assignments for one card do not overlap.

Applies to: `customer_address`, `account_holder`, `card_assignment`.

## R04 — cross_entity

Each credit-card account has exactly one facility and an initial nonnegative limit event; deposits have none. Facility currency equals account currency.

Applies to: `credit_facility`, `account`, `product`, `credit_limit_event`.

## R05 — cross_entity

Cards belong only to credit-card accounts. Issue precedes expiry. Assignments begin no earlier than issue; PRIMARY card users must be active primary account owners at assignment start.

Applies to: `card`, `card_assignment`, `account`.

## R06 — graph

A replacement references an older card on the same account; no self-reference or replacement cycle is allowed.

Applies to: `card`.

## R07 — cross_entity

Card activity occurs after issue. Linked authorizations must be approved and use the same card, merchant and currency; multiple presentments are allowed. Refunds have no authorization link in this release.

Applies to: `card_transaction`, `card_authorization`, `card`, `merchant`.

## R08 — aggregate

A REFUND references a PURCHASE on the same card, merchant and currency. A PURCHASE has no original reference. Refund posting does not precede purchase posting; cumulative refunds do not exceed purchase amount.

Applies to: `card_transaction`.

## R09 — row

All transaction, requested, payment, entry and claimed amounts are strictly positive. Money is represented as decimal strings in future JSON records, never binary floating-point values.

Applies to: `card_transaction`, `card_authorization`, `payment`, `account_entry`, `dispute`.

## R10 — conditional

CARD entries have only card_transaction_id populated among source references; PAYMENT has only payment_id; FEE has only fee_type_id; ADJUSTMENT has none; REVERSAL has only reverses_entry_id. Non-reversals have no reversal reference.

Applies to: `account_entry`, `card_transaction`, `payment`, `fee_type`.

## R11 — cross_entity

Each card transaction has exactly one original CARD entry for its card account and equal amount; PURCHASE is DEBIT and REFUND is CREDIT. Each POSTED payment has exactly one original PAYMENT CREDIT entry of equal amount for its receiving account. PENDING or FAILED payments have none.

Applies to: `account_entry`, `card_transaction`, `payment`, `card`, `account`.

## R12 — cross_entity

A reversal points to one non-reversal entry on the same account, has equal amount and opposite direction, and posts no earlier. Each original entry may be reversed at most once; partial reversals are deferred.

Applies to: `account_entry`.

## R13 — reconciliation

Statement lines refer to entries on the statement account within its half-open period. For credit-card statements, closing_balance = opening_balance + debits - credits. Cycles on one account do not overlap; each eligible entry appears exactly once in its issued cycle.

Applies to: `statement`, `statement_line`, `account_entry`.

## R14 — row

Statements exist only for credit-card accounts. Period start precedes end; issue is on or after period end; due date is after issue; minimum due is nonnegative and no greater than max(closing_balance,0).

Applies to: `statement`, `account`, `product`.

## R15 — reconciliation

Between consecutive daily snapshots, deposit balance changes by credits minus debits; credit-card amount owed changes by debits minus credits. A gap requires all intervening entries. Snapshots may be negative.

Applies to: `account_balance_snapshot`, `account_entry`, `account`, `product`.

## R16 — cross_entity

A dispute references a PURCHASE; claim does not exceed its amount. Claimant is an account owner or assigned card user at purchase occurrence. Multiple cases may exist, but only one active case per purchase is allowed.

Applies to: `dispute`, `card_transaction`, `card_assignment`, `account_holder`, `card`.

## R17 — temporal

Effective times are unique within each owner stream (consent also by purpose). Initial states are OPEN for accounts, ISSUED for cards and OPEN for disputes; latest event defines current state. Full allowed-transition matrices are deferred.

Applies to: `account_status_event`, `card_status_event`, `dispute_event`, `credit_limit_event`, `customer_consent`.

## R18 — cross_entity

All currencies are CAD; payment and card activity currency must equal the associated account currency. Payment destination is a credit-card account.

Applies to: `payment`, `card_transaction`, `card_authorization`, `account`, `currency`.

## R19 — aggregate

At most one preferred contact exists per customer and contact type.

Applies to: `customer_contact`.

## R20 — temporal

Closure date is on or after opening and agrees with the CLOSED event business date. Reopening is deferred. UTC instants map to business dates using America/Toronto.

Applies to: `account`, `account_status_event`.

## R21 — temporal

Consent decisions are immutable events. Current consent is the latest decision for the customer and purpose; absence means no recorded grant.

Applies to: `customer_consent`.

