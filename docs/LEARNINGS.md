# What this project teaches

1. **Start with a question and a grain.** “One complaint resolution” is a different record from “one customer request.” A table name alone does not explain its meaning.
2. **Preserve distinctions that matter.** A signal is not a verdict, a promise is not a payment, a payment instruction is not settlement, and a snapshot is not a movement.
3. **Separate structure from behavior.** A schema can be structurally valid while its transactions violate business rules. Both layers need tests.
4. **Keep corrections visible.** Opposite entries preserve the original movement. Updating history would make the audit trail and old statements harder to explain.
5. **Use independent expectations.** Recalculating a closing balance and then checking it against the same calculation proves little. Supplied snapshots create a separate expectation.
6. **Balanced does not mean correct.** Two compensating errors can leave a trial balance at zero. Check individual ledger accounts and customer accounts too.
7. **Control join multiplication.** Aggregate entries and allocations at their own grain before combining them with other one-to-many relationships.
8. **Version semantics separately from the UI.** Application 1.0.0 is a portfolio release; model 0.4.0 identifies its business metadata. A new theme does not change accounting meaning.
9. **Make coverage visible.** A large diagram is not evidence that every lifecycle works. Each table states whether example records are available.
10. **Treat visual design as part of usability.** Domain filters, readable panels, keyboard-accessible lists, persistent themes and focused journeys make the model usable without understanding its code first.

A concrete correction during development: an early narrative described a loan repayment as coming from a deposit account, while the journal used external cash. The documentation was corrected to match the executable scenario. Reconciliation exposes why this distinction matters.
