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
