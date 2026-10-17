# Business journeys

These presets drive the interactive explorer. Each journey selects only its listed entities and relationships.

## Investigate a disputed purchase

Who used the card, what posted, and what happened to the complaint?

1. **customer** — Find the customer raising the complaint.
2. **card_assignment** — Identify their card assignment at the purchase time.
3. **card** — Keep the original card even if it has since been replaced.
4. **card_transaction** — Find the posted purchase rather than an authorization hold.
5. **merchant** — Identify the merchant involved.
6. **dispute** — Read the amount and reason for the claim.
7. **dispute_event** — Follow the case history.

The highlighted graph explains joins; it does not prove a claim or automatically credit an account.

Highlighted relationships: `card_assignment__customer_id`, `card_assignment__card_id`, `card_transaction__card_id`, `card_transaction__merchant_id`, `dispute__card_transaction_id`, `dispute_event__dispute_id`.

## Explain a monthly statement

How did purchases, repayments and fees affect the amount owed?

1. **account** — Select the credit-card account.
2. **statement** — Read the billing period and opening balance.
3. **statement_line** — Find the items included in the issued document.
4. **account_entry** — Use booked debits and credits to reconcile the closing balance.
5. **card_transaction** — Trace card entries to purchases or refunds.
6. **payment** — Trace repayment entries to posted payments.
7. **fee_type** — Explain any fee categories.

This is a branching explanation, not a single SQL join path. Aggregate entries before joining optional source tables; the statement is not an interest calculator.

Highlighted relationships: `statement__account_id`, `statement_line__statement_id`, `statement_line__account_entry_id`, `account_entry__card_transaction_id`, `account_entry__payment_id`, `account_entry__fee_type_id`.

## Onboard a customer

What evidence and decisions precede opening an account?

1. **customer** — Start with the person, not an approved account.
2. **onboarding_case** — Open a case for initial onboarding or refresh.
3. **identity_check** — Record identity-check attempts without document contents.
4. **kyc_review** — Inspect the due-diligence review outcome.
5. **screening_review** — Separate screening results from review decisions.
6. **product_application** — Follow the requested product to its booking.
7. **account** — Inspect the resulting account.

These are illustrative workflow records, not an automated compliance system.

Highlighted relationships: `onboarding_case__customer_id`, `identity_check__onboarding_case_id`, `kyc_review__onboarding_case_id`, `screening_review__onboarding_case_id`, `product_application__onboarding_case_id`, `product_application__booked_account_id`.

## Trace a deposit payment

How does an instruction become a posting and an external settlement?

1. **account** — Identify the source deposit account.
2. **payment_order** — Inspect the amount and destination type.
3. **beneficiary** — For outbound orders, identify the saved external payee.
4. **payment_event** — Read the execution history.
5. **payment_settlement** — Compare outbound instructions with settlement.
6. **account_entry** — Find the customer-account movement.

Internal transfers have two customer entries and no external settlement. The diagram is a branching view, not one row per joined result.

Highlighted relationships: `payment_order__source_account_id`, `payment_order__beneficiary_id`, `payment_event__payment_order_id`, `payment_settlement__payment_order_id`, `account_entry__payment_order_id`.

## Fund a term loan

What separates a request, approval, contract and funded balance?

1. **customer** — Identify the borrower.
2. **loan_application** — Read the requested amount and term.
3. **credit_decision** — Find the supplied credit decision.
4. **loan_contract** — Inspect the accepted terms.
5. **loan_disbursement** — Trace the funded amount.
6. **account** — Identify the internal deposit destination.
7. **loan_schedule_item** — Inspect the supplied installment schedule.

This models supplied decisions and schedules. It does not underwrite borrowers or calculate interest.

Highlighted relationships: `loan_application__customer_id`, `credit_decision__loan_application_id`, `loan_contract__credit_decision_id`, `loan_disbursement__loan_contract_id`, `loan_disbursement__destination_account_id`, `loan_schedule_item__loan_contract_id`.

## Reconcile to the ledger

Can customer-account activity be traced to balanced accounting?

1. **account_entry** — Start with a booked customer-account entry.
2. **posting_link** — Inspect its allocated accounting mappings.
3. **journal_line** — Read the ledger debit or credit.
4. **gl_account** — Identify the ledger classification.
5. **journal** — Check the whole journal balances, not just one line.
6. **reconciliation_item** — Review recorded matches or exceptions.
7. **reconciliation_run** — Inspect the comparison scope and completion status.

A balanced journal can still be economically wrong. Reconciliation and source completeness remain separate checks.

Highlighted relationships: `posting_link__account_entry_id`, `posting_link__journal_line_id`, `journal_line__gl_account_id`, `journal_line__journal_id`, `reconciliation_item__account_entry_id`, `reconciliation_item__reconciliation_run_id`.

## Review a fraud alert

How does a signal become an investigated decision?

1. **card_transaction** — Identify the posted activity.
2. **fraud_alert** — Read the signal and its reason.
3. **fraud_case_alert** — Locate the investigation association.
4. **fraud_case** — Review the customer case.
5. **fraud_decision** — Read the recorded conclusion.
6. **fraud_action** — Inspect the requested response.

Synthetic records and selected checks are included. Full workflow automation and domain-specific policy are not implemented.

Highlighted relationships: `fraud_alert__card_transaction_id`, `fraud_case_alert__fraud_alert_id`, `fraud_case_alert__fraud_case_id`, `fraud_decision__fraud_case_id`, `fraud_action__fraud_decision_id`.

## Support an overdue account

How are arrears, outreach and support kept distinct?

1. **delinquency_snapshot** — Inspect the supplied overdue position.
2. **account** — Identify the financial relationship.
3. **collection_case** — Find the follow-up case.
4. **collection_contact** — Review outreach attempts.
5. **promise_to_pay** — Read the commitment, not a payment.
6. **hardship_plan** — Inspect any agreed support terms.

Synthetic records and selected checks are included. Full workflow automation and domain-specific policy are not implemented.

Highlighted relationships: `delinquency_snapshot__account_id`, `collection_case__account_id`, `collection_contact__collection_case_id`, `promise_to_pay__collection_case_id`, `hardship_plan__collection_case_id`.

## Trace reward points

How do purchases, redemptions and adjustments affect points?

1. **card_transaction** — Find the original purchase.
2. **reward_earn** — Inspect the recorded award.
3. **reward_membership** — Identify the account membership.
4. **reward_redemption** — Review requested or fulfilled benefits.
5. **reward_adjustment** — Review explicit corrections.
6. **reward_balance_snapshot** — Compare the supplied closing position.

Synthetic records and selected checks are included. Full workflow automation and domain-specific policy are not implemented.

Highlighted relationships: `reward_earn__card_transaction_id`, `reward_earn__reward_membership_id`, `reward_redemption__reward_membership_id`, `reward_adjustment__reward_membership_id`, `reward_balance_snapshot__reward_membership_id`.

## Resolve a complaint

How is a customer concern recorded and answered?

1. **customer** — Identify who raised the concern.
2. **service_request** — Read the intake context.
3. **complaint** — Separate dissatisfaction from routine assistance.
4. **complaint_resolution** — Read the recorded outcome.
5. **communication** — Inspect response delivery.
6. **document_reference** — Find references to supporting evidence.

Synthetic records and selected checks are included. Full workflow automation and domain-specific policy are not implemented.

Highlighted relationships: `service_request__customer_id`, `complaint__service_request_id`, `complaint_resolution__complaint_id`, `communication__service_request_id`, `document_reference__service_request_id`.

