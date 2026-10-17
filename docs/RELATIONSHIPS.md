# Relationships

Read each row from the referencing table to the referenced table. Reverse cardinality describes the maximum number of children; conditional minimums live in business rules.

| Relationship | From | To | Referenced rows per source | Source rows per target | Meaning |
|---|---|---|---|---|---|
| `customer_address__customer_id` | `customer_address.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Person to whom this address belongs. |
| `customer_contact__customer_id` | `customer_contact.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Customer reached by this contact. |
| `customer_consent__customer_id` | `customer_consent.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Person who made the choice. |
| `customer_consent__channel_id` | `customer_consent.channel_id` | `channel.channel_id` | exactly_one | zero_or_many | Channel that recorded the choice. |
| `product_version__product_id` | `product_version.product_id` | `product.product_id` | exactly_one | zero_or_many | Product whose terms are versioned. |
| `account__product_version_id` | `account.product_version_id` | `product_version.product_version_id` | exactly_one | zero_or_many | Product terms booked at account opening. |
| `account__branch_id` | `account.branch_id` | `branch.branch_id` | exactly_one | zero_or_many | Branch responsible for servicing. |
| `account__currency_id` | `account.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Account denomination. |
| `account_holder__account_id` | `account_holder.account_id` | `account.account_id` | exactly_one | zero_or_many | Account to which the role applies. |
| `account_holder__customer_id` | `account_holder.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Person assigned the role. |
| `account_status_event__account_id` | `account_status_event.account_id` | `account.account_id` | exactly_one | zero_or_many | Account whose status changed. |
| `credit_facility__account_id` | `credit_facility.account_id` | `account.account_id` | exactly_one | zero_or_one | Credit-card account supported by this facility. |
| `credit_facility__currency_id` | `credit_facility.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Must match the linked account currency. |
| `credit_limit_event__credit_facility_id` | `credit_limit_event.credit_facility_id` | `credit_facility.credit_facility_id` | exactly_one | zero_or_many | Facility whose limit changed. |
| `card__account_id` | `card.account_id` | `account.account_id` | exactly_one | zero_or_many | Credit-card account billed for use. |
| `card__replaces_card_id` | `card.replaces_card_id` | `card.card_id` | zero_or_one | zero_or_many | Earlier card replaced by this card, when applicable. |
| `card_assignment__card_id` | `card_assignment.card_id` | `card.card_id` | exactly_one | zero_or_many | Card being assigned. |
| `card_assignment__customer_id` | `card_assignment.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Person authorized to use it. |
| `card_status_event__card_id` | `card_status_event.card_id` | `card.card_id` | exactly_one | zero_or_many | Card whose status changed. |
| `merchant__merchant_category_id` | `merchant.merchant_category_id` | `merchant_category.merchant_category_id` | exactly_one | zero_or_many | Merchant analytics category. |
| `card_authorization__card_id` | `card_authorization.card_id` | `card.card_id` | exactly_one | zero_or_many | Card presented for authorization. |
| `card_authorization__merchant_id` | `card_authorization.merchant_id` | `merchant.merchant_id` | exactly_one | zero_or_many | Merchant requesting authorization. |
| `card_authorization__currency_id` | `card_authorization.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Requested currency. |
| `card_authorization__channel_id` | `card_authorization.channel_id` | `channel.channel_id` | exactly_one | zero_or_many | Origin of the request. |
| `card_transaction__card_id` | `card_transaction.card_id` | `card.card_id` | exactly_one | zero_or_many | Card used for this activity. |
| `card_transaction__merchant_id` | `card_transaction.merchant_id` | `merchant.merchant_id` | exactly_one | zero_or_many | Merchant involved. |
| `card_transaction__currency_id` | `card_transaction.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Posted currency. |
| `card_transaction__authorization_id` | `card_transaction.authorization_id` | `card_authorization.card_authorization_id` | zero_or_one | zero_or_many | Related authorization when available; may be absent for offline clearing. |
| `card_transaction__original_transaction_id` | `card_transaction.original_transaction_id` | `card_transaction.card_transaction_id` | zero_or_one | zero_or_many | Purchase refunded by this refund. |
| `account_entry__account_id` | `account_entry.account_id` | `account.account_id` | exactly_one | zero_or_many | Account affected. |
| `account_entry__card_transaction_id` | `account_entry.card_transaction_id` | `card_transaction.card_transaction_id` | zero_or_one | zero_or_many | Card activity behind this entry, if any. |
| `account_entry__payment_id` | `account_entry.payment_id` | `payment.payment_id` | zero_or_one | zero_or_many | Repayment behind this entry, if any. |
| `account_entry__fee_type_id` | `account_entry.fee_type_id` | `fee_type.fee_type_id` | zero_or_one | zero_or_many | Fee category when this is a fee. |
| `account_entry__reverses_entry_id` | `account_entry.reverses_entry_id` | `account_entry.account_entry_id` | zero_or_one | zero_or_many | Earlier entry reversed by this entry. |
| `payment__account_id` | `payment.account_id` | `account.account_id` | exactly_one | zero_or_many | Credit-card account receiving the repayment. |
| `payment__channel_id` | `payment.channel_id` | `channel.channel_id` | exactly_one | zero_or_many | How the instruction arrived. |
| `payment__currency_id` | `payment.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Payment currency; must match the account. |
| `statement__account_id` | `statement.account_id` | `account.account_id` | exactly_one | zero_or_many | Credit-card account being billed. |
| `statement_line__statement_id` | `statement_line.statement_id` | `statement.statement_id` | exactly_one | zero_or_many | Statement containing this line. |
| `statement_line__account_entry_id` | `statement_line.account_entry_id` | `account_entry.account_entry_id` | exactly_one | zero_or_one | Booked entry being displayed. |
| `account_balance_snapshot__account_id` | `account_balance_snapshot.account_id` | `account.account_id` | exactly_one | zero_or_many | Account summarized. |
| `dispute__card_transaction_id` | `dispute.card_transaction_id` | `card_transaction.card_transaction_id` | exactly_one | zero_or_many | Purchase being challenged. |
| `dispute__raised_by_customer_id` | `dispute.raised_by_customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Customer raising the case. |
| `dispute__dispute_reason_id` | `dispute.dispute_reason_id` | `dispute_reason.dispute_reason_id` | exactly_one | zero_or_many | Reason for the claim. |
| `dispute_event__dispute_id` | `dispute_event.dispute_id` | `dispute.dispute_id` | exactly_one | zero_or_many | Case being progressed. |
| `onboarding_case__customer_id` | `onboarding_case.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Person whose relationship is being reviewed. |
| `identity_check__onboarding_case_id` | `identity_check.onboarding_case_id` | `onboarding_case.onboarding_case_id` | exactly_one | zero_or_many | Case requiring this check. |
| `kyc_review__onboarding_case_id` | `kyc_review.onboarding_case_id` | `onboarding_case.onboarding_case_id` | exactly_one | zero_or_many | Case being reviewed. |
| `screening_review__onboarding_case_id` | `screening_review.onboarding_case_id` | `onboarding_case.onboarding_case_id` | exactly_one | zero_or_many | Case associated with the screening. |
| `customer_risk_assessment__customer_id` | `customer_risk_assessment.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Customer being assessed. |
| `customer_risk_assessment__onboarding_case_id` | `customer_risk_assessment.onboarding_case_id` | `onboarding_case.onboarding_case_id` | zero_or_one | zero_or_many | Related onboarding or refresh case, if applicable. |
| `product_application__customer_id` | `product_application.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Applicant. |
| `product_application__product_version_id` | `product_application.product_version_id` | `product_version.product_version_id` | exactly_one | zero_or_many | Requested offering. |
| `product_application__onboarding_case_id` | `product_application.onboarding_case_id` | `onboarding_case.onboarding_case_id` | exactly_one | zero_or_many | Onboarding case supporting the application. |
| `product_application__booked_account_id` | `product_application.booked_account_id` | `account.account_id` | zero_or_one | zero_or_one | Account opened after approval, if booked. |
| `beneficiary__customer_id` | `beneficiary.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Customer who saved the payee. |
| `standing_order__source_account_id` | `standing_order.source_account_id` | `account.account_id` | exactly_one | zero_or_many | Deposit account to debit. |
| `standing_order__beneficiary_id` | `standing_order.beneficiary_id` | `beneficiary.beneficiary_id` | exactly_one | zero_or_many | Saved external destination. |
| `payment_order__source_account_id` | `payment_order.source_account_id` | `account.account_id` | exactly_one | zero_or_many | Deposit account funding the instruction. |
| `payment_order__destination_account_id` | `payment_order.destination_account_id` | `account.account_id` | zero_or_one | zero_or_many | Internal deposit destination; absent for external instructions. |
| `payment_order__beneficiary_id` | `payment_order.beneficiary_id` | `beneficiary.beneficiary_id` | zero_or_one | zero_or_many | External payee; absent for internal instructions. |
| `payment_order__standing_order_id` | `payment_order.standing_order_id` | `standing_order.standing_order_id` | zero_or_one | zero_or_many | Recurring template that produced the order, if any. |
| `payment_order__channel_id` | `payment_order.channel_id` | `channel.channel_id` | exactly_one | zero_or_many | Channel accepting the instruction. |
| `payment_order__currency_id` | `payment_order.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Instruction currency. |
| `payment_event__payment_order_id` | `payment_event.payment_order_id` | `payment_order.payment_order_id` | exactly_one | zero_or_many | Instruction being progressed. |
| `payment_settlement__payment_order_id` | `payment_settlement.payment_order_id` | `payment_order.payment_order_id` | exactly_one | zero_or_one | Outbound order being settled. |
| `payment_settlement__currency_id` | `payment_settlement.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Settlement currency. |
| `account_hold__account_id` | `account_hold.account_id` | `account.account_id` | exactly_one | zero_or_many | Deposit account with reserved funds. |
| `account_hold__payment_order_id` | `account_hold.payment_order_id` | `payment_order.payment_order_id` | exactly_one | zero_or_many | Order causing the reservation. |
| `loan_application__customer_id` | `loan_application.customer_id` | `customer.customer_id` | exactly_one | zero_or_many | Applicant and proposed borrower. |
| `loan_application__product_version_id` | `loan_application.product_version_id` | `product_version.product_version_id` | exactly_one | zero_or_many | Requested TERM_LOAN product. |
| `loan_application__onboarding_case_id` | `loan_application.onboarding_case_id` | `onboarding_case.onboarding_case_id` | exactly_one | zero_or_many | Supporting onboarding case. |
| `credit_decision__loan_application_id` | `credit_decision.loan_application_id` | `loan_application.loan_application_id` | exactly_one | zero_or_many | Application considered. |
| `loan_contract__account_id` | `loan_contract.account_id` | `account.account_id` | exactly_one | zero_or_one | TERM_LOAN account representing the principal obligation. |
| `loan_contract__credit_decision_id` | `loan_contract.credit_decision_id` | `credit_decision.credit_decision_id` | exactly_one | zero_or_one | Approved decision accepted by the borrower. |
| `loan_schedule_item__loan_contract_id` | `loan_schedule_item.loan_contract_id` | `loan_contract.loan_contract_id` | exactly_one | zero_or_many | Contract being scheduled. |
| `loan_disbursement__loan_contract_id` | `loan_disbursement.loan_contract_id` | `loan_contract.loan_contract_id` | exactly_one | zero_or_one | Contract providing the funds. |
| `loan_disbursement__destination_account_id` | `loan_disbursement.destination_account_id` | `account.account_id` | exactly_one | zero_or_many | Internal deposit account receiving proceeds. |
| `loan_repayment__loan_contract_id` | `loan_repayment.loan_contract_id` | `loan_contract.loan_contract_id` | exactly_one | zero_or_many | Loan being repaid. |
| `journal__currency_id` | `journal.currency_id` | `currency.currency_id` | exactly_one | zero_or_many | Common currency of all lines. |
| `journal_line__journal_id` | `journal_line.journal_id` | `journal.journal_id` | exactly_one | zero_or_many | Journal containing the line. |
| `journal_line__gl_account_id` | `journal_line.gl_account_id` | `gl_account.gl_account_id` | exactly_one | zero_or_many | Ledger account affected. |
| `posting_link__account_entry_id` | `posting_link.account_entry_id` | `account_entry.account_entry_id` | exactly_one | zero_or_many | Customer-account entry being mapped. |
| `posting_link__journal_line_id` | `posting_link.journal_line_id` | `journal_line.journal_line_id` | exactly_one | zero_or_many | Related ledger line. |
| `reconciliation_item__reconciliation_run_id` | `reconciliation_item.reconciliation_run_id` | `reconciliation_run.reconciliation_run_id` | exactly_one | zero_or_many | Run that produced the outcome. |
| `reconciliation_item__account_entry_id` | `reconciliation_item.account_entry_id` | `account_entry.account_entry_id` | zero_or_one | zero_or_many | Entry involved when comparing account and ledger records. |
| `reconciliation_item__journal_line_id` | `reconciliation_item.journal_line_id` | `journal_line.journal_line_id` | zero_or_one | zero_or_many | Ledger line involved when available. |
| `reconciliation_item__payment_order_id` | `reconciliation_item.payment_order_id` | `payment_order.payment_order_id` | zero_or_one | zero_or_many | Order involved when comparing payments and settlement. |
| `reconciliation_item__statement_id` | `reconciliation_item.statement_id` | `statement.statement_id` | zero_or_one | zero_or_many | Statement involved when comparing billing totals. |
| `account_entry__payment_order_id` | `account_entry.payment_order_id` | `payment_order.payment_order_id` | zero_or_one | zero_or_many | Deposit payment instruction behind this entry, if any. |
| `account_entry__loan_disbursement_id` | `account_entry.loan_disbursement_id` | `loan_disbursement.loan_disbursement_id` | zero_or_one | zero_or_many | Loan draw behind this principal or deposit entry, if any. |
| `account_entry__loan_repayment_id` | `account_entry.loan_repayment_id` | `loan_repayment.loan_repayment_id` | zero_or_one | zero_or_many | Loan repayment behind a principal reduction, if any. |
| `gl_balance_snapshot__gl_account_id` | `gl_balance_snapshot.gl_account_id` | `gl_account.gl_account_id` | exactly_one | zero_or_many | Connect the reconciliation record to its represented account. |
| `account_gl_mapping__account_id` | `account_gl_mapping.account_id` | `account.account_id` | exactly_one | zero_or_one | Connect the reconciliation record to its represented account. |
| `account_gl_mapping__gl_account_id` | `account_gl_mapping.gl_account_id` | `gl_account.gl_account_id` | exactly_one | zero_or_many | Connect the reconciliation record to its represented account. |
