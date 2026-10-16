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

