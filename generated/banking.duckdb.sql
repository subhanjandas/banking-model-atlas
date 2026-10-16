-- Banking Model Atlas | model 0.2.0
-- Dialect: DuckDB. Run in a fresh database. No DROP or destructive reset.
-- PK, non-self FK, UNIQUE, NOT NULL and enumerations are enforced.
-- Self-reference integrity and selected business rules are checked by scripts/run_demo.py.
-- TIMESTAMP values represent UTC by convention; no automatic time-zone conversion.
-- This reference DDL is not a production bank deployment.

-- One servicing branch.
CREATE TABLE "branch" (
  "branch_id" VARCHAR NOT NULL,
  "branch_code" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  "province_code" VARCHAR NOT NULL,
  PRIMARY KEY ("branch_id"),
  UNIQUE ("branch_code")
);
COMMENT ON TABLE "branch" IS 'A servicing location or virtual branch. Grain: One servicing branch.';
COMMENT ON COLUMN "branch"."branch_id" IS 'Stable synthetic identifier for branch.';
COMMENT ON COLUMN "branch"."branch_code" IS 'Unique fictional branch code.';
COMMENT ON COLUMN "branch"."name" IS 'Display name.';
COMMENT ON COLUMN "branch"."province_code" IS 'Servicing province or territory.';

-- One interaction channel.
CREATE TABLE "channel" (
  "channel_id" VARCHAR NOT NULL,
  "code" VARCHAR NOT NULL CHECK ("code" IN ('APP', 'WEB', 'BRANCH', 'PHONE', 'NETWORK')),
  "name" VARCHAR NOT NULL,
  PRIMARY KEY ("channel_id"),
  UNIQUE ("code")
);
COMMENT ON TABLE "channel" IS 'A route through which a customer action occurs. Grain: One interaction channel.';
COMMENT ON COLUMN "channel"."channel_id" IS 'Stable synthetic identifier for channel.';
COMMENT ON COLUMN "channel"."code" IS 'Stable channel code.';
COMMENT ON COLUMN "channel"."name" IS 'Human-readable channel name.';

-- One currency.
CREATE TABLE "currency" (
  "currency_id" VARCHAR NOT NULL,
  "code" VARCHAR NOT NULL CHECK ("code" IN ('CAD')),
  "minor_unit_digits" INTEGER NOT NULL,
  PRIMARY KEY ("currency_id"),
  UNIQUE ("code")
);
COMMENT ON TABLE "currency" IS 'A currency reference used by monetary entities. Grain: One currency.';
COMMENT ON COLUMN "currency"."currency_id" IS 'Stable synthetic identifier for currency.';
COMMENT ON COLUMN "currency"."code" IS 'Currency code; CAD is the only supported value.';
COMMENT ON COLUMN "currency"."minor_unit_digits" IS 'Number of fractional digits; 2 for CAD.';

-- One natural person.
CREATE TABLE "customer" (
  "customer_id" VARCHAR NOT NULL,
  "display_name" VARCHAR NOT NULL,
  "customer_since" DATE NOT NULL,
  "segment" VARCHAR NOT NULL CHECK ("segment" IN ('STANDARD', 'PREMIUM')),
  "status" VARCHAR NOT NULL CHECK ("status" IN ('ACTIVE', 'CLOSED')),
  PRIMARY KEY ("customer_id")
);
COMMENT ON TABLE "customer" IS 'A person with a relationship to the fictional bank. Grain: One natural person.';
COMMENT ON COLUMN "customer"."customer_id" IS 'Stable synthetic identifier for customer.';
COMMENT ON COLUMN "customer"."display_name" IS 'Invented display name; never an actual customer name.';
COMMENT ON COLUMN "customer"."customer_since" IS 'Date this customer relationship began.';
COMMENT ON COLUMN "customer"."segment" IS 'Simple service grouping.';
COMMENT ON COLUMN "customer"."status" IS 'Current customer relationship status.';

-- One dispute reason.
CREATE TABLE "dispute_reason" (
  "dispute_reason_id" VARCHAR NOT NULL,
  "code" VARCHAR NOT NULL CHECK ("code" IN ('UNRECOGNIZED', 'DUPLICATE', 'GOODS_NOT_RECEIVED')),
  "description" VARCHAR NOT NULL,
  PRIMARY KEY ("dispute_reason_id"),
  UNIQUE ("code")
);
COMMENT ON TABLE "dispute_reason" IS 'A project-local category for customer claims. Grain: One dispute reason.';
COMMENT ON COLUMN "dispute_reason"."dispute_reason_id" IS 'Stable synthetic identifier for dispute reason.';
COMMENT ON COLUMN "dispute_reason"."code" IS 'Project-local reason code.';
COMMENT ON COLUMN "dispute_reason"."description" IS 'Explanation of the reason.';

-- One fee category.
CREATE TABLE "fee_type" (
  "fee_type_id" VARCHAR NOT NULL,
  "code" VARCHAR NOT NULL CHECK ("code" IN ('ANNUAL', 'LATE', 'SERVICE')),
  "description" VARCHAR NOT NULL,
  PRIMARY KEY ("fee_type_id"),
  UNIQUE ("code")
);
COMMENT ON TABLE "fee_type" IS 'A category of account fee. Grain: One fee category.';
COMMENT ON COLUMN "fee_type"."fee_type_id" IS 'Stable synthetic identifier for fee type.';
COMMENT ON COLUMN "fee_type"."code" IS 'Stable fee category.';
COMMENT ON COLUMN "fee_type"."description" IS 'What the category means.';

-- One general-ledger account.
CREATE TABLE "gl_account" (
  "gl_account_id" VARCHAR NOT NULL,
  "code" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  "account_class" VARCHAR NOT NULL CHECK ("account_class" IN ('ASSET', 'LIABILITY', 'EQUITY', 'INCOME', 'EXPENSE')),
  "normal_balance" VARCHAR NOT NULL CHECK ("normal_balance" IN ('DEBIT', 'CREDIT')),
  PRIMARY KEY ("gl_account_id"),
  UNIQUE ("code")
);
COMMENT ON TABLE "gl_account" IS 'An account in the fictional bank chart of accounts. Grain: One general-ledger account.';
COMMENT ON COLUMN "gl_account"."gl_account_id" IS 'Stable synthetic identifier for gl account.';
COMMENT ON COLUMN "gl_account"."code" IS 'Unique project-local ledger code.';
COMMENT ON COLUMN "gl_account"."name" IS 'Ledger account description.';
COMMENT ON COLUMN "gl_account"."account_class" IS 'Financial statement classification.';
COMMENT ON COLUMN "gl_account"."normal_balance" IS 'Expected normal balance side.';

-- One merchant category.
CREATE TABLE "merchant_category" (
  "merchant_category_id" VARCHAR NOT NULL,
  "code" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  PRIMARY KEY ("merchant_category_id"),
  UNIQUE ("code")
);
COMMENT ON TABLE "merchant_category" IS 'A fictional grouping for merchant analytics. Grain: One merchant category.';
COMMENT ON COLUMN "merchant_category"."merchant_category_id" IS 'Stable synthetic identifier for merchant category.';
COMMENT ON COLUMN "merchant_category"."code" IS 'Project-local category code.';
COMMENT ON COLUMN "merchant_category"."name" IS 'Display category such as groceries or travel.';

-- One product family.
CREATE TABLE "product" (
  "product_id" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  "kind" VARCHAR NOT NULL CHECK ("kind" IN ('DEPOSIT', 'CREDIT_CARD', 'TERM_LOAN')),
  PRIMARY KEY ("product_id")
);
COMMENT ON TABLE "product" IS 'A named deposit or credit-card offering. Grain: One product family.';
COMMENT ON COLUMN "product"."product_id" IS 'Stable synthetic identifier for product.';
COMMENT ON COLUMN "product"."name" IS 'Fictional marketing name.';
COMMENT ON COLUMN "product"."kind" IS 'Account family supported by this product.';

-- One reconciliation execution for one business date and scope.
CREATE TABLE "reconciliation_run" (
  "reconciliation_run_id" VARCHAR NOT NULL,
  "business_date" DATE NOT NULL,
  "scope" VARCHAR NOT NULL CHECK ("scope" IN ('ACCOUNT_TO_GL', 'PAYMENT_TO_SETTLEMENT', 'STATEMENT_TO_ENTRIES')),
  "started_at" TIMESTAMP NOT NULL,
  "completed_at" TIMESTAMP,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('RUNNING', 'COMPLETE', 'FAILED')),
  PRIMARY KEY ("reconciliation_run_id")
);
COMMENT ON TABLE "reconciliation_run" IS 'A recorded comparison between two financial record sets. Grain: One reconciliation execution for one business date and scope.';
COMMENT ON COLUMN "reconciliation_run"."reconciliation_run_id" IS 'Stable synthetic identifier for reconciliation run.';
COMMENT ON COLUMN "reconciliation_run"."business_date" IS 'Date being reconciled.';
COMMENT ON COLUMN "reconciliation_run"."scope" IS 'Comparison being performed.';
COMMENT ON COLUMN "reconciliation_run"."started_at" IS 'UTC start time.';
COMMENT ON COLUMN "reconciliation_run"."completed_at" IS 'UTC completion time.';
COMMENT ON COLUMN "reconciliation_run"."status" IS 'Execution outcome.';

-- One customer-owned beneficiary record.
CREATE TABLE "beneficiary" (
  "beneficiary_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "display_name" VARCHAR NOT NULL,
  "routing_reference" VARCHAR NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('ACTIVE', 'DISABLED')),
  PRIMARY KEY ("beneficiary_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id")
);
COMMENT ON TABLE "beneficiary" IS 'A payee saved by a customer for an external payment. Grain: One customer-owned beneficiary record.';
COMMENT ON COLUMN "beneficiary"."beneficiary_id" IS 'Stable synthetic identifier for beneficiary.';
COMMENT ON COLUMN "beneficiary"."customer_id" IS 'Customer who saved the payee.';
COMMENT ON COLUMN "beneficiary"."display_name" IS 'Invented payee label.';
COMMENT ON COLUMN "beneficiary"."routing_reference" IS 'Opaque synthetic destination reference; not a real account number.';
COMMENT ON COLUMN "beneficiary"."status" IS 'Current availability.';

-- One customer address assignment for one purpose and interval.
CREATE TABLE "customer_address" (
  "customer_address_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "purpose" VARCHAR NOT NULL CHECK ("purpose" IN ('HOME', 'MAILING')),
  "address_text" VARCHAR NOT NULL,
  "province_code" VARCHAR NOT NULL,
  "valid_from" DATE NOT NULL,
  "valid_to" DATE,
  PRIMARY KEY ("customer_address_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id")
);
COMMENT ON TABLE "customer_address" IS 'An address held for a customer over a period. Grain: One customer address assignment for one purpose and interval.';
COMMENT ON COLUMN "customer_address"."customer_address_id" IS 'Stable synthetic identifier for customer address.';
COMMENT ON COLUMN "customer_address"."customer_id" IS 'Person to whom this address belongs.';
COMMENT ON COLUMN "customer_address"."purpose" IS 'Reason this address is held.';
COMMENT ON COLUMN "customer_address"."address_text" IS 'Invented street and locality.';
COMMENT ON COLUMN "customer_address"."province_code" IS 'Province or territory abbreviation.';
COMMENT ON COLUMN "customer_address"."valid_from" IS 'First valid day, inclusive.';
COMMENT ON COLUMN "customer_address"."valid_to" IS 'First invalid day, exclusive; null means open-ended.';

-- One consent decision event for one customer and purpose.
CREATE TABLE "customer_consent" (
  "customer_consent_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "purpose" VARCHAR NOT NULL CHECK ("purpose" IN ('EMAIL_MARKETING', 'SMS_MARKETING')),
  "decision" VARCHAR NOT NULL CHECK ("decision" IN ('GRANTED', 'WITHDRAWN')),
  "decided_at" TIMESTAMP NOT NULL,
  "channel_id" VARCHAR NOT NULL,
  PRIMARY KEY ("customer_consent_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id"),
  FOREIGN KEY ("channel_id") REFERENCES "channel" ("channel_id")
);
COMMENT ON TABLE "customer_consent" IS 'A recorded choice about a specific optional purpose. Grain: One consent decision event for one customer and purpose.';
COMMENT ON COLUMN "customer_consent"."customer_consent_id" IS 'Stable synthetic identifier for customer consent.';
COMMENT ON COLUMN "customer_consent"."customer_id" IS 'Person who made the choice.';
COMMENT ON COLUMN "customer_consent"."purpose" IS 'Optional use covered by the choice.';
COMMENT ON COLUMN "customer_consent"."decision" IS 'Choice recorded.';
COMMENT ON COLUMN "customer_consent"."decided_at" IS 'UTC time of the decision.';
COMMENT ON COLUMN "customer_consent"."channel_id" IS 'Channel that recorded the choice.';

-- One contact method for a customer.
CREATE TABLE "customer_contact" (
  "customer_contact_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "contact_type" VARCHAR NOT NULL CHECK ("contact_type" IN ('EMAIL', 'PHONE')),
  "contact_value" VARCHAR NOT NULL,
  "is_preferred" BOOLEAN NOT NULL,
  PRIMARY KEY ("customer_contact_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id")
);
COMMENT ON TABLE "customer_contact" IS 'A way to reach a customer. Grain: One contact method for a customer.';
COMMENT ON COLUMN "customer_contact"."customer_contact_id" IS 'Stable synthetic identifier for customer contact.';
COMMENT ON COLUMN "customer_contact"."customer_id" IS 'Customer reached by this contact.';
COMMENT ON COLUMN "customer_contact"."contact_type" IS 'Contact medium.';
COMMENT ON COLUMN "customer_contact"."contact_value" IS 'Fictional contact value; example emails use example.com.';
COMMENT ON COLUMN "customer_contact"."is_preferred" IS 'Whether this is preferred within its contact type.';

-- One single-currency journal for one legal entity.
CREATE TABLE "journal" (
  "journal_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "legal_entity_code" VARCHAR NOT NULL CHECK ("legal_entity_code" IN ('MHB_BANK')),
  "booked_on" DATE NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('DRAFT', 'POSTED')),
  "description" VARCHAR NOT NULL,
  "source_reference" VARCHAR NOT NULL,
  PRIMARY KEY ("journal_id"),
  UNIQUE ("source_reference"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id")
);
COMMENT ON TABLE "journal" IS 'A set of accounting lines posted together. Grain: One single-currency journal for one legal entity.';
COMMENT ON COLUMN "journal"."journal_id" IS 'Stable synthetic identifier for journal.';
COMMENT ON COLUMN "journal"."currency_id" IS 'Common currency of all lines.';
COMMENT ON COLUMN "journal"."legal_entity_code" IS 'Single legal entity represented.';
COMMENT ON COLUMN "journal"."booked_on" IS 'Accounting business date.';
COMMENT ON COLUMN "journal"."status" IS 'Journal lifecycle state.';
COMMENT ON COLUMN "journal"."description" IS 'Synthetic accounting narrative.';
COMMENT ON COLUMN "journal"."source_reference" IS 'Unique producer event reference for idempotent ingestion.';

-- One merchant.
CREATE TABLE "merchant" (
  "merchant_id" VARCHAR NOT NULL,
  "merchant_category_id" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  "country_code" VARCHAR NOT NULL CHECK ("country_code" IN ('CA')),
  PRIMARY KEY ("merchant_id"),
  FOREIGN KEY ("merchant_category_id") REFERENCES "merchant_category" ("merchant_category_id")
);
COMMENT ON TABLE "merchant" IS 'A merchant identity observed in card activity. Grain: One merchant.';
COMMENT ON COLUMN "merchant"."merchant_id" IS 'Stable synthetic identifier for merchant.';
COMMENT ON COLUMN "merchant"."merchant_category_id" IS 'Merchant analytics category.';
COMMENT ON COLUMN "merchant"."name" IS 'Invented merchant name.';
COMMENT ON COLUMN "merchant"."country_code" IS 'Country code; CA in this scenario.';

-- One onboarding case for an existing customer identity.
CREATE TABLE "onboarding_case" (
  "onboarding_case_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "opened_at" TIMESTAMP NOT NULL,
  "case_type" VARCHAR NOT NULL CHECK ("case_type" IN ('INITIAL', 'REFRESH')),
  "status" VARCHAR NOT NULL CHECK ("status" IN ('OPEN', 'APPROVED', 'DECLINED', 'WITHDRAWN')),
  "closed_at" TIMESTAMP,
  PRIMARY KEY ("onboarding_case_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id")
);
COMMENT ON TABLE "onboarding_case" IS 'A customer onboarding or refresh workflow. Grain: One onboarding case for an existing customer identity.';
COMMENT ON COLUMN "onboarding_case"."onboarding_case_id" IS 'Stable synthetic identifier for onboarding case.';
COMMENT ON COLUMN "onboarding_case"."customer_id" IS 'Person whose relationship is being reviewed.';
COMMENT ON COLUMN "onboarding_case"."opened_at" IS 'UTC time the case opened.';
COMMENT ON COLUMN "onboarding_case"."case_type" IS 'Reason for this workflow.';
COMMENT ON COLUMN "onboarding_case"."status" IS 'Current workflow outcome.';
COMMENT ON COLUMN "onboarding_case"."closed_at" IS 'UTC closure time, if complete.';

-- One version of one product.
CREATE TABLE "product_version" (
  "product_version_id" VARCHAR NOT NULL,
  "product_id" VARCHAR NOT NULL,
  "version_number" INTEGER NOT NULL,
  "effective_from" DATE NOT NULL,
  "effective_to" DATE,
  "terms_summary" VARCHAR NOT NULL,
  PRIMARY KEY ("product_version_id"),
  UNIQUE ("product_id", "version_number"),
  FOREIGN KEY ("product_id") REFERENCES "product" ("product_id")
);
COMMENT ON TABLE "product_version" IS 'A dated edition of product terms. Grain: One version of one product.';
COMMENT ON COLUMN "product_version"."product_version_id" IS 'Stable synthetic identifier for product version.';
COMMENT ON COLUMN "product_version"."product_id" IS 'Product whose terms are versioned.';
COMMENT ON COLUMN "product_version"."version_number" IS 'Increasing number within the product.';
COMMENT ON COLUMN "product_version"."effective_from" IS 'First day offered, inclusive.';
COMMENT ON COLUMN "product_version"."effective_to" IS 'First day no longer offered, exclusive.';
COMMENT ON COLUMN "product_version"."terms_summary" IS 'Plain-language description; not a contract.';

-- One account contract.
CREATE TABLE "account" (
  "account_id" VARCHAR NOT NULL,
  "product_version_id" VARCHAR NOT NULL,
  "branch_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "opened_on" DATE NOT NULL,
  "closed_on" DATE,
  PRIMARY KEY ("account_id"),
  FOREIGN KEY ("product_version_id") REFERENCES "product_version" ("product_version_id"),
  FOREIGN KEY ("branch_id") REFERENCES "branch" ("branch_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id")
);
COMMENT ON TABLE "account" IS 'A customer-facing deposit, credit-card or term-loan account. Grain: One account contract.';
COMMENT ON COLUMN "account"."account_id" IS 'Stable synthetic identifier for account.';
COMMENT ON COLUMN "account"."product_version_id" IS 'Product terms booked at account opening.';
COMMENT ON COLUMN "account"."branch_id" IS 'Branch responsible for servicing.';
COMMENT ON COLUMN "account"."currency_id" IS 'Account denomination.';
COMMENT ON COLUMN "account"."opened_on" IS 'First day of the account.';
COMMENT ON COLUMN "account"."closed_on" IS 'Closure date, if closed.';

-- One assessment event for one customer.
CREATE TABLE "customer_risk_assessment" (
  "customer_risk_assessment_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "onboarding_case_id" VARCHAR,
  "risk_band" VARCHAR NOT NULL CHECK ("risk_band" IN ('LOW', 'MEDIUM', 'HIGH')),
  "assessed_at" TIMESTAMP NOT NULL,
  "next_review_on" DATE NOT NULL,
  PRIMARY KEY ("customer_risk_assessment_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id"),
  FOREIGN KEY ("onboarding_case_id") REFERENCES "onboarding_case" ("onboarding_case_id")
);
COMMENT ON TABLE "customer_risk_assessment" IS 'A dated internal customer risk classification. Grain: One assessment event for one customer.';
COMMENT ON COLUMN "customer_risk_assessment"."customer_risk_assessment_id" IS 'Stable synthetic identifier for customer risk assessment.';
COMMENT ON COLUMN "customer_risk_assessment"."customer_id" IS 'Customer being assessed.';
COMMENT ON COLUMN "customer_risk_assessment"."onboarding_case_id" IS 'Related onboarding or refresh case, if applicable.';
COMMENT ON COLUMN "customer_risk_assessment"."risk_band" IS 'Illustrative internal classification.';
COMMENT ON COLUMN "customer_risk_assessment"."assessed_at" IS 'UTC assessment time.';
COMMENT ON COLUMN "customer_risk_assessment"."next_review_on" IS 'Planned review date.';

-- One identity check attempt within an onboarding case.
CREATE TABLE "identity_check" (
  "identity_check_id" VARCHAR NOT NULL,
  "onboarding_case_id" VARCHAR NOT NULL,
  "method" VARCHAR NOT NULL CHECK ("method" IN ('DOCUMENT_REVIEW', 'TRUSTED_SOURCE')),
  "outcome" VARCHAR NOT NULL CHECK ("outcome" IN ('PASS', 'FAIL', 'REVIEW')),
  "checked_at" TIMESTAMP NOT NULL,
  "evidence_reference" VARCHAR NOT NULL,
  PRIMARY KEY ("identity_check_id"),
  FOREIGN KEY ("onboarding_case_id") REFERENCES "onboarding_case" ("onboarding_case_id")
);
COMMENT ON TABLE "identity_check" IS 'A recorded identity-verification attempt, without identity documents. Grain: One identity check attempt within an onboarding case.';
COMMENT ON COLUMN "identity_check"."identity_check_id" IS 'Stable synthetic identifier for identity check.';
COMMENT ON COLUMN "identity_check"."onboarding_case_id" IS 'Case requiring this check.';
COMMENT ON COLUMN "identity_check"."method" IS 'Illustrative method category.';
COMMENT ON COLUMN "identity_check"."outcome" IS 'Recorded result.';
COMMENT ON COLUMN "identity_check"."checked_at" IS 'UTC time of the check.';
COMMENT ON COLUMN "identity_check"."evidence_reference" IS 'Synthetic opaque reference; no document number or image.';

-- One line within one journal.
CREATE TABLE "journal_line" (
  "journal_line_id" VARCHAR NOT NULL,
  "journal_id" VARCHAR NOT NULL,
  "gl_account_id" VARCHAR NOT NULL,
  "line_number" INTEGER NOT NULL,
  "direction" VARCHAR NOT NULL CHECK ("direction" IN ('DEBIT', 'CREDIT')),
  "amount" DECIMAL(18,2) NOT NULL,
  PRIMARY KEY ("journal_line_id"),
  UNIQUE ("journal_id", "line_number"),
  FOREIGN KEY ("journal_id") REFERENCES "journal" ("journal_id"),
  FOREIGN KEY ("gl_account_id") REFERENCES "gl_account" ("gl_account_id")
);
COMMENT ON TABLE "journal_line" IS 'One debit or credit within an accounting journal. Grain: One line within one journal.';
COMMENT ON COLUMN "journal_line"."journal_line_id" IS 'Stable synthetic identifier for journal line.';
COMMENT ON COLUMN "journal_line"."journal_id" IS 'Journal containing the line.';
COMMENT ON COLUMN "journal_line"."gl_account_id" IS 'Ledger account affected.';
COMMENT ON COLUMN "journal_line"."line_number" IS 'Positive sequence within the journal.';
COMMENT ON COLUMN "journal_line"."direction" IS 'Accounting debit or credit.';
COMMENT ON COLUMN "journal_line"."amount" IS 'Positive amount in journal currency.';

-- One review attempt within an onboarding case.
CREATE TABLE "kyc_review" (
  "kyc_review_id" VARCHAR NOT NULL,
  "onboarding_case_id" VARCHAR NOT NULL,
  "outcome" VARCHAR NOT NULL CHECK ("outcome" IN ('PASS', 'FAIL', 'REVIEW')),
  "reviewed_at" TIMESTAMP NOT NULL,
  "rationale_code" VARCHAR NOT NULL,
  PRIMARY KEY ("kyc_review_id"),
  FOREIGN KEY ("onboarding_case_id") REFERENCES "onboarding_case" ("onboarding_case_id")
);
COMMENT ON TABLE "kyc_review" IS 'A due-diligence review outcome recorded for a case. Grain: One review attempt within an onboarding case.';
COMMENT ON COLUMN "kyc_review"."kyc_review_id" IS 'Stable synthetic identifier for kyc review.';
COMMENT ON COLUMN "kyc_review"."onboarding_case_id" IS 'Case being reviewed.';
COMMENT ON COLUMN "kyc_review"."outcome" IS 'Recorded reviewer outcome.';
COMMENT ON COLUMN "kyc_review"."reviewed_at" IS 'UTC review time.';
COMMENT ON COLUMN "kyc_review"."rationale_code" IS 'Synthetic policy rationale code.';

-- One application by one primary borrower.
CREATE TABLE "loan_application" (
  "loan_application_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "product_version_id" VARCHAR NOT NULL,
  "onboarding_case_id" VARCHAR NOT NULL,
  "requested_principal" DECIMAL(18,2) NOT NULL,
  "requested_term_months" INTEGER NOT NULL,
  "submitted_at" TIMESTAMP NOT NULL,
  PRIMARY KEY ("loan_application_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id"),
  FOREIGN KEY ("product_version_id") REFERENCES "product_version" ("product_version_id"),
  FOREIGN KEY ("onboarding_case_id") REFERENCES "onboarding_case" ("onboarding_case_id")
);
COMMENT ON TABLE "loan_application" IS 'A request for a fixed-term consumer loan. Grain: One application by one primary borrower.';
COMMENT ON COLUMN "loan_application"."loan_application_id" IS 'Stable synthetic identifier for loan application.';
COMMENT ON COLUMN "loan_application"."customer_id" IS 'Applicant and proposed borrower.';
COMMENT ON COLUMN "loan_application"."product_version_id" IS 'Requested TERM_LOAN product.';
COMMENT ON COLUMN "loan_application"."onboarding_case_id" IS 'Supporting onboarding case.';
COMMENT ON COLUMN "loan_application"."requested_principal" IS 'Positive requested principal in CAD.';
COMMENT ON COLUMN "loan_application"."requested_term_months" IS 'Positive requested term.';
COMMENT ON COLUMN "loan_application"."submitted_at" IS 'UTC submission time.';

-- One screening attempt within an onboarding case.
CREATE TABLE "screening_review" (
  "screening_review_id" VARCHAR NOT NULL,
  "onboarding_case_id" VARCHAR NOT NULL,
  "screening_type" VARCHAR NOT NULL CHECK ("screening_type" IN ('SANCTIONS', 'PEP')),
  "outcome" VARCHAR NOT NULL CHECK ("outcome" IN ('CLEAR', 'REVIEW', 'CONFIRMED')),
  "screened_at" TIMESTAMP NOT NULL,
  PRIMARY KEY ("screening_review_id"),
  FOREIGN KEY ("onboarding_case_id") REFERENCES "onboarding_case" ("onboarding_case_id")
);
COMMENT ON TABLE "screening_review" IS 'A screening result and subsequent review outcome. Grain: One screening attempt within an onboarding case.';
COMMENT ON COLUMN "screening_review"."screening_review_id" IS 'Stable synthetic identifier for screening review.';
COMMENT ON COLUMN "screening_review"."onboarding_case_id" IS 'Case associated with the screening.';
COMMENT ON COLUMN "screening_review"."screening_type" IS 'Illustrative screening purpose.';
COMMENT ON COLUMN "screening_review"."outcome" IS 'Recorded result.';
COMMENT ON COLUMN "screening_review"."screened_at" IS 'UTC time screening occurred.';

-- One account and business date.
CREATE TABLE "account_balance_snapshot" (
  "account_balance_snapshot_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "as_of_date" DATE NOT NULL,
  "balance_amount" DECIMAL(18,2) NOT NULL,
  PRIMARY KEY ("account_balance_snapshot_id"),
  UNIQUE ("account_id", "as_of_date"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id")
);
COMMENT ON TABLE "account_balance_snapshot" IS 'A supplied end-of-day account balance. Grain: One account and business date.';
COMMENT ON COLUMN "account_balance_snapshot"."account_balance_snapshot_id" IS 'Stable synthetic identifier for account balance snapshot.';
COMMENT ON COLUMN "account_balance_snapshot"."account_id" IS 'Account summarized.';
COMMENT ON COLUMN "account_balance_snapshot"."as_of_date" IS 'Business date of the snapshot.';
COMMENT ON COLUMN "account_balance_snapshot"."balance_amount" IS 'Signed deposit funds or credit-card/term-loan amount owed, according to product kind.';

-- One customer role on an account for an interval.
CREATE TABLE "account_holder" (
  "account_holder_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "role" VARCHAR NOT NULL CHECK ("role" IN ('PRIMARY', 'JOINT')),
  "valid_from" DATE NOT NULL,
  "valid_to" DATE,
  PRIMARY KEY ("account_holder_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id")
);
COMMENT ON TABLE "account_holder" IS 'Ownership or signing authority over an account. Grain: One customer role on an account for an interval.';
COMMENT ON COLUMN "account_holder"."account_holder_id" IS 'Stable synthetic identifier for account holder.';
COMMENT ON COLUMN "account_holder"."account_id" IS 'Account to which the role applies.';
COMMENT ON COLUMN "account_holder"."customer_id" IS 'Person assigned the role.';
COMMENT ON COLUMN "account_holder"."role" IS 'Legal or operational role in this fictional scenario.';
COMMENT ON COLUMN "account_holder"."valid_from" IS 'First valid day, inclusive.';
COMMENT ON COLUMN "account_holder"."valid_to" IS 'First invalid day, exclusive.';

-- One account status event.
CREATE TABLE "account_status_event" (
  "account_status_event_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('OPEN', 'RESTRICTED', 'CLOSED')),
  "effective_at" TIMESTAMP NOT NULL,
  "reason" VARCHAR NOT NULL,
  PRIMARY KEY ("account_status_event_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id")
);
COMMENT ON TABLE "account_status_event" IS 'A lifecycle change for an account. Grain: One account status event.';
COMMENT ON COLUMN "account_status_event"."account_status_event_id" IS 'Stable synthetic identifier for account status event.';
COMMENT ON COLUMN "account_status_event"."account_id" IS 'Account whose status changed.';
COMMENT ON COLUMN "account_status_event"."status" IS 'New status.';
COMMENT ON COLUMN "account_status_event"."effective_at" IS 'UTC effective time.';
COMMENT ON COLUMN "account_status_event"."reason" IS 'Human-readable reason for the change.';

-- One issued card instance, including each replacement.
CREATE TABLE "card" (
  "card_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "issued_on" DATE NOT NULL,
  "expires_on" DATE NOT NULL,
  "replaces_card_id" VARCHAR,
  PRIMARY KEY ("card_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id")
);
COMMENT ON TABLE "card" IS 'An issued credit-card instrument. Grain: One issued card instance, including each replacement.';
COMMENT ON COLUMN "card"."card_id" IS 'Stable synthetic identifier for card.';
COMMENT ON COLUMN "card"."account_id" IS 'Credit-card account billed for use.';
COMMENT ON COLUMN "card"."issued_on" IS 'Issue date.';
COMMENT ON COLUMN "card"."expires_on" IS 'Last valid calendar day.';
COMMENT ON COLUMN "card"."replaces_card_id" IS 'Earlier card replaced by this card, when applicable.';

-- One dated decision on an application.
CREATE TABLE "credit_decision" (
  "credit_decision_id" VARCHAR NOT NULL,
  "loan_application_id" VARCHAR NOT NULL,
  "outcome" VARCHAR NOT NULL CHECK ("outcome" IN ('APPROVED', 'DECLINED', 'REFER')),
  "approved_principal" DECIMAL(18,2),
  "approved_term_months" INTEGER,
  "decided_at" TIMESTAMP NOT NULL,
  "expires_on" DATE NOT NULL,
  PRIMARY KEY ("credit_decision_id"),
  FOREIGN KEY ("loan_application_id") REFERENCES "loan_application" ("loan_application_id")
);
COMMENT ON TABLE "credit_decision" IS 'A recorded lending decision for an application. Grain: One dated decision on an application.';
COMMENT ON COLUMN "credit_decision"."credit_decision_id" IS 'Stable synthetic identifier for credit decision.';
COMMENT ON COLUMN "credit_decision"."loan_application_id" IS 'Application considered.';
COMMENT ON COLUMN "credit_decision"."outcome" IS 'Decision outcome.';
COMMENT ON COLUMN "credit_decision"."approved_principal" IS 'Approved principal; present only for APPROVED.';
COMMENT ON COLUMN "credit_decision"."approved_term_months" IS 'Approved term; present only for APPROVED.';
COMMENT ON COLUMN "credit_decision"."decided_at" IS 'UTC decision time.';
COMMENT ON COLUMN "credit_decision"."expires_on" IS 'Last valid acceptance date.';

-- One facility per credit-card account.
CREATE TABLE "credit_facility" (
  "credit_facility_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "approved_on" DATE NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  PRIMARY KEY ("credit_facility_id"),
  UNIQUE ("account_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id")
);
COMMENT ON TABLE "credit_facility" IS 'The credit agreement attached to a credit-card account. Grain: One facility per credit-card account.';
COMMENT ON COLUMN "credit_facility"."credit_facility_id" IS 'Stable synthetic identifier for credit facility.';
COMMENT ON COLUMN "credit_facility"."account_id" IS 'Credit-card account supported by this facility.';
COMMENT ON COLUMN "credit_facility"."approved_on" IS 'Date credit was approved.';
COMMENT ON COLUMN "credit_facility"."currency_id" IS 'Must match the linked account currency.';

-- One received payment instruction.
CREATE TABLE "payment" (
  "payment_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "channel_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "amount" DECIMAL(18,2) NOT NULL,
  "received_at" TIMESTAMP NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('PENDING', 'POSTED', 'FAILED')),
  PRIMARY KEY ("payment_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("channel_id") REFERENCES "channel" ("channel_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id")
);
COMMENT ON TABLE "payment" IS 'An external repayment to a credit-card account. Grain: One received payment instruction.';
COMMENT ON COLUMN "payment"."payment_id" IS 'Stable synthetic identifier for payment.';
COMMENT ON COLUMN "payment"."account_id" IS 'Credit-card account receiving the repayment.';
COMMENT ON COLUMN "payment"."channel_id" IS 'How the instruction arrived.';
COMMENT ON COLUMN "payment"."currency_id" IS 'Payment currency; must match the account.';
COMMENT ON COLUMN "payment"."amount" IS 'Positive repayment amount.';
COMMENT ON COLUMN "payment"."received_at" IS 'UTC receipt time.';
COMMENT ON COLUMN "payment"."status" IS 'Current processing outcome.';

-- One product application submitted by a customer.
CREATE TABLE "product_application" (
  "product_application_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "product_version_id" VARCHAR NOT NULL,
  "onboarding_case_id" VARCHAR NOT NULL,
  "submitted_at" TIMESTAMP NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('SUBMITTED', 'APPROVED', 'DECLINED', 'WITHDRAWN')),
  "booked_account_id" VARCHAR,
  PRIMARY KEY ("product_application_id"),
  UNIQUE ("booked_account_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id"),
  FOREIGN KEY ("product_version_id") REFERENCES "product_version" ("product_version_id"),
  FOREIGN KEY ("onboarding_case_id") REFERENCES "onboarding_case" ("onboarding_case_id"),
  FOREIGN KEY ("booked_account_id") REFERENCES "account" ("account_id")
);
COMMENT ON TABLE "product_application" IS 'A request to open a deposit or credit-card product. Grain: One product application submitted by a customer.';
COMMENT ON COLUMN "product_application"."product_application_id" IS 'Stable synthetic identifier for product application.';
COMMENT ON COLUMN "product_application"."customer_id" IS 'Applicant.';
COMMENT ON COLUMN "product_application"."product_version_id" IS 'Requested offering.';
COMMENT ON COLUMN "product_application"."onboarding_case_id" IS 'Onboarding case supporting the application.';
COMMENT ON COLUMN "product_application"."submitted_at" IS 'UTC submission time.';
COMMENT ON COLUMN "product_application"."status" IS 'Application outcome.';
COMMENT ON COLUMN "product_application"."booked_account_id" IS 'Account opened after approval, if booked.';

-- One standing-order arrangement.
CREATE TABLE "standing_order" (
  "standing_order_id" VARCHAR NOT NULL,
  "source_account_id" VARCHAR NOT NULL,
  "beneficiary_id" VARCHAR NOT NULL,
  "amount" DECIMAL(18,2) NOT NULL,
  "frequency" VARCHAR NOT NULL CHECK ("frequency" IN ('MONTHLY')),
  "starts_on" DATE NOT NULL,
  "ends_on" DATE,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('ACTIVE', 'CANCELLED')),
  PRIMARY KEY ("standing_order_id"),
  FOREIGN KEY ("source_account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("beneficiary_id") REFERENCES "beneficiary" ("beneficiary_id")
);
COMMENT ON TABLE "standing_order" IS 'A recurring instruction template for an external payment. Grain: One standing-order arrangement.';
COMMENT ON COLUMN "standing_order"."standing_order_id" IS 'Stable synthetic identifier for standing order.';
COMMENT ON COLUMN "standing_order"."source_account_id" IS 'Deposit account to debit.';
COMMENT ON COLUMN "standing_order"."beneficiary_id" IS 'Saved external destination.';
COMMENT ON COLUMN "standing_order"."amount" IS 'Positive amount per scheduled execution.';
COMMENT ON COLUMN "standing_order"."frequency" IS 'Supported recurrence.';
COMMENT ON COLUMN "standing_order"."starts_on" IS 'First eligible date.';
COMMENT ON COLUMN "standing_order"."ends_on" IS 'Last eligible date, inclusive.';
COMMENT ON COLUMN "standing_order"."status" IS 'Current instruction state.';

-- One issued statement for an account and cycle.
CREATE TABLE "statement" (
  "statement_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "period_start" DATE NOT NULL,
  "period_end_exclusive" DATE NOT NULL,
  "issued_on" DATE NOT NULL,
  "due_on" DATE NOT NULL,
  "opening_balance" DECIMAL(18,2) NOT NULL,
  "closing_balance" DECIMAL(18,2) NOT NULL,
  "minimum_due" DECIMAL(18,2) NOT NULL,
  PRIMARY KEY ("statement_id"),
  UNIQUE ("account_id", "period_start", "period_end_exclusive"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id")
);
COMMENT ON TABLE "statement" IS 'An issued monthly billing snapshot for a credit-card account. Grain: One issued statement for an account and cycle.';
COMMENT ON COLUMN "statement"."statement_id" IS 'Stable synthetic identifier for statement.';
COMMENT ON COLUMN "statement"."account_id" IS 'Credit-card account being billed.';
COMMENT ON COLUMN "statement"."period_start" IS 'First included posting date.';
COMMENT ON COLUMN "statement"."period_end_exclusive" IS 'First excluded posting date.';
COMMENT ON COLUMN "statement"."issued_on" IS 'Issue date.';
COMMENT ON COLUMN "statement"."due_on" IS 'Payment due date.';
COMMENT ON COLUMN "statement"."opening_balance" IS 'Signed amount owed at start; negative means customer credit.';
COMMENT ON COLUMN "statement"."closing_balance" IS 'Signed amount owed at end.';
COMMENT ON COLUMN "statement"."minimum_due" IS 'Nonnegative supplied amount; calculation is outside scope.';

-- One card-to-person assignment interval.
CREATE TABLE "card_assignment" (
  "card_assignment_id" VARCHAR NOT NULL,
  "card_id" VARCHAR NOT NULL,
  "customer_id" VARCHAR NOT NULL,
  "role" VARCHAR NOT NULL CHECK ("role" IN ('PRIMARY', 'SUPPLEMENTARY')),
  "valid_from" DATE NOT NULL,
  "valid_to" DATE,
  PRIMARY KEY ("card_assignment_id"),
  FOREIGN KEY ("card_id") REFERENCES "card" ("card_id"),
  FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id")
);
COMMENT ON TABLE "card_assignment" IS 'The person authorized to use a card. Grain: One card-to-person assignment interval.';
COMMENT ON COLUMN "card_assignment"."card_assignment_id" IS 'Stable synthetic identifier for card assignment.';
COMMENT ON COLUMN "card_assignment"."card_id" IS 'Card being assigned.';
COMMENT ON COLUMN "card_assignment"."customer_id" IS 'Person authorized to use it.';
COMMENT ON COLUMN "card_assignment"."role" IS 'Card-user role.';
COMMENT ON COLUMN "card_assignment"."valid_from" IS 'First valid day, inclusive.';
COMMENT ON COLUMN "card_assignment"."valid_to" IS 'First invalid day, exclusive.';

-- One authorization request.
CREATE TABLE "card_authorization" (
  "card_authorization_id" VARCHAR NOT NULL,
  "card_id" VARCHAR NOT NULL,
  "merchant_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "requested_amount" DECIMAL(18,2) NOT NULL,
  "requested_at" TIMESTAMP NOT NULL,
  "decision" VARCHAR NOT NULL CHECK ("decision" IN ('APPROVED', 'DECLINED')),
  "channel_id" VARCHAR NOT NULL,
  PRIMARY KEY ("card_authorization_id"),
  FOREIGN KEY ("card_id") REFERENCES "card" ("card_id"),
  FOREIGN KEY ("merchant_id") REFERENCES "merchant" ("merchant_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id"),
  FOREIGN KEY ("channel_id") REFERENCES "channel" ("channel_id")
);
COMMENT ON TABLE "card_authorization" IS 'A request to approve card spending before posting. Grain: One authorization request.';
COMMENT ON COLUMN "card_authorization"."card_authorization_id" IS 'Stable synthetic identifier for card authorization.';
COMMENT ON COLUMN "card_authorization"."card_id" IS 'Card presented for authorization.';
COMMENT ON COLUMN "card_authorization"."merchant_id" IS 'Merchant requesting authorization.';
COMMENT ON COLUMN "card_authorization"."currency_id" IS 'Requested currency.';
COMMENT ON COLUMN "card_authorization"."requested_amount" IS 'Positive requested amount.';
COMMENT ON COLUMN "card_authorization"."requested_at" IS 'UTC request time.';
COMMENT ON COLUMN "card_authorization"."decision" IS 'Authorization result.';
COMMENT ON COLUMN "card_authorization"."channel_id" IS 'Origin of the request.';

-- One card status event.
CREATE TABLE "card_status_event" (
  "card_status_event_id" VARCHAR NOT NULL,
  "card_id" VARCHAR NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('ISSUED', 'ACTIVE', 'BLOCKED', 'EXPIRED', 'CLOSED')),
  "effective_at" TIMESTAMP NOT NULL,
  PRIMARY KEY ("card_status_event_id"),
  FOREIGN KEY ("card_id") REFERENCES "card" ("card_id")
);
COMMENT ON TABLE "card_status_event" IS 'A change in a card lifecycle. Grain: One card status event.';
COMMENT ON COLUMN "card_status_event"."card_status_event_id" IS 'Stable synthetic identifier for card status event.';
COMMENT ON COLUMN "card_status_event"."card_id" IS 'Card whose status changed.';
COMMENT ON COLUMN "card_status_event"."status" IS 'New lifecycle status.';
COMMENT ON COLUMN "card_status_event"."effective_at" IS 'UTC effective time.';

-- One effective limit change per facility.
CREATE TABLE "credit_limit_event" (
  "credit_limit_event_id" VARCHAR NOT NULL,
  "credit_facility_id" VARCHAR NOT NULL,
  "effective_at" TIMESTAMP NOT NULL,
  "limit_amount" DECIMAL(18,2) NOT NULL,
  "reason" VARCHAR NOT NULL,
  PRIMARY KEY ("credit_limit_event_id"),
  FOREIGN KEY ("credit_facility_id") REFERENCES "credit_facility" ("credit_facility_id")
);
COMMENT ON TABLE "credit_limit_event" IS 'A change in the approved credit limit. Grain: One effective limit change per facility.';
COMMENT ON COLUMN "credit_limit_event"."credit_limit_event_id" IS 'Stable synthetic identifier for credit limit event.';
COMMENT ON COLUMN "credit_limit_event"."credit_facility_id" IS 'Facility whose limit changed.';
COMMENT ON COLUMN "credit_limit_event"."effective_at" IS 'UTC time from which the limit applies.';
COMMENT ON COLUMN "credit_limit_event"."limit_amount" IS 'Nonnegative approved limit in facility currency.';
COMMENT ON COLUMN "credit_limit_event"."reason" IS 'Reason for changing the limit.';

-- One loan contract and its loan account.
CREATE TABLE "loan_contract" (
  "loan_contract_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "credit_decision_id" VARCHAR NOT NULL,
  "principal_amount" DECIMAL(18,2) NOT NULL,
  "term_months" INTEGER NOT NULL,
  "accepted_on" DATE NOT NULL,
  "matures_on" DATE NOT NULL,
  PRIMARY KEY ("loan_contract_id"),
  UNIQUE ("account_id"),
  UNIQUE ("credit_decision_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("credit_decision_id") REFERENCES "credit_decision" ("credit_decision_id")
);
COMMENT ON TABLE "loan_contract" IS 'An accepted fixed-term loan agreement. Grain: One loan contract and its loan account.';
COMMENT ON COLUMN "loan_contract"."loan_contract_id" IS 'Stable synthetic identifier for loan contract.';
COMMENT ON COLUMN "loan_contract"."account_id" IS 'TERM_LOAN account representing the principal obligation.';
COMMENT ON COLUMN "loan_contract"."credit_decision_id" IS 'Approved decision accepted by the borrower.';
COMMENT ON COLUMN "loan_contract"."principal_amount" IS 'Contracted principal in account currency.';
COMMENT ON COLUMN "loan_contract"."term_months" IS 'Positive contractual term.';
COMMENT ON COLUMN "loan_contract"."accepted_on" IS 'Contract acceptance date.';
COMMENT ON COLUMN "loan_contract"."matures_on" IS 'Contractual maturity date.';

-- One customer-authorized internal or outbound payment instruction.
CREATE TABLE "payment_order" (
  "payment_order_id" VARCHAR NOT NULL,
  "source_account_id" VARCHAR NOT NULL,
  "destination_account_id" VARCHAR,
  "beneficiary_id" VARCHAR,
  "standing_order_id" VARCHAR,
  "channel_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "kind" VARCHAR NOT NULL CHECK ("kind" IN ('INTERNAL', 'OUTBOUND')),
  "amount" DECIMAL(18,2) NOT NULL,
  "requested_at" TIMESTAMP NOT NULL,
  "requested_execution_on" DATE NOT NULL,
  "idempotency_key" VARCHAR NOT NULL,
  PRIMARY KEY ("payment_order_id"),
  UNIQUE ("idempotency_key"),
  FOREIGN KEY ("source_account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("destination_account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("beneficiary_id") REFERENCES "beneficiary" ("beneficiary_id"),
  FOREIGN KEY ("standing_order_id") REFERENCES "standing_order" ("standing_order_id"),
  FOREIGN KEY ("channel_id") REFERENCES "channel" ("channel_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id")
);
COMMENT ON TABLE "payment_order" IS 'An instruction to move funds from a deposit account. Grain: One customer-authorized internal or outbound payment instruction.';
COMMENT ON COLUMN "payment_order"."payment_order_id" IS 'Stable synthetic identifier for payment order.';
COMMENT ON COLUMN "payment_order"."source_account_id" IS 'Deposit account funding the instruction.';
COMMENT ON COLUMN "payment_order"."destination_account_id" IS 'Internal deposit destination; absent for external instructions.';
COMMENT ON COLUMN "payment_order"."beneficiary_id" IS 'External payee; absent for internal instructions.';
COMMENT ON COLUMN "payment_order"."standing_order_id" IS 'Recurring template that produced the order, if any.';
COMMENT ON COLUMN "payment_order"."channel_id" IS 'Channel accepting the instruction.';
COMMENT ON COLUMN "payment_order"."currency_id" IS 'Instruction currency.';
COMMENT ON COLUMN "payment_order"."kind" IS 'Supported instruction type.';
COMMENT ON COLUMN "payment_order"."amount" IS 'Positive instructed amount.';
COMMENT ON COLUMN "payment_order"."requested_at" IS 'UTC acceptance time.';
COMMENT ON COLUMN "payment_order"."requested_execution_on" IS 'Requested business execution date.';
COMMENT ON COLUMN "payment_order"."idempotency_key" IS 'Unique client-request key in this single-bank scenario.';

-- One reservation associated with a payment order.
CREATE TABLE "account_hold" (
  "account_hold_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "payment_order_id" VARCHAR NOT NULL,
  "amount" DECIMAL(18,2) NOT NULL,
  "placed_at" TIMESTAMP NOT NULL,
  "released_at" TIMESTAMP,
  "expires_at" TIMESTAMP NOT NULL,
  PRIMARY KEY ("account_hold_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("payment_order_id") REFERENCES "payment_order" ("payment_order_id")
);
COMMENT ON TABLE "account_hold" IS 'A temporary reservation of funds on a deposit account. Grain: One reservation associated with a payment order.';
COMMENT ON COLUMN "account_hold"."account_hold_id" IS 'Stable synthetic identifier for account hold.';
COMMENT ON COLUMN "account_hold"."account_id" IS 'Deposit account with reserved funds.';
COMMENT ON COLUMN "account_hold"."payment_order_id" IS 'Order causing the reservation.';
COMMENT ON COLUMN "account_hold"."amount" IS 'Positive reserved amount.';
COMMENT ON COLUMN "account_hold"."placed_at" IS 'UTC reservation time.';
COMMENT ON COLUMN "account_hold"."released_at" IS 'UTC release time; null means still held.';
COMMENT ON COLUMN "account_hold"."expires_at" IS 'UTC expiry time.';

-- One posted card purchase or refund.
CREATE TABLE "card_transaction" (
  "card_transaction_id" VARCHAR NOT NULL,
  "card_id" VARCHAR NOT NULL,
  "merchant_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "authorization_id" VARCHAR,
  "original_transaction_id" VARCHAR,
  "kind" VARCHAR NOT NULL CHECK ("kind" IN ('PURCHASE', 'REFUND')),
  "amount" DECIMAL(18,2) NOT NULL,
  "occurred_at" TIMESTAMP NOT NULL,
  "posted_on" DATE NOT NULL,
  PRIMARY KEY ("card_transaction_id"),
  FOREIGN KEY ("card_id") REFERENCES "card" ("card_id"),
  FOREIGN KEY ("merchant_id") REFERENCES "merchant" ("merchant_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id"),
  FOREIGN KEY ("authorization_id") REFERENCES "card_authorization" ("card_authorization_id")
);
COMMENT ON TABLE "card_transaction" IS 'A posted purchase or refund received through the card network. Grain: One posted card purchase or refund.';
COMMENT ON COLUMN "card_transaction"."card_transaction_id" IS 'Stable synthetic identifier for card transaction.';
COMMENT ON COLUMN "card_transaction"."card_id" IS 'Card used for this activity.';
COMMENT ON COLUMN "card_transaction"."merchant_id" IS 'Merchant involved.';
COMMENT ON COLUMN "card_transaction"."currency_id" IS 'Posted currency.';
COMMENT ON COLUMN "card_transaction"."authorization_id" IS 'Related authorization when available; may be absent for offline clearing.';
COMMENT ON COLUMN "card_transaction"."original_transaction_id" IS 'Purchase refunded by this refund.';
COMMENT ON COLUMN "card_transaction"."kind" IS 'Type of posted card activity.';
COMMENT ON COLUMN "card_transaction"."amount" IS 'Positive amount; kind determines economic direction.';
COMMENT ON COLUMN "card_transaction"."occurred_at" IS 'UTC time of merchant activity.';
COMMENT ON COLUMN "card_transaction"."posted_on" IS 'Business date on which activity was posted.';

-- One completed principal disbursement.
CREATE TABLE "loan_disbursement" (
  "loan_disbursement_id" VARCHAR NOT NULL,
  "loan_contract_id" VARCHAR NOT NULL,
  "destination_account_id" VARCHAR NOT NULL,
  "amount" DECIMAL(18,2) NOT NULL,
  "disbursed_on" DATE NOT NULL,
  PRIMARY KEY ("loan_disbursement_id"),
  UNIQUE ("loan_contract_id"),
  FOREIGN KEY ("loan_contract_id") REFERENCES "loan_contract" ("loan_contract_id"),
  FOREIGN KEY ("destination_account_id") REFERENCES "account" ("account_id")
);
COMMENT ON TABLE "loan_disbursement" IS 'A funded principal draw on a loan contract. Grain: One completed principal disbursement.';
COMMENT ON COLUMN "loan_disbursement"."loan_disbursement_id" IS 'Stable synthetic identifier for loan disbursement.';
COMMENT ON COLUMN "loan_disbursement"."loan_contract_id" IS 'Contract providing the funds.';
COMMENT ON COLUMN "loan_disbursement"."destination_account_id" IS 'Internal deposit account receiving proceeds.';
COMMENT ON COLUMN "loan_disbursement"."amount" IS 'Positive principal disbursed.';
COMMENT ON COLUMN "loan_disbursement"."disbursed_on" IS 'Funding business date.';

-- One received repayment with supplied principal/interest split.
CREATE TABLE "loan_repayment" (
  "loan_repayment_id" VARCHAR NOT NULL,
  "loan_contract_id" VARCHAR NOT NULL,
  "principal_amount" DECIMAL(18,2) NOT NULL,
  "interest_amount" DECIMAL(18,2) NOT NULL,
  "received_on" DATE NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('PENDING', 'POSTED', 'FAILED')),
  PRIMARY KEY ("loan_repayment_id"),
  FOREIGN KEY ("loan_contract_id") REFERENCES "loan_contract" ("loan_contract_id")
);
COMMENT ON TABLE "loan_repayment" IS 'A received external repayment against a loan. Grain: One received repayment with supplied principal/interest split.';
COMMENT ON COLUMN "loan_repayment"."loan_repayment_id" IS 'Stable synthetic identifier for loan repayment.';
COMMENT ON COLUMN "loan_repayment"."loan_contract_id" IS 'Loan being repaid.';
COMMENT ON COLUMN "loan_repayment"."principal_amount" IS 'Nonnegative principal portion.';
COMMENT ON COLUMN "loan_repayment"."interest_amount" IS 'Nonnegative interest portion.';
COMMENT ON COLUMN "loan_repayment"."received_on" IS 'Receipt business date.';
COMMENT ON COLUMN "loan_repayment"."status" IS 'Current processing state.';

-- One installment for a loan contract.
CREATE TABLE "loan_schedule_item" (
  "loan_schedule_item_id" VARCHAR NOT NULL,
  "loan_contract_id" VARCHAR NOT NULL,
  "installment_number" INTEGER NOT NULL,
  "due_on" DATE NOT NULL,
  "principal_due" DECIMAL(18,2) NOT NULL,
  "interest_due" DECIMAL(18,2) NOT NULL,
  PRIMARY KEY ("loan_schedule_item_id"),
  UNIQUE ("loan_contract_id", "installment_number"),
  FOREIGN KEY ("loan_contract_id") REFERENCES "loan_contract" ("loan_contract_id")
);
COMMENT ON TABLE "loan_schedule_item" IS 'An expected installment in a supplied repayment schedule. Grain: One installment for a loan contract.';
COMMENT ON COLUMN "loan_schedule_item"."loan_schedule_item_id" IS 'Stable synthetic identifier for loan schedule item.';
COMMENT ON COLUMN "loan_schedule_item"."loan_contract_id" IS 'Contract being scheduled.';
COMMENT ON COLUMN "loan_schedule_item"."installment_number" IS 'Positive sequence within the loan.';
COMMENT ON COLUMN "loan_schedule_item"."due_on" IS 'Due date.';
COMMENT ON COLUMN "loan_schedule_item"."principal_due" IS 'Nonnegative scheduled principal.';
COMMENT ON COLUMN "loan_schedule_item"."interest_due" IS 'Nonnegative supplied interest amount.';

-- One execution event for an order.
CREATE TABLE "payment_event" (
  "payment_event_id" VARCHAR NOT NULL,
  "payment_order_id" VARCHAR NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('RECEIVED', 'VALIDATED', 'POSTED', 'SETTLED', 'FAILED', 'CANCELLED')),
  "occurred_at" TIMESTAMP NOT NULL,
  "reason_code" VARCHAR NOT NULL,
  PRIMARY KEY ("payment_event_id"),
  UNIQUE ("payment_order_id", "occurred_at"),
  FOREIGN KEY ("payment_order_id") REFERENCES "payment_order" ("payment_order_id")
);
COMMENT ON TABLE "payment_event" IS 'A lifecycle event for a deposit payment instruction. Grain: One execution event for an order.';
COMMENT ON COLUMN "payment_event"."payment_event_id" IS 'Stable synthetic identifier for payment event.';
COMMENT ON COLUMN "payment_event"."payment_order_id" IS 'Instruction being progressed.';
COMMENT ON COLUMN "payment_event"."status" IS 'New execution state.';
COMMENT ON COLUMN "payment_event"."occurred_at" IS 'UTC event time.';
COMMENT ON COLUMN "payment_event"."reason_code" IS 'Project-local processing reason.';

-- One settlement observation for an outbound order.
CREATE TABLE "payment_settlement" (
  "payment_settlement_id" VARCHAR NOT NULL,
  "payment_order_id" VARCHAR NOT NULL,
  "currency_id" VARCHAR NOT NULL,
  "settled_amount" DECIMAL(18,2) NOT NULL,
  "settled_on" DATE NOT NULL,
  "external_reference" VARCHAR NOT NULL,
  PRIMARY KEY ("payment_settlement_id"),
  UNIQUE ("payment_order_id"),
  FOREIGN KEY ("payment_order_id") REFERENCES "payment_order" ("payment_order_id"),
  FOREIGN KEY ("currency_id") REFERENCES "currency" ("currency_id")
);
COMMENT ON TABLE "payment_settlement" IS 'An observed external settlement result. Grain: One settlement observation for an outbound order.';
COMMENT ON COLUMN "payment_settlement"."payment_settlement_id" IS 'Stable synthetic identifier for payment settlement.';
COMMENT ON COLUMN "payment_settlement"."payment_order_id" IS 'Outbound order being settled.';
COMMENT ON COLUMN "payment_settlement"."currency_id" IS 'Settlement currency.';
COMMENT ON COLUMN "payment_settlement"."settled_amount" IS 'Positive settled amount.';
COMMENT ON COLUMN "payment_settlement"."settled_on" IS 'Settlement business date.';
COMMENT ON COLUMN "payment_settlement"."external_reference" IS 'Synthetic clearing reference.';

-- One booked debit or credit on an account.
CREATE TABLE "account_entry" (
  "account_entry_id" VARCHAR NOT NULL,
  "account_id" VARCHAR NOT NULL,
  "card_transaction_id" VARCHAR,
  "payment_id" VARCHAR,
  "fee_type_id" VARCHAR,
  "reverses_entry_id" VARCHAR,
  "kind" VARCHAR NOT NULL CHECK ("kind" IN ('CARD', 'PAYMENT', 'FEE', 'ADJUSTMENT', 'REVERSAL', 'DEPOSIT_PAYMENT', 'LOAN_DRAW', 'LOAN_REPAYMENT')),
  "direction" VARCHAR NOT NULL CHECK ("direction" IN ('DEBIT', 'CREDIT')),
  "amount" DECIMAL(18,2) NOT NULL,
  "posted_on" DATE NOT NULL,
  "description" VARCHAR NOT NULL,
  "payment_order_id" VARCHAR,
  "loan_disbursement_id" VARCHAR,
  "loan_repayment_id" VARCHAR,
  PRIMARY KEY ("account_entry_id"),
  FOREIGN KEY ("account_id") REFERENCES "account" ("account_id"),
  FOREIGN KEY ("card_transaction_id") REFERENCES "card_transaction" ("card_transaction_id"),
  FOREIGN KEY ("payment_id") REFERENCES "payment" ("payment_id"),
  FOREIGN KEY ("fee_type_id") REFERENCES "fee_type" ("fee_type_id"),
  FOREIGN KEY ("payment_order_id") REFERENCES "payment_order" ("payment_order_id"),
  FOREIGN KEY ("loan_disbursement_id") REFERENCES "loan_disbursement" ("loan_disbursement_id"),
  FOREIGN KEY ("loan_repayment_id") REFERENCES "loan_repayment" ("loan_repayment_id")
);
COMMENT ON TABLE "account_entry" IS 'An immutable customer-account movement used for statement presentation. Grain: One booked debit or credit on an account.';
COMMENT ON COLUMN "account_entry"."account_entry_id" IS 'Stable synthetic identifier for account entry.';
COMMENT ON COLUMN "account_entry"."account_id" IS 'Account affected.';
COMMENT ON COLUMN "account_entry"."card_transaction_id" IS 'Card activity behind this entry, if any.';
COMMENT ON COLUMN "account_entry"."payment_id" IS 'Repayment behind this entry, if any.';
COMMENT ON COLUMN "account_entry"."fee_type_id" IS 'Fee category when this is a fee.';
COMMENT ON COLUMN "account_entry"."reverses_entry_id" IS 'Earlier entry reversed by this entry.';
COMMENT ON COLUMN "account_entry"."kind" IS 'Business source of the entry.';
COMMENT ON COLUMN "account_entry"."direction" IS 'Customer-account debit or credit.';
COMMENT ON COLUMN "account_entry"."amount" IS 'Positive amount in account currency.';
COMMENT ON COLUMN "account_entry"."posted_on" IS 'Booking business date.';
COMMENT ON COLUMN "account_entry"."description" IS 'Short statement narrative.';
COMMENT ON COLUMN "account_entry"."payment_order_id" IS 'Deposit payment instruction behind this entry, if any.';
COMMENT ON COLUMN "account_entry"."loan_disbursement_id" IS 'Loan draw behind this principal or deposit entry, if any.';
COMMENT ON COLUMN "account_entry"."loan_repayment_id" IS 'Loan repayment behind a principal reduction, if any.';

-- One dispute case against one purchase.
CREATE TABLE "dispute" (
  "dispute_id" VARCHAR NOT NULL,
  "card_transaction_id" VARCHAR NOT NULL,
  "raised_by_customer_id" VARCHAR NOT NULL,
  "dispute_reason_id" VARCHAR NOT NULL,
  "claimed_amount" DECIMAL(18,2) NOT NULL,
  "opened_at" TIMESTAMP NOT NULL,
  PRIMARY KEY ("dispute_id"),
  FOREIGN KEY ("card_transaction_id") REFERENCES "card_transaction" ("card_transaction_id"),
  FOREIGN KEY ("raised_by_customer_id") REFERENCES "customer" ("customer_id"),
  FOREIGN KEY ("dispute_reason_id") REFERENCES "dispute_reason" ("dispute_reason_id")
);
COMMENT ON TABLE "dispute" IS 'A customer claim about a posted purchase. Grain: One dispute case against one purchase.';
COMMENT ON COLUMN "dispute"."dispute_id" IS 'Stable synthetic identifier for dispute.';
COMMENT ON COLUMN "dispute"."card_transaction_id" IS 'Purchase being challenged.';
COMMENT ON COLUMN "dispute"."raised_by_customer_id" IS 'Customer raising the case.';
COMMENT ON COLUMN "dispute"."dispute_reason_id" IS 'Reason for the claim.';
COMMENT ON COLUMN "dispute"."claimed_amount" IS 'Positive challenged portion of the purchase.';
COMMENT ON COLUMN "dispute"."opened_at" IS 'UTC time the case was opened.';

-- One event in a dispute.
CREATE TABLE "dispute_event" (
  "dispute_event_id" VARCHAR NOT NULL,
  "dispute_id" VARCHAR NOT NULL,
  "status" VARCHAR NOT NULL CHECK ("status" IN ('OPEN', 'UNDER_REVIEW', 'RESOLVED_CUSTOMER', 'RESOLVED_MERCHANT', 'CLOSED')),
  "occurred_at" TIMESTAMP NOT NULL,
  "summary" VARCHAR NOT NULL,
  PRIMARY KEY ("dispute_event_id"),
  FOREIGN KEY ("dispute_id") REFERENCES "dispute" ("dispute_id")
);
COMMENT ON TABLE "dispute_event" IS 'A lifecycle event within a dispute case. Grain: One event in a dispute.';
COMMENT ON COLUMN "dispute_event"."dispute_event_id" IS 'Stable synthetic identifier for dispute event.';
COMMENT ON COLUMN "dispute_event"."dispute_id" IS 'Case being progressed.';
COMMENT ON COLUMN "dispute_event"."status" IS 'New case status.';
COMMENT ON COLUMN "dispute_event"."occurred_at" IS 'UTC event time.';
COMMENT ON COLUMN "dispute_event"."summary" IS 'Synthetic operational note; no personal narrative.';

-- One allocation of an account entry to a journal line.
CREATE TABLE "posting_link" (
  "posting_link_id" VARCHAR NOT NULL,
  "account_entry_id" VARCHAR NOT NULL,
  "journal_line_id" VARCHAR NOT NULL,
  "allocated_amount" DECIMAL(18,2) NOT NULL,
  PRIMARY KEY ("posting_link_id"),
  UNIQUE ("account_entry_id", "journal_line_id"),
  FOREIGN KEY ("account_entry_id") REFERENCES "account_entry" ("account_entry_id"),
  FOREIGN KEY ("journal_line_id") REFERENCES "journal_line" ("journal_line_id")
);
COMMENT ON TABLE "posting_link" IS 'A reconciliation mapping from customer-account activity to a ledger line. Grain: One allocation of an account entry to a journal line.';
COMMENT ON COLUMN "posting_link"."posting_link_id" IS 'Stable synthetic identifier for posting link.';
COMMENT ON COLUMN "posting_link"."account_entry_id" IS 'Customer-account entry being mapped.';
COMMENT ON COLUMN "posting_link"."journal_line_id" IS 'Related ledger line.';
COMMENT ON COLUMN "posting_link"."allocated_amount" IS 'Positive mapped portion of the account entry.';

-- One comparison outcome within one run.
CREATE TABLE "reconciliation_item" (
  "reconciliation_item_id" VARCHAR NOT NULL,
  "reconciliation_run_id" VARCHAR NOT NULL,
  "account_entry_id" VARCHAR,
  "journal_line_id" VARCHAR,
  "payment_order_id" VARCHAR,
  "statement_id" VARCHAR,
  "outcome" VARCHAR NOT NULL CHECK ("outcome" IN ('MATCHED', 'UNMATCHED', 'AMOUNT_MISMATCH')),
  "difference_amount" DECIMAL(18,2) NOT NULL,
  "explanation" VARCHAR NOT NULL,
  PRIMARY KEY ("reconciliation_item_id"),
  FOREIGN KEY ("reconciliation_run_id") REFERENCES "reconciliation_run" ("reconciliation_run_id"),
  FOREIGN KEY ("account_entry_id") REFERENCES "account_entry" ("account_entry_id"),
  FOREIGN KEY ("journal_line_id") REFERENCES "journal_line" ("journal_line_id"),
  FOREIGN KEY ("payment_order_id") REFERENCES "payment_order" ("payment_order_id"),
  FOREIGN KEY ("statement_id") REFERENCES "statement" ("statement_id")
);
COMMENT ON TABLE "reconciliation_item" IS 'A match or exception recorded by a reconciliation run. Grain: One comparison outcome within one run.';
COMMENT ON COLUMN "reconciliation_item"."reconciliation_item_id" IS 'Stable synthetic identifier for reconciliation item.';
COMMENT ON COLUMN "reconciliation_item"."reconciliation_run_id" IS 'Run that produced the outcome.';
COMMENT ON COLUMN "reconciliation_item"."account_entry_id" IS 'Entry involved when comparing account and ledger records.';
COMMENT ON COLUMN "reconciliation_item"."journal_line_id" IS 'Ledger line involved when available.';
COMMENT ON COLUMN "reconciliation_item"."payment_order_id" IS 'Order involved when comparing payments and settlement.';
COMMENT ON COLUMN "reconciliation_item"."statement_id" IS 'Statement involved when comparing billing totals.';
COMMENT ON COLUMN "reconciliation_item"."outcome" IS 'Comparison result.';
COMMENT ON COLUMN "reconciliation_item"."difference_amount" IS 'Signed left-side minus right-side difference in CAD.';
COMMENT ON COLUMN "reconciliation_item"."explanation" IS 'Synthetic explanation of the match or exception.';

-- One account entry displayed on one statement.
CREATE TABLE "statement_line" (
  "statement_line_id" VARCHAR NOT NULL,
  "statement_id" VARCHAR NOT NULL,
  "account_entry_id" VARCHAR NOT NULL,
  "line_number" INTEGER NOT NULL,
  "narrative" VARCHAR NOT NULL,
  PRIMARY KEY ("statement_line_id"),
  UNIQUE ("statement_id", "line_number"),
  UNIQUE ("account_entry_id"),
  FOREIGN KEY ("statement_id") REFERENCES "statement" ("statement_id"),
  FOREIGN KEY ("account_entry_id") REFERENCES "account_entry" ("account_entry_id")
);
COMMENT ON TABLE "statement_line" IS 'A printed item on an issued statement. Grain: One account entry displayed on one statement.';
COMMENT ON COLUMN "statement_line"."statement_line_id" IS 'Stable synthetic identifier for statement line.';
COMMENT ON COLUMN "statement_line"."statement_id" IS 'Statement containing this line.';
COMMENT ON COLUMN "statement_line"."account_entry_id" IS 'Booked entry being displayed.';
COMMENT ON COLUMN "statement_line"."line_number" IS 'Positive order within the statement.';
COMMENT ON COLUMN "statement_line"."narrative" IS 'Narrative captured at issue time.';
