# Data dictionary

Logical types are intentionally engine-neutral. Dates are calendar dates; timestamps are UTC instants.

## customer

A person with a relationship to the fictional bank.

**Grain:** One natural person.

**Primary key:** customer_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `customer_id` | `string` | false | identifier | Stable synthetic identifier for customer. |
| `display_name` | `string` | false | personal | Invented display name; never an actual customer name. |
| `customer_since` | `date` | false | internal | Date this customer relationship began. |
| `segment` | `string` | false | internal | Simple service grouping. Allowed: STANDARD, PREMIUM. |
| `status` | `string` | false | internal | Current customer relationship status. Allowed: ACTIVE, CLOSED. |

**Unique keys:** Primary key only.

**Notes:** Organizations and beneficial ownership are outside this version.

**Rules:** 

## customer_address

An address held for a customer over a period.

**Grain:** One customer address assignment for one purpose and interval.

**Primary key:** customer_address_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `customer_address_id` | `string` | false | identifier | Stable synthetic identifier for customer address. |
| `customer_id` | `string` | false | identifier | Person to whom this address belongs. |
| `purpose` | `string` | false | internal | Reason this address is held. Allowed: HOME, MAILING. |
| `address_text` | `string` | false | personal | Invented street and locality. |
| `province_code` | `string` | false | internal | Province or territory abbreviation. |
| `valid_from` | `date` | false | internal | First valid day, inclusive. |
| `valid_to` | `date` | true | internal | First invalid day, exclusive; null means open-ended. |

**Unique keys:** Primary key only.

**Notes:** Overlapping addresses of the same purpose are disallowed in this fictional scenario.

**Rules:** R03

## customer_contact

A way to reach a customer.

**Grain:** One contact method for a customer.

**Primary key:** customer_contact_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `customer_contact_id` | `string` | false | identifier | Stable synthetic identifier for customer contact. |
| `customer_id` | `string` | false | identifier | Customer reached by this contact. |
| `contact_type` | `string` | false | internal | Contact medium. Allowed: EMAIL, PHONE. |
| `contact_value` | `string` | false | personal | Fictional contact value; example emails use example.com. |
| `is_preferred` | `boolean` | false | internal | Whether this is preferred within its contact type. |

**Unique keys:** Primary key only.

**Notes:** Contact history and verification evidence are deferred.

**Rules:** R19

## customer_consent

A recorded choice about a specific optional purpose.

**Grain:** One consent decision event for one customer and purpose.

**Primary key:** customer_consent_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `customer_consent_id` | `string` | false | identifier | Stable synthetic identifier for customer consent. |
| `customer_id` | `string` | false | identifier | Person who made the choice. |
| `purpose` | `string` | false | internal | Optional use covered by the choice. Allowed: EMAIL_MARKETING, SMS_MARKETING. |
| `decision` | `string` | false | internal | Choice recorded. Allowed: GRANTED, WITHDRAWN. |
| `decided_at` | `timestamp` | false | internal | UTC time of the decision. |
| `channel_id` | `string` | false | identifier | Channel that recorded the choice. |

**Unique keys:** Primary key only.

**Notes:** Latest event per customer and purpose defines the current choice. This is not a legal compliance implementation.

**Rules:** R17, R21

## branch

A servicing location or virtual branch.

**Grain:** One servicing branch.

**Primary key:** branch_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `branch_id` | `string` | false | identifier | Stable synthetic identifier for branch. |
| `branch_code` | `string` | false | internal | Unique fictional branch code. |
| `name` | `string` | false | internal | Display name. |
| `province_code` | `string` | false | internal | Servicing province or territory. |

**Unique keys:** branch_code

**Notes:** Virtual branch allows digital accounts without forcing a physical visit.

**Rules:** 

## channel

A route through which a customer action occurs.

**Grain:** One interaction channel.

**Primary key:** channel_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `channel_id` | `string` | false | identifier | Stable synthetic identifier for channel. |
| `code` | `string` | false | internal | Stable channel code. Allowed: APP, WEB, BRANCH, PHONE, NETWORK. |
| `name` | `string` | false | internal | Human-readable channel name. |

**Unique keys:** code

**Notes:** Channel describes origin, not a person or device.

**Rules:** 

## currency

A currency reference used by monetary entities.

**Grain:** One currency.

**Primary key:** currency_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `currency_id` | `string` | false | identifier | Stable synthetic identifier for currency. |
| `code` | `string` | false | internal | Currency code; CAD is the only supported value. Allowed: CAD. |
| `minor_unit_digits` | `integer` | false | internal | Number of fractional digits; 2 for CAD. |

**Unique keys:** code

**Notes:** Foreign exchange and cross-currency settlement are excluded.

**Rules:** R18

## product

A named deposit or credit-card offering.

**Grain:** One product family.

**Primary key:** product_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `product_id` | `string` | false | identifier | Stable synthetic identifier for product. |
| `name` | `string` | false | internal | Fictional marketing name. |
| `kind` | `string` | false | internal | Account family supported by this product. Allowed: DEPOSIT, CREDIT_CARD. |

**Unique keys:** Primary key only.

**Notes:** An account refers to a version, not directly to a mutable marketing description.

**Rules:** R01, R02, R04, R14, R15

## product_version

A dated edition of product terms.

**Grain:** One version of one product.

**Primary key:** product_version_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `product_version_id` | `string` | false | identifier | Stable synthetic identifier for product version. |
| `product_id` | `string` | false | identifier | Product whose terms are versioned. |
| `version_number` | `integer` | false | internal | Increasing number within the product. |
| `effective_from` | `date` | false | internal | First day offered, inclusive. |
| `effective_to` | `date` | true | internal | First day no longer offered, exclusive. |
| `terms_summary` | `string` | false | internal | Plain-language description; not a contract. |

**Unique keys:** product_id, version_number

**Notes:** Existing accounts retain their booked version after the offering closes. APR calculations are out of scope.

**Rules:** R01

## fee_type

A category of account fee.

**Grain:** One fee category.

**Primary key:** fee_type_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `fee_type_id` | `string` | false | identifier | Stable synthetic identifier for fee type. |
| `code` | `string` | false | internal | Stable fee category. Allowed: ANNUAL, LATE, SERVICE. |
| `description` | `string` | false | internal | What the category means. |

**Unique keys:** code

**Notes:** No fee engine or fee schedule is implemented.

**Rules:** R10

## account

A customer-facing deposit or credit-card account.

**Grain:** One account contract.

**Primary key:** account_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_id` | `string` | false | identifier | Stable synthetic identifier for account. |
| `product_version_id` | `string` | false | identifier | Product terms booked at account opening. |
| `branch_id` | `string` | false | identifier | Branch responsible for servicing. |
| `currency_id` | `string` | false | identifier | Account denomination. |
| `opened_on` | `date` | false | internal | First day of the account. |
| `closed_on` | `date` | true | internal | Closure date, if closed. |

**Unique keys:** Primary key only.

**Notes:** Kind is derived through product_version and product. Account numbers are not stored.

**Rules:** R01, R02, R04, R05, R11, R14, R15, R18, R20

## account_holder

Ownership or signing authority over an account.

**Grain:** One customer role on an account for an interval.

**Primary key:** account_holder_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_holder_id` | `string` | false | identifier | Stable synthetic identifier for account holder. |
| `account_id` | `string` | false | identifier | Account to which the role applies. |
| `customer_id` | `string` | false | identifier | Person assigned the role. |
| `role` | `string` | false | internal | Legal or operational role in this fictional scenario. Allowed: PRIMARY, JOINT. |
| `valid_from` | `date` | false | internal | First valid day, inclusive. |
| `valid_to` | `date` | true | internal | First invalid day, exclusive. |

**Unique keys:** Primary key only.

**Notes:** Deposits can have joint owners. Credit-card accounts have one primary owner; supplementary card users are not account owners.

**Rules:** R02, R03, R16

## account_status_event

A lifecycle change for an account.

**Grain:** One account status event.

**Primary key:** account_status_event_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_status_event_id` | `string` | false | identifier | Stable synthetic identifier for account status event. |
| `account_id` | `string` | false | identifier | Account whose status changed. |
| `status` | `string` | false | internal | New status. Allowed: OPEN, RESTRICTED, CLOSED. |
| `effective_at` | `timestamp` | false | internal | UTC effective time. |
| `reason` | `string` | false | internal | Human-readable reason for the change. |

**Unique keys:** Primary key only.

**Notes:** The latest event defines current status; historical entries are not rejected using current status.

**Rules:** R17, R20

## credit_facility

The credit agreement attached to a credit-card account.

**Grain:** One facility per credit-card account.

**Primary key:** credit_facility_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `credit_facility_id` | `string` | false | identifier | Stable synthetic identifier for credit facility. |
| `account_id` | `string` | false | identifier | Credit-card account supported by this facility. |
| `approved_on` | `date` | false | internal | Date credit was approved. |
| `currency_id` | `string` | false | identifier | Must match the linked account currency. |

**Unique keys:** account_id

**Notes:** Exactly one facility for each credit-card account; none for deposit accounts. Loans and underwriting are excluded.

**Rules:** R04

## credit_limit_event

A change in the approved credit limit.

**Grain:** One effective limit change per facility.

**Primary key:** credit_limit_event_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `credit_limit_event_id` | `string` | false | identifier | Stable synthetic identifier for credit limit event. |
| `credit_facility_id` | `string` | false | identifier | Facility whose limit changed. |
| `effective_at` | `timestamp` | false | internal | UTC time from which the limit applies. |
| `limit_amount` | `decimal(18,2)` | false | financial | Nonnegative approved limit in facility currency. |
| `reason` | `string` | false | internal | Reason for changing the limit. |

**Unique keys:** Primary key only.

**Notes:** Latest effective event gives current limit. Available credit also needs holds and balances, so it is not calculated here.

**Rules:** R04, R17

## card

An issued credit-card instrument.

**Grain:** One issued card instance, including each replacement.

**Primary key:** card_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `card_id` | `string` | false | identifier | Stable synthetic identifier for card. |
| `account_id` | `string` | false | identifier | Credit-card account billed for use. |
| `issued_on` | `date` | false | internal | Issue date. |
| `expires_on` | `date` | false | internal | Last valid calendar day. |
| `replaces_card_id` | `string` | true | identifier | Earlier card replaced by this card, when applicable. |

**Unique keys:** Primary key only.

**Notes:** No PAN, CVV, PIN or magnetic-stripe data. Debit cards and digital tokens are deferred.

**Rules:** R05, R06, R07, R11, R16

## card_assignment

The person authorized to use a card.

**Grain:** One card-to-person assignment interval.

**Primary key:** card_assignment_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `card_assignment_id` | `string` | false | identifier | Stable synthetic identifier for card assignment. |
| `card_id` | `string` | false | identifier | Card being assigned. |
| `customer_id` | `string` | false | identifier | Person authorized to use it. |
| `role` | `string` | false | internal | Card-user role. Allowed: PRIMARY, SUPPLEMENTARY. |
| `valid_from` | `date` | false | internal | First valid day, inclusive. |
| `valid_to` | `date` | true | internal | First invalid day, exclusive. |

**Unique keys:** Primary key only.

**Notes:** A supplementary user need not own the account. A card has at most one assigned person at a time.

**Rules:** R03, R05, R16

## card_status_event

A change in a card lifecycle.

**Grain:** One card status event.

**Primary key:** card_status_event_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `card_status_event_id` | `string` | false | identifier | Stable synthetic identifier for card status event. |
| `card_id` | `string` | false | identifier | Card whose status changed. |
| `status` | `string` | false | internal | New lifecycle status. Allowed: ISSUED, ACTIVE, BLOCKED, EXPIRED, CLOSED. |
| `effective_at` | `timestamp` | false | internal | UTC effective time. |

**Unique keys:** Primary key only.

**Notes:** Replacement does not move old transactions onto the new card.

**Rules:** R17

## merchant_category

A fictional grouping for merchant analytics.

**Grain:** One merchant category.

**Primary key:** merchant_category_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `merchant_category_id` | `string` | false | identifier | Stable synthetic identifier for merchant category. |
| `code` | `string` | false | internal | Project-local category code. |
| `name` | `string` | false | internal | Display category such as groceries or travel. |

**Unique keys:** code

**Notes:** Codes are illustrative; no claim of a complete network MCC reference.

**Rules:** 

## merchant

A merchant identity observed in card activity.

**Grain:** One merchant.

**Primary key:** merchant_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `merchant_id` | `string` | false | identifier | Stable synthetic identifier for merchant. |
| `merchant_category_id` | `string` | false | identifier | Merchant analytics category. |
| `name` | `string` | false | internal | Invented merchant name. |
| `country_code` | `string` | false | internal | Country code; CA in this scenario. Allowed: CA. |

**Unique keys:** Primary key only.

**Notes:** Merchant identity resolution across acquirers is deferred.

**Rules:** R07

## card_authorization

A request to approve card spending before posting.

**Grain:** One authorization request.

**Primary key:** card_authorization_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `card_authorization_id` | `string` | false | identifier | Stable synthetic identifier for card authorization. |
| `card_id` | `string` | false | identifier | Card presented for authorization. |
| `merchant_id` | `string` | false | identifier | Merchant requesting authorization. |
| `currency_id` | `string` | false | identifier | Requested currency. |
| `requested_amount` | `decimal(18,2)` | false | financial | Positive requested amount. |
| `requested_at` | `timestamp` | false | internal | UTC request time. |
| `decision` | `string` | false | internal | Authorization result. Allowed: APPROVED, DECLINED. |
| `channel_id` | `string` | false | identifier | Origin of the request. |

**Unique keys:** Primary key only.

**Notes:** An authorization is not a posted purchase. Hold expiry, incremental authorizations and reversals are deferred.

**Rules:** R07, R09, R18

## card_transaction

A posted purchase or refund received through the card network.

**Grain:** One posted card purchase or refund.

**Primary key:** card_transaction_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `card_transaction_id` | `string` | false | identifier | Stable synthetic identifier for card transaction. |
| `card_id` | `string` | false | identifier | Card used for this activity. |
| `merchant_id` | `string` | false | identifier | Merchant involved. |
| `currency_id` | `string` | false | identifier | Posted currency. |
| `authorization_id` | `string` | true | identifier | Related authorization when available; may be absent for offline clearing. |
| `original_transaction_id` | `string` | true | identifier | Purchase refunded by this refund. |
| `kind` | `string` | false | internal | Type of posted card activity. Allowed: PURCHASE, REFUND. |
| `amount` | `decimal(18,2)` | false | financial | Positive amount; kind determines economic direction. |
| `occurred_at` | `timestamp` | false | internal | UTC time of merchant activity. |
| `posted_on` | `date` | false | internal | Business date on which activity was posted. |

**Unique keys:** Primary key only.

**Notes:** One authorization may support multiple posted presentments. The relationship does not imply equal amounts.

**Rules:** R07, R08, R09, R10, R11, R16, R18

## account_entry

An immutable customer-account movement used for statement presentation.

**Grain:** One booked debit or credit on an account.

**Primary key:** account_entry_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_entry_id` | `string` | false | identifier | Stable synthetic identifier for account entry. |
| `account_id` | `string` | false | identifier | Account affected. |
| `card_transaction_id` | `string` | true | identifier | Card activity behind this entry, if any. |
| `payment_id` | `string` | true | identifier | Repayment behind this entry, if any. |
| `fee_type_id` | `string` | true | identifier | Fee category when this is a fee. |
| `reverses_entry_id` | `string` | true | identifier | Earlier entry reversed by this entry. |
| `kind` | `string` | false | internal | Business source of the entry. Allowed: CARD, PAYMENT, FEE, ADJUSTMENT, REVERSAL. |
| `direction` | `string` | false | internal | Customer-account debit or credit. Allowed: DEBIT, CREDIT. |
| `amount` | `decimal(18,2)` | false | financial | Positive amount in account currency. |
| `posted_on` | `date` | false | internal | Booking business date. |
| `description` | `string` | false | internal | Short statement narrative. |

**Unique keys:** Primary key only.

**Notes:** These are account subledger-style entries, not a balanced general ledger. A separate rule defines balance signs by account kind.

**Rules:** R09, R10, R11, R12, R13, R15

## payment

An external repayment to a credit-card account.

**Grain:** One received payment instruction.

**Primary key:** payment_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `payment_id` | `string` | false | identifier | Stable synthetic identifier for payment. |
| `account_id` | `string` | false | identifier | Credit-card account receiving the repayment. |
| `channel_id` | `string` | false | identifier | How the instruction arrived. |
| `currency_id` | `string` | false | identifier | Payment currency; must match the account. |
| `amount` | `decimal(18,2)` | false | financial | Positive repayment amount. |
| `received_at` | `timestamp` | false | internal | UTC receipt time. |
| `status` | `string` | false | internal | Current processing outcome. Allowed: PENDING, POSTED, FAILED. |

**Unique keys:** Primary key only.

**Notes:** All funding is external in this release. No internal transfer or payment-rail implementation.

**Rules:** R09, R10, R11, R18

## statement

An issued monthly billing snapshot for a credit-card account.

**Grain:** One issued statement for an account and cycle.

**Primary key:** statement_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `statement_id` | `string` | false | identifier | Stable synthetic identifier for statement. |
| `account_id` | `string` | false | identifier | Credit-card account being billed. |
| `period_start` | `date` | false | internal | First included posting date. |
| `period_end_exclusive` | `date` | false | internal | First excluded posting date. |
| `issued_on` | `date` | false | internal | Issue date. |
| `due_on` | `date` | false | internal | Payment due date. |
| `opening_balance` | `decimal(18,2)` | false | financial | Signed amount owed at start; negative means customer credit. |
| `closing_balance` | `decimal(18,2)` | false | financial | Signed amount owed at end. |
| `minimum_due` | `decimal(18,2)` | false | financial | Nonnegative supplied amount; calculation is outside scope. |

**Unique keys:** account_id, period_start, period_end_exclusive

**Notes:** Issued statements are immutable. Reissues and interest calculations are deferred.

**Rules:** R13, R14

## statement_line

A printed item on an issued statement.

**Grain:** One account entry displayed on one statement.

**Primary key:** statement_line_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `statement_line_id` | `string` | false | identifier | Stable synthetic identifier for statement line. |
| `statement_id` | `string` | false | identifier | Statement containing this line. |
| `account_entry_id` | `string` | false | identifier | Booked entry being displayed. |
| `line_number` | `integer` | false | internal | Positive order within the statement. |
| `narrative` | `string` | false | internal | Narrative captured at issue time. |

**Unique keys:** statement_id, line_number; account_entry_id

**Notes:** Amounts come from immutable entries. An entry appears on at most one issued statement in this simplified model.

**Rules:** R13

## account_balance_snapshot

A supplied end-of-day account balance.

**Grain:** One account and business date.

**Primary key:** account_balance_snapshot_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_balance_snapshot_id` | `string` | false | identifier | Stable synthetic identifier for account balance snapshot. |
| `account_id` | `string` | false | identifier | Account summarized. |
| `as_of_date` | `date` | false | internal | Business date of the snapshot. |
| `balance_amount` | `decimal(18,2)` | false | financial | Signed deposit funds or signed credit-card amount owed, according to account kind. |

**Unique keys:** account_id, as_of_date

**Notes:** A snapshot is a reconciliation reference, not a second source of transactions. Opening positions are required to rebuild balances.

**Rules:** R15

## dispute_reason

A project-local category for customer claims.

**Grain:** One dispute reason.

**Primary key:** dispute_reason_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `dispute_reason_id` | `string` | false | identifier | Stable synthetic identifier for dispute reason. |
| `code` | `string` | false | internal | Project-local reason code. Allowed: UNRECOGNIZED, DUPLICATE, GOODS_NOT_RECEIVED. |
| `description` | `string` | false | internal | Explanation of the reason. |

**Unique keys:** code

**Notes:** Not a card-network reason-code catalogue.

**Rules:** 

## dispute

A customer claim about a posted purchase.

**Grain:** One dispute case against one purchase.

**Primary key:** dispute_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `dispute_id` | `string` | false | identifier | Stable synthetic identifier for dispute. |
| `card_transaction_id` | `string` | false | identifier | Purchase being challenged. |
| `raised_by_customer_id` | `string` | false | identifier | Customer raising the case. |
| `dispute_reason_id` | `string` | false | identifier | Reason for the claim. |
| `claimed_amount` | `decimal(18,2)` | false | financial | Positive challenged portion of the purchase. |
| `opened_at` | `timestamp` | false | internal | UTC time the case was opened. |

**Unique keys:** Primary key only.

**Notes:** The owner or assigned card user may raise a case. A claim does not itself create a refund or provisional credit.

**Rules:** R09, R16

## dispute_event

A lifecycle event within a dispute case.

**Grain:** One event in a dispute.

**Primary key:** dispute_event_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `dispute_event_id` | `string` | false | identifier | Stable synthetic identifier for dispute event. |
| `dispute_id` | `string` | false | identifier | Case being progressed. |
| `status` | `string` | false | internal | New case status. Allowed: OPEN, UNDER_REVIEW, RESOLVED_CUSTOMER, RESOLVED_MERCHANT, CLOSED. |
| `occurred_at` | `timestamp` | false | internal | UTC event time. |
| `summary` | `string` | false | internal | Synthetic operational note; no personal narrative. |

**Unique keys:** Primary key only.

**Notes:** Chargeback messages, evidence files and provisional-credit postings are deferred.

**Rules:** R17

