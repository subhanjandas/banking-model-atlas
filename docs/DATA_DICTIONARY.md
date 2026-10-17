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
| `kind` | `string` | false | internal | Account family supported by this product. Allowed: DEPOSIT, CREDIT_CARD, TERM_LOAN. |

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

**Rules:** R01, R23

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

A customer-facing deposit, credit-card or term-loan account.

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

**Rules:** R01, R02, R04, R05, R11, R14, R15, R18, R20, R23, R25, R30, R35

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

**Notes:** Deposits can have joint owners. Credit-card and term-loan accounts have one primary owner; supplementary card users are not account owners.

**Rules:** R02, R03, R16, R30

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

**Unique keys:** account_id, effective_at

**Notes:** The latest event defines current status; historical entries are not rejected using current status.

**Rules:** R17, R20, R40

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

**Notes:** One facility for each credit-card account. Fixed-term loans have a separate loan_contract; underwriting decisions are supplied, not calculated.

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

**Unique keys:** card_id, effective_at

**Notes:** Replacement does not move old transactions onto the new card.

**Rules:** R17, R40

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
| `kind` | `string` | false | internal | Business source of the entry. Allowed: CARD, PAYMENT, FEE, ADJUSTMENT, REVERSAL, DEPOSIT_PAYMENT, LOAN_DRAW, LOAN_REPAYMENT. |
| `direction` | `string` | false | internal | Customer-account debit or credit. Allowed: DEBIT, CREDIT. |
| `amount` | `decimal(18,2)` | false | financial | Positive amount in account currency. |
| `posted_on` | `date` | false | internal | Booking business date. |
| `description` | `string` | false | internal | Short statement narrative. |
| `payment_order_id` | `string` | true | identifier | Deposit payment instruction behind this entry, if any. |
| `loan_disbursement_id` | `string` | true | identifier | Loan draw behind this principal or deposit entry, if any. |
| `loan_repayment_id` | `string` | true | identifier | Loan repayment behind a principal reduction, if any. |

**Unique keys:** Primary key only.

**Notes:** Customer-facing account entries form a subledger view. The separate journal and posting_link entities support accounting and reconciliation; the model is not a complete bank ledger platform.

**Rules:** R09, R10, R11, R12, R13, R15, R26, R32, R33, R35, R39, R42

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
| `balance_amount` | `decimal(18,2)` | false | financial | Signed deposit funds or credit-card/term-loan amount owed, according to product kind. |

**Unique keys:** account_id, as_of_date

**Notes:** A snapshot is a reconciliation reference, not a second source of transactions. Opening positions are required to rebuild balances.

**Rules:** R15, R42

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

## onboarding_case

A customer onboarding or refresh workflow.

**Grain:** One onboarding case for an existing customer identity.

**Primary key:** onboarding_case_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `onboarding_case_id` | `string` | false | identifier | Stable synthetic identifier for onboarding case. |
| `customer_id` | `string` | false | identifier | Person whose relationship is being reviewed. |
| `opened_at` | `timestamp` | false | internal | UTC time the case opened. |
| `case_type` | `string` | false | internal | Reason for this workflow. Allowed: INITIAL, REFRESH. |
| `status` | `string` | false | internal | Current workflow outcome. Allowed: OPEN, APPROVED, DECLINED, WITHDRAWN. |
| `closed_at` | `timestamp` | true | internal | UTC closure time, if complete. |

**Unique keys:** Primary key only.

**Notes:** The customer ID may exist before an account is approved. Workflow status is a current snapshot; full workflow events are deferred.

**Rules:** R22, R23, R24

## identity_check

A recorded identity-verification attempt, without identity documents.

**Grain:** One identity check attempt within an onboarding case.

**Primary key:** identity_check_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `identity_check_id` | `string` | false | identifier | Stable synthetic identifier for identity check. |
| `onboarding_case_id` | `string` | false | identifier | Case requiring this check. |
| `method` | `string` | false | internal | Illustrative method category. Allowed: DOCUMENT_REVIEW, TRUSTED_SOURCE. |
| `outcome` | `string` | false | internal | Recorded result. Allowed: PASS, FAIL, REVIEW. |
| `checked_at` | `timestamp` | false | internal | UTC time of the check. |
| `evidence_reference` | `string` | false | personal | Synthetic opaque reference; no document number or image. |

**Unique keys:** Primary key only.

**Notes:** No identity provider integration or statutory verification claim. Repeat attempts are separate rows.

**Rules:** R22

## kyc_review

A due-diligence review outcome recorded for a case.

**Grain:** One review attempt within an onboarding case.

**Primary key:** kyc_review_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `kyc_review_id` | `string` | false | identifier | Stable synthetic identifier for kyc review. |
| `onboarding_case_id` | `string` | false | identifier | Case being reviewed. |
| `outcome` | `string` | false | internal | Recorded reviewer outcome. Allowed: PASS, FAIL, REVIEW. |
| `reviewed_at` | `timestamp` | false | internal | UTC review time. |
| `rationale_code` | `string` | false | internal | Synthetic policy rationale code. |

**Unique keys:** Primary key only.

**Notes:** A PASS is a fictional workflow outcome, not proof of compliance. No sensitive review narrative is included.

**Rules:** R22

## screening_review

A screening result and subsequent review outcome.

**Grain:** One screening attempt within an onboarding case.

**Primary key:** screening_review_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `screening_review_id` | `string` | false | identifier | Stable synthetic identifier for screening review. |
| `onboarding_case_id` | `string` | false | identifier | Case associated with the screening. |
| `screening_type` | `string` | false | internal | Illustrative screening purpose. Allowed: SANCTIONS, PEP. |
| `outcome` | `string` | false | internal | Recorded result. Allowed: CLEAR, REVIEW, CONFIRMED. |
| `screened_at` | `timestamp` | false | internal | UTC time screening occurred. |

**Unique keys:** Primary key only.

**Notes:** No live lists, matched names or automated decisions. Potential matches require separate human review outside this demo.

**Rules:** R22

## customer_risk_assessment

A dated internal customer risk classification.

**Grain:** One assessment event for one customer.

**Primary key:** customer_risk_assessment_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `customer_risk_assessment_id` | `string` | false | identifier | Stable synthetic identifier for customer risk assessment. |
| `customer_id` | `string` | false | identifier | Customer being assessed. |
| `onboarding_case_id` | `string` | true | identifier | Related onboarding or refresh case, if applicable. |
| `risk_band` | `string` | false | internal | Illustrative internal classification. Allowed: LOW, MEDIUM, HIGH. |
| `assessed_at` | `timestamp` | false | internal | UTC assessment time. |
| `next_review_on` | `date` | false | internal | Planned review date. |

**Unique keys:** Primary key only.

**Notes:** No scoring algorithm or risk inference is implemented. Latest assessment gives current classification.

**Rules:** R24

## product_application

A request to open a deposit or credit-card product.

**Grain:** One product application submitted by a customer.

**Primary key:** product_application_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `product_application_id` | `string` | false | identifier | Stable synthetic identifier for product application. |
| `customer_id` | `string` | false | identifier | Applicant. |
| `product_version_id` | `string` | false | identifier | Requested offering. |
| `onboarding_case_id` | `string` | false | identifier | Onboarding case supporting the application. |
| `submitted_at` | `timestamp` | false | internal | UTC submission time. |
| `status` | `string` | false | internal | Application outcome. Allowed: SUBMITTED, APPROVED, DECLINED, WITHDRAWN. |
| `booked_account_id` | `string` | true | identifier | Account opened after approval, if booked. |

**Unique keys:** booked_account_id

**Notes:** Term-loan applications use loan_application. Approval need not mean an account has already been booked.

**Rules:** R23

## beneficiary

A payee saved by a customer for an external payment.

**Grain:** One customer-owned beneficiary record.

**Primary key:** beneficiary_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `beneficiary_id` | `string` | false | identifier | Stable synthetic identifier for beneficiary. |
| `customer_id` | `string` | false | identifier | Customer who saved the payee. |
| `display_name` | `string` | false | personal | Invented payee label. |
| `routing_reference` | `string` | false | personal | Opaque synthetic destination reference; not a real account number. |
| `status` | `string` | false | internal | Current availability. Allowed: ACTIVE, DISABLED. |

**Unique keys:** Primary key only.

**Notes:** An external payee is not assumed to be another modeled customer. Beneficiary changes and fraud controls are deferred.

**Rules:** R25

## standing_order

A recurring instruction template for an external payment.

**Grain:** One standing-order arrangement.

**Primary key:** standing_order_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `standing_order_id` | `string` | false | identifier | Stable synthetic identifier for standing order. |
| `source_account_id` | `string` | false | identifier | Deposit account to debit. |
| `beneficiary_id` | `string` | false | identifier | Saved external destination. |
| `amount` | `decimal(18,2)` | false | financial | Positive amount per scheduled execution. |
| `frequency` | `string` | false | internal | Supported recurrence. Allowed: MONTHLY. |
| `starts_on` | `date` | false | internal | First eligible date. |
| `ends_on` | `date` | true | internal | Last eligible date, inclusive. |
| `status` | `string` | false | internal | Current instruction state. Allowed: ACTIVE, CANCELLED. |

**Unique keys:** Primary key only.

**Notes:** Each execution creates a separate payment_order. Holiday calendars, retry logic and a scheduler are not implemented.

**Rules:** R28

## payment_order

An instruction to move funds from a deposit account.

**Grain:** One customer-authorized internal or outbound payment instruction.

**Primary key:** payment_order_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `payment_order_id` | `string` | false | identifier | Stable synthetic identifier for payment order. |
| `source_account_id` | `string` | false | identifier | Deposit account funding the instruction. |
| `destination_account_id` | `string` | true | identifier | Internal deposit destination; absent for external instructions. |
| `beneficiary_id` | `string` | true | identifier | External payee; absent for internal instructions. |
| `standing_order_id` | `string` | true | identifier | Recurring template that produced the order, if any. |
| `channel_id` | `string` | false | identifier | Channel accepting the instruction. |
| `currency_id` | `string` | false | identifier | Instruction currency. |
| `kind` | `string` | false | internal | Supported instruction type. Allowed: INTERNAL, OUTBOUND. |
| `amount` | `decimal(18,2)` | false | financial | Positive instructed amount. |
| `requested_at` | `timestamp` | false | internal | UTC acceptance time. |
| `requested_execution_on` | `date` | false | internal | Requested business execution date. |
| `idempotency_key` | `string` | false | internal | Unique client-request key in this single-bank scenario. |

**Unique keys:** idempotency_key

**Notes:** Status comes from payment_event. Internal movements have two customer-account entries; external ones have one.

**Rules:** R25, R26, R27, R28, R39

## payment_event

A lifecycle event for a deposit payment instruction.

**Grain:** One execution event for an order.

**Primary key:** payment_event_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `payment_event_id` | `string` | false | identifier | Stable synthetic identifier for payment event. |
| `payment_order_id` | `string` | false | identifier | Instruction being progressed. |
| `status` | `string` | false | internal | New execution state. Allowed: RECEIVED, VALIDATED, POSTED, SETTLED, FAILED, CANCELLED, REVERSED, RETURNED. |
| `occurred_at` | `timestamp` | false | internal | UTC event time. |
| `reason_code` | `string` | false | internal | Project-local processing reason. |

**Unique keys:** payment_order_id, occurred_at

**Notes:** Latest event gives status. Posting and external settlement are separate milestones.

**Rules:** R26, R27, R29, R39, R40

## payment_settlement

An observed external settlement result.

**Grain:** One settlement observation for an outbound order.

**Primary key:** payment_settlement_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `payment_settlement_id` | `string` | false | identifier | Stable synthetic identifier for payment settlement. |
| `payment_order_id` | `string` | false | identifier | Outbound order being settled. |
| `currency_id` | `string` | false | identifier | Settlement currency. |
| `settled_amount` | `decimal(18,2)` | false | financial | Positive settled amount. |
| `settled_on` | `date` | false | internal | Settlement business date. |
| `external_reference` | `string` | false | internal | Synthetic clearing reference. |

**Unique keys:** payment_order_id

**Notes:** One full settlement per order in this version. Partial settlement, returns and incoming rails are deferred.

**Rules:** R27

## account_hold

A temporary reservation of funds on a deposit account.

**Grain:** One reservation associated with a payment order.

**Primary key:** account_hold_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_hold_id` | `string` | false | identifier | Stable synthetic identifier for account hold. |
| `account_id` | `string` | false | identifier | Deposit account with reserved funds. |
| `payment_order_id` | `string` | false | identifier | Order causing the reservation. |
| `amount` | `decimal(18,2)` | false | financial | Positive reserved amount. |
| `placed_at` | `timestamp` | false | internal | UTC reservation time. |
| `released_at` | `timestamp` | true | internal | UTC release time; null means still held. |
| `expires_at` | `timestamp` | false | internal | UTC expiry time. |

**Unique keys:** Primary key only.

**Notes:** Holds affect availability but are not booked account entries. Full available-balance computation is deferred.

**Rules:** R28

## loan_application

A request for a fixed-term consumer loan.

**Grain:** One application by one primary borrower.

**Primary key:** loan_application_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `loan_application_id` | `string` | false | identifier | Stable synthetic identifier for loan application. |
| `customer_id` | `string` | false | identifier | Applicant and proposed borrower. |
| `product_version_id` | `string` | false | identifier | Requested TERM_LOAN product. |
| `onboarding_case_id` | `string` | false | identifier | Supporting onboarding case. |
| `requested_principal` | `decimal(18,2)` | false | financial | Positive requested principal in CAD. |
| `requested_term_months` | `integer` | false | internal | Positive requested term. |
| `submitted_at` | `timestamp` | false | internal | UTC submission time. |

**Unique keys:** Primary key only.

**Notes:** Co-borrowers, collateral and underwriting models are deferred.

**Rules:** R30

## credit_decision

A recorded lending decision for an application.

**Grain:** One dated decision on an application.

**Primary key:** credit_decision_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `credit_decision_id` | `string` | false | identifier | Stable synthetic identifier for credit decision. |
| `loan_application_id` | `string` | false | identifier | Application considered. |
| `outcome` | `string` | false | internal | Decision outcome. Allowed: APPROVED, DECLINED, REFER. |
| `approved_principal` | `decimal(18,2)` | true | financial | Approved principal; present only for APPROVED. |
| `approved_term_months` | `integer` | true | internal | Approved term; present only for APPROVED. |
| `decided_at` | `timestamp` | false | internal | UTC decision time. |
| `expires_on` | `date` | false | internal | Last valid acceptance date. |

**Unique keys:** Primary key only.

**Notes:** Decisions are supplied synthetic outcomes, not a credit scoring engine. Subsequent decisions are separate rows.

**Rules:** R30, R37

## loan_contract

An accepted fixed-term loan agreement.

**Grain:** One loan contract and its loan account.

**Primary key:** loan_contract_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `loan_contract_id` | `string` | false | identifier | Stable synthetic identifier for loan contract. |
| `account_id` | `string` | false | identifier | TERM_LOAN account representing the principal obligation. |
| `credit_decision_id` | `string` | false | identifier | Approved decision accepted by the borrower. |
| `principal_amount` | `decimal(18,2)` | false | financial | Contracted principal in account currency. |
| `term_months` | `integer` | false | internal | Positive contractual term. |
| `accepted_on` | `date` | false | internal | Contract acceptance date. |
| `matures_on` | `date` | false | internal | Contractual maturity date. |

**Unique keys:** account_id; credit_decision_id

**Notes:** Rates, interest accrual, modifications, arrears and impairment are out of scope. Schedule interest values are supplied.

**Rules:** R30, R31, R32, R33

## loan_schedule_item

An expected installment in a supplied repayment schedule.

**Grain:** One installment for a loan contract.

**Primary key:** loan_schedule_item_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `loan_schedule_item_id` | `string` | false | identifier | Stable synthetic identifier for loan schedule item. |
| `loan_contract_id` | `string` | false | identifier | Contract being scheduled. |
| `installment_number` | `integer` | false | internal | Positive sequence within the loan. |
| `due_on` | `date` | false | internal | Due date. |
| `principal_due` | `decimal(18,2)` | false | financial | Nonnegative scheduled principal. |
| `interest_due` | `decimal(18,2)` | false | financial | Nonnegative supplied interest amount. |

**Unique keys:** loan_contract_id, installment_number

**Notes:** This version stores a schedule; it does not calculate amortization or allocate payments to installments.

**Rules:** R31

## loan_disbursement

A funded principal draw on a loan contract.

**Grain:** One completed principal disbursement.

**Primary key:** loan_disbursement_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `loan_disbursement_id` | `string` | false | identifier | Stable synthetic identifier for loan disbursement. |
| `loan_contract_id` | `string` | false | identifier | Contract providing the funds. |
| `destination_account_id` | `string` | false | identifier | Internal deposit account receiving proceeds. |
| `amount` | `decimal(18,2)` | false | financial | Positive principal disbursed. |
| `disbursed_on` | `date` | false | internal | Funding business date. |

**Unique keys:** loan_contract_id

**Notes:** One full disbursement to a deposit account in this release. External funding and progressive draws are deferred.

**Rules:** R32

## loan_repayment

A received external repayment against a loan.

**Grain:** One received repayment with supplied principal/interest split.

**Primary key:** loan_repayment_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `loan_repayment_id` | `string` | false | identifier | Stable synthetic identifier for loan repayment. |
| `loan_contract_id` | `string` | false | identifier | Loan being repaid. |
| `principal_amount` | `decimal(18,2)` | false | financial | Nonnegative principal portion. |
| `interest_amount` | `decimal(18,2)` | false | financial | Nonnegative interest portion. |
| `received_on` | `date` | false | internal | Receipt business date. |
| `status` | `string` | false | internal | Current processing state. Allowed: PENDING, POSTED, FAILED. |

**Unique keys:** Primary key only.

**Notes:** Only the principal portion reduces the loan account balance. Interest goes to the accounting journal. Payment allocation and delinquency calculation are deferred.

**Rules:** R33

## gl_account

An account in the fictional bank chart of accounts.

**Grain:** One general-ledger account.

**Primary key:** gl_account_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `gl_account_id` | `string` | false | identifier | Stable synthetic identifier for gl account. |
| `code` | `string` | false | internal | Unique project-local ledger code. |
| `name` | `string` | false | internal | Ledger account description. |
| `account_class` | `string` | false | internal | Financial statement classification. Allowed: ASSET, LIABILITY, EQUITY, INCOME, EXPENSE. |
| `normal_balance` | `string` | false | internal | Expected normal balance side. Allowed: DEBIT, CREDIT. |

**Unique keys:** code

**Notes:** This is a small illustrative chart, not a regulatory chart of accounts.

**Rules:** R38, R41

## journal

A set of accounting lines posted together.

**Grain:** One single-currency journal for one legal entity.

**Primary key:** journal_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `journal_id` | `string` | false | identifier | Stable synthetic identifier for journal. |
| `currency_id` | `string` | false | identifier | Common currency of all lines. |
| `legal_entity_code` | `string` | false | internal | Single legal entity represented. Allowed: MHB_BANK. |
| `booked_on` | `date` | false | internal | Accounting business date. |
| `status` | `string` | false | internal | Journal lifecycle state. Allowed: DRAFT, POSTED. |
| `description` | `string` | false | internal | Synthetic accounting narrative. |
| `source_reference` | `string` | false | internal | Unique producer event reference for idempotent ingestion. |

**Unique keys:** source_reference

**Notes:** Every POSTED journal must balance independently. Journals are immutable after posting; corrections use new journals.

**Rules:** R34, R35, R41

## journal_line

One debit or credit within an accounting journal.

**Grain:** One line within one journal.

**Primary key:** journal_line_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `journal_line_id` | `string` | false | identifier | Stable synthetic identifier for journal line. |
| `journal_id` | `string` | false | identifier | Journal containing the line. |
| `gl_account_id` | `string` | false | identifier | Ledger account affected. |
| `line_number` | `integer` | false | internal | Positive sequence within the journal. |
| `direction` | `string` | false | internal | Accounting debit or credit. Allowed: DEBIT, CREDIT. |
| `amount` | `decimal(18,2)` | false | financial | Positive amount in journal currency. |

**Unique keys:** journal_id, line_number

**Notes:** A journal has at least two lines when posted. Bank general-ledger balances and customer-account balances have different meanings.

**Rules:** R34, R35, R38, R41

## posting_link

A reconciliation mapping from customer-account activity to a ledger line.

**Grain:** One allocation of an account entry to a journal line.

**Primary key:** posting_link_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `posting_link_id` | `string` | false | identifier | Stable synthetic identifier for posting link. |
| `account_entry_id` | `string` | false | identifier | Customer-account entry being mapped. |
| `journal_line_id` | `string` | false | identifier | Related ledger line. |
| `allocated_amount` | `decimal(18,2)` | false | financial | Positive mapped portion of the account entry. |

**Unique keys:** account_entry_id, journal_line_id

**Notes:** The mapped line uses the same debit/credit direction and currency as the account entry. Counterpart ledger lines need not have customer-account entries.

**Rules:** R35, R42

## reconciliation_run

A recorded comparison between two financial record sets.

**Grain:** One reconciliation execution for one business date and scope.

**Primary key:** reconciliation_run_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `reconciliation_run_id` | `string` | false | identifier | Stable synthetic identifier for reconciliation run. |
| `business_date` | `date` | false | internal | Date being reconciled. |
| `scope` | `string` | false | internal | Comparison being performed. Allowed: ACCOUNT_TO_GL, PAYMENT_TO_SETTLEMENT, STATEMENT_TO_ENTRIES. |
| `started_at` | `timestamp` | false | internal | UTC start time. |
| `completed_at` | `timestamp` | true | internal | UTC completion time. |
| `status` | `string` | false | internal | Execution outcome. Allowed: RUNNING, COMPLETE, FAILED. |

**Unique keys:** Primary key only.

**Notes:** A COMPLETE run may still contain unmatched items; completion does not mean reconciliation succeeded.

**Rules:** R36

## reconciliation_item

A match or exception recorded by a reconciliation run.

**Grain:** One comparison outcome within one run.

**Primary key:** reconciliation_item_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `reconciliation_item_id` | `string` | false | identifier | Stable synthetic identifier for reconciliation item. |
| `reconciliation_run_id` | `string` | false | identifier | Run that produced the outcome. |
| `account_entry_id` | `string` | true | identifier | Entry involved when comparing account and ledger records. |
| `journal_line_id` | `string` | true | identifier | Ledger line involved when available. |
| `payment_order_id` | `string` | true | identifier | Order involved when comparing payments and settlement. |
| `statement_id` | `string` | true | identifier | Statement involved when comparing billing totals. |
| `outcome` | `string` | false | internal | Comparison result. Allowed: MATCHED, UNMATCHED, AMOUNT_MISMATCH. |
| `difference_amount` | `decimal(18,2)` | false | financial | Signed left-side minus right-side difference in CAD. |
| `explanation` | `string` | false | internal | Synthetic explanation of the match or exception. |

**Unique keys:** Primary key only.

**Notes:** References are conditional on run scope. A reconciliation result is evidence, not a financial posting.

**Rules:** R36

## gl_balance_snapshot

One independently supplied ledger account balance at a business-date close.

**Grain:** One independently supplied ledger account balance at a business-date close.

**Primary key:** gl_balance_snapshot_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `gl_balance_snapshot_id` | `string` | false | identifier | Stable synthetic identifier. |
| `gl_account_id` | `string` | false | identifier | Ledger account being reconciled. |
| `as_of_date` | `date` | false | internal | Inclusive business-date close. |
| `signed_balance` | `decimal(18,2)` | false | financial | Debit-positive, credit-negative closing position. |

**Unique keys:** gl_account_id, as_of_date

**Notes:** Single CAD legal entity; balances use debit-positive signed amounts.

**Rules:** R41, R42

## account_gl_mapping

One customer account mapped to its ledger control account.

**Grain:** One customer account mapped to its ledger control account.

**Primary key:** account_gl_mapping_id

| Column | Type | Nullable | Classification | Definition |
|---|---|---|---|---|
| `account_gl_mapping_id` | `string` | false | identifier | Stable synthetic identifier. |
| `account_id` | `string` | false | identifier | Customer account represented. |
| `gl_account_id` | `string` | false | identifier | Control ledger account. |

**Unique keys:** account_id

**Notes:** Single CAD legal entity; balances use debit-positive signed amounts.

**Rules:** R42

