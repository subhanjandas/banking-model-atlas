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
| `account` | A customer-facing deposit or credit-card account. | One account contract. |
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

