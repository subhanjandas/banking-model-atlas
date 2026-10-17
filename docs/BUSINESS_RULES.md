# Business rules

These are specifications, not implemented data-quality checks. The metadata validator verifies their references only.

## R01 — cross_entity

An account opens within its product version offering interval and keeps that version; later product migration is deferred.

Applies to: `account`, `product_version`, `product`.

## R02 — temporal

Every open account has exactly one active PRIMARY owner. JOINT roles are allowed only for deposits. Credit-card and term-loan accounts have one primary owner. Identical customer/account/role intervals must not overlap.

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

Exactly the source reference corresponding to kind is populated: CARD→card_transaction_id, PAYMENT→payment_id, FEE→fee_type_id, REVERSAL→reverses_entry_id, DEPOSIT_PAYMENT→payment_order_id, LOAN_DRAW→loan_disbursement_id, LOAN_REPAYMENT→loan_repayment_id. ADJUSTMENT has none. All other source references are null.

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

Between daily snapshots, deposits change by credits minus debits; credit-card and term-loan amounts owed change by debits minus credits. A gap requires all intervening entries. Snapshots may be negative; loan principal interest is accounted separately.

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

## R22 — cross_entity

An APPROVED onboarding case has a latest PASS identity check, latest PASS KYC review and latest CLEAR screening for each required type (SANCTIONS and PEP); all occur no later than closure. Ties within a check stream are disallowed.

Applies to: `onboarding_case`, `identity_check`, `kyc_review`, `screening_review`.

## R23 — cross_entity

A booked product application is APPROVED, has an APPROVED case for the same applicant, and references an account opened with the requested product version. TERM_LOAN requests use loan_application instead.

Applies to: `product_application`, `onboarding_case`, `account`, `product_version`.

## R24 — temporal

Risk assessment and linked case refer to the same customer. Next review date is after the assessment business date; no risk score is computed.

Applies to: `customer_risk_assessment`, `onboarding_case`.

## R25 — conditional

An INTERNAL order has a non-null destination account, a null beneficiary and different source/destination accounts. An OUTBOUND order has a beneficiary and no destination account. Both accounts are deposits and currency matches the order; the initiating authority must be checked separately.

Applies to: `payment_order`, `account`, `beneficiary`.

## R26 — reconciliation

Each POSTED or SETTLED internal order has exactly one DEPOSIT_PAYMENT debit on the source and one equal credit on the destination. An outbound order has exactly one source debit. Entries match amount and currency. FAILED or CANCELLED orders have no unreversed posting in this simplified version.

Applies to: `payment_order`, `payment_event`, `account_entry`.

## R27 — reconciliation

Settlement belongs only to an OUTBOUND order. There is one full settlement per order with equal amount and currency. SETTLED requires a settlement observation; internal orders finish at POSTED.

Applies to: `payment_settlement`, `payment_order`, `payment_event`.

## R28 — temporal

A hold uses its order source account, has positive amount, expires after placement and is not released before placement. A standing-order execution matches the template account, payee and amount; duplicate scheduled executions must be prevented by the scheduler.

Applies to: `account_hold`, `payment_order`, `standing_order`.

## R29 — temporal

Within an order, event times are unique. Allowed transitions: RECEIVED→VALIDATED/FAILED/CANCELLED; VALIDATED→POSTED/FAILED/CANCELLED; POSTED→SETTLED for outbound only. Returns after posting are a deferred process, not a FAILED rewrite.

Applies to: `payment_event`.

## R30 — cross_entity

A contract uses a non-expired APPROVED decision for the same application borrower and TERM_LOAN product. Contract principal and term equal the approved amounts. Approval is not automatic disbursement.

Applies to: `loan_application`, `credit_decision`, `loan_contract`, `account`, `account_holder`.

## R31 — aggregate

Installment numbers are unique and positive; principal and interest due are nonnegative. Scheduled principal totals contractual principal. Due dates do not precede acceptance or exceed maturity.

Applies to: `loan_schedule_item`, `loan_contract`.

## R32 — reconciliation

One full disbursement equals contract principal and creates a LOAN_DRAW debit to the loan account and an equal credit to the internal deposit destination. Funding date is not before contract acceptance.

Applies to: `loan_disbursement`, `loan_contract`, `account_entry`.

## R33 — reconciliation

A POSTED repayment has nonnegative principal and interest and a positive total. Its principal portion creates one LOAN_REPAYMENT credit to the loan account when positive, and none when zero. Interest is journaled separately. Total principal repayments cannot exceed disbursed principal.

Applies to: `loan_repayment`, `loan_contract`, `account_entry`.

## R34 — aggregate

Each POSTED journal contains at least two strictly positive lines and equal total debits and credits, in its one declared currency and legal entity. A DRAFT journal may be incomplete.

Applies to: `journal`, `journal_line`.

## R35 — reconciliation

Allocated amounts are positive. For entries included in an ACCOUNT_TO_GL reconciliation, allocations must total the entry amount. Linked line direction and currency match the entry; allocations to one ledger line cannot exceed that line amount. Counterpart lines may be unmapped.

Applies to: `posting_link`, `account_entry`, `journal_line`, `journal`, `account`.

## R36 — conditional

A COMPLETE run has a completion time no earlier than start. MATCHED items have zero difference. ACCOUNT_TO_GL items use account/ledger references; PAYMENT_TO_SETTLEMENT uses payment_order; STATEMENT_TO_ENTRIES uses statement. Exceptions may legitimately have a missing side.

Applies to: `reconciliation_run`, `reconciliation_item`.

## R37 — conditional

Only APPROVED decisions contain positive approved principal and term. DECLINED and REFER have null approved amounts. Decision expiry is not before its decision business date.

Applies to: `credit_decision`.

## R38 — row

Normal balance is DEBIT for ASSET and EXPENSE, CREDIT for LIABILITY, EQUITY and INCOME. Individual lines may be on either side; normal balance is not a prohibition on opposite entries.

Applies to: `gl_account`, `journal_line`.

## R39 — cross_row

Full internal reversals follow POSTED; full outbound returns follow SETTLED. Preserve original entries and append one equal opposite entry per original entry, on the same account and a later or equal business date. Partial and repeated reversals are excluded.

Applies to: `payment_order`, `payment_event`, `account_entry`.

## R40 — cross_row

Complete event histories begin in the declared initial state and follow the explicit transition matrix in lifecycle_transitions.json. Effective timestamps are unique per subject; closed and terminal payment states cannot reopen.

Applies to: `payment_event`, `account_status_event`, `card_status_event`.

## R41 — cross_row

For every chart account, closing debit-positive balance equals opening balance plus posted debits minus credits strictly after the opening date and through the closing date. Both trial balances sum to zero.

Applies to: `gl_account`, `gl_balance_snapshot`, `journal`, `journal_line`.

## R42 — cross_row

Every customer account maps to one control account and every booked entry has complete allocations to that control account. Signed account balances reconcile to control balances at opening and closing. Deposit balances are negated for debit-positive accounting.

Applies to: `account_gl_mapping`, `account_balance_snapshot`, `account_entry`, `posting_link`, `gl_balance_snapshot`.

## R43 — cross_row

An alert is a signal, not a verdict. Case-alert associations must concern the case customer; a confirmed decision does not automatically book a loss or refund.

Applies to: `fraud_rule`, `fraud_alert`, `fraud_case`, `fraud_case_alert`, `fraud_decision`, `fraud_action`.

## R44 — cross_row

Overdue amounts and days past due are nonnegative. Promises have positive amounts and due dates no earlier than their recorded dates; kept promises require independent payment evidence.

Applies to: `delinquency_snapshot`, `collection_case`, `collection_contact`, `promise_to_pay`, `hardship_plan`, `collection_case_event`.

## R45 — cross_row

Earning and redemption amounts are positive integer points. Membership, purchase and account ownership must agree. Closing points equal opening plus earnings and adjustments minus fulfilled redemptions.

Applies to: `reward_program`, `reward_membership`, `reward_earn`, `reward_redemption`, `reward_adjustment`, `reward_balance_snapshot`.

## R46 — cross_row

Request events and complaint resolutions cannot precede intake. Account-specific requests require a valid customer relationship. Documents are references only and contain no credentials.

Applies to: `service_request`, `service_request_event`, `complaint`, `complaint_resolution`, `communication`, `document_reference`.

