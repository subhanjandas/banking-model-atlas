# Entity catalogue

Generated from `model/banking.model.json`. Edit the model and regenerate.

## Customers

Who banks with us and how we contact them.

| Entity | Meaning | Grain |
|---|---|---|
| `customer` | A person with a relationship to the fictional bank. | One natural person. |
| `customer_address` | An address held for a customer over a period. | One customer address assignment for one purpose and interval. |
| `customer_contact` | A way to reach a customer. | One contact method for a customer. |
| `customer_consent` | A recorded choice about a specific optional purpose. | One consent decision event for one customer and purpose. |

## Bank and reference data

Shared branch, channel and currency definitions.

| Entity | Meaning | Grain |
|---|---|---|
| `branch` | A servicing location or virtual branch. | One servicing branch. |
| `channel` | A route through which a customer action occurs. | One interaction channel. |
| `currency` | A currency reference used by monetary entities. | One currency. |

## Products

What the bank offers and which version was agreed.

| Entity | Meaning | Grain |
|---|---|---|
| `product` | A named deposit or credit-card offering. | One product family. |
| `product_version` | A dated edition of product terms. | One version of one product. |
| `fee_type` | A category of account fee. | One fee category. |

## Accounts and credit

Ownership, account lifecycle and credit limits.

| Entity | Meaning | Grain |
|---|---|---|
| `account` | A customer-facing deposit, credit-card or term-loan account. | One account contract. |
| `account_holder` | Ownership or signing authority over an account. | One customer role on an account for an interval. |
| `account_status_event` | A lifecycle change for an account. | One account status event. |
| `credit_facility` | The credit agreement attached to a credit-card account. | One facility per credit-card account. |
| `credit_limit_event` | A change in the approved credit limit. | One effective limit change per facility. |

## Cards

Issued cards, their users and their lifecycle.

| Entity | Meaning | Grain |
|---|---|---|
| `card` | An issued credit-card instrument. | One issued card instance, including each replacement. |
| `card_assignment` | The person authorized to use a card. | One card-to-person assignment interval. |
| `card_status_event` | A change in a card lifecycle. | One card status event. |

## Merchants and activity

Authorization, clearing and account entries.

| Entity | Meaning | Grain |
|---|---|---|
| `merchant_category` | A fictional grouping for merchant analytics. | One merchant category. |
| `merchant` | A merchant identity observed in card activity. | One merchant. |
| `card_authorization` | A request to approve card spending before posting. | One authorization request. |
| `card_transaction` | A posted purchase or refund received through the card network. | One posted card purchase or refund. |
| `account_entry` | An immutable customer-account movement used for statement presentation. | One booked debit or credit on an account. |

## Payments and statements

Repayments, billing documents and balance snapshots.

| Entity | Meaning | Grain |
|---|---|---|
| `payment` | An external repayment to a credit-card account. | One received payment instruction. |
| `statement` | An issued monthly billing snapshot for a credit-card account. | One issued statement for an account and cycle. |
| `statement_line` | A printed item on an issued statement. | One account entry displayed on one statement. |
| `account_balance_snapshot` | A supplied end-of-day account balance. | One account and business date. |

## Disputes

Customer claims and the progress of each case.

| Entity | Meaning | Grain |
|---|---|---|
| `dispute_reason` | A project-local category for customer claims. | One dispute reason. |
| `dispute` | A customer claim about a posted purchase. | One dispute case against one purchase. |
| `dispute_event` | A lifecycle event within a dispute case. | One event in a dispute. |

## Onboarding and due diligence

Customer onboarding, identity evidence outcomes and product applications.

| Entity | Meaning | Grain |
|---|---|---|
| `onboarding_case` | A customer onboarding or refresh workflow. | One onboarding case for an existing customer identity. |
| `identity_check` | A recorded identity-verification attempt, without identity documents. | One identity check attempt within an onboarding case. |
| `kyc_review` | A due-diligence review outcome recorded for a case. | One review attempt within an onboarding case. |
| `screening_review` | A screening result and subsequent review outcome. | One screening attempt within an onboarding case. |
| `customer_risk_assessment` | A dated internal customer risk classification. | One assessment event for one customer. |
| `product_application` | A request to open a deposit or credit-card product. | One product application submitted by a customer. |

## Deposit payments

Payment instructions, execution events, settlement and reserved funds.

| Entity | Meaning | Grain |
|---|---|---|
| `beneficiary` | A payee saved by a customer for an external payment. | One customer-owned beneficiary record. |
| `standing_order` | A recurring instruction template for an external payment. | One standing-order arrangement. |
| `payment_order` | An instruction to move funds from a deposit account. | One customer-authorized internal or outbound payment instruction. |
| `payment_event` | A lifecycle event for a deposit payment instruction. | One execution event for an order. |
| `payment_settlement` | An observed external settlement result. | One settlement observation for an outbound order. |
| `account_hold` | A temporary reservation of funds on a deposit account. | One reservation associated with a payment order. |

## Term lending

Applications, decisions, contracts, schedules and principal movements.

| Entity | Meaning | Grain |
|---|---|---|
| `loan_application` | A request for a fixed-term consumer loan. | One application by one primary borrower. |
| `credit_decision` | A recorded lending decision for an application. | One dated decision on an application. |
| `loan_contract` | An accepted fixed-term loan agreement. | One loan contract and its loan account. |
| `loan_schedule_item` | An expected installment in a supplied repayment schedule. | One installment for a loan contract. |
| `loan_disbursement` | A funded principal draw on a loan contract. | One completed principal disbursement. |
| `loan_repayment` | A received external repayment against a loan. | One received repayment with supplied principal/interest split. |

## Accounting and reconciliation

Double-entry journals, account-entry mappings and reconciliation exceptions.

| Entity | Meaning | Grain |
|---|---|---|
| `gl_account` | An account in the fictional bank chart of accounts. | One general-ledger account. |
| `journal` | A set of accounting lines posted together. | One single-currency journal for one legal entity. |
| `journal_line` | One debit or credit within an accounting journal. | One line within one journal. |
| `posting_link` | A reconciliation mapping from customer-account activity to a ledger line. | One allocation of an account entry to a journal line. |
| `reconciliation_run` | A recorded comparison between two financial record sets. | One reconciliation execution for one business date and scope. |
| `reconciliation_item` | A match or exception recorded by a reconciliation run. | One comparison outcome within one run. |
| `gl_balance_snapshot` | One independently supplied ledger account balance at a business-date close. | One independently supplied ledger account balance at a business-date close. |
| `account_gl_mapping` | One customer account mapped to its ledger control account. | One customer account mapped to its ledger control account. |

