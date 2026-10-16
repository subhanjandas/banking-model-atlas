# Roadmap and checkpoint status

## Hour 1 — foundation

Completed locally: fictional scenario, 30-entity model, 161 column definitions, 45 relationships, 21 rule specifications, two connected journey definitions, metadata validator, 18 tests, generated reference documents, explorer specification and CI configuration.

Pending external action: creation of the new GitHub repository and upload of this checkpoint. No hosted explorer exists yet.

## Next — complete one vertical slice of the viewer

Implement the application shell, load the model, render a small connected subset, select a table and an edge, and inspect their metadata. Use customer, card_assignment, card, card_transaction, dispute and dispute_event as an initial slice. This validates the interface before expanding the canvas.

Then render all domains, add search, domain visibility, neighbour focus, the two journeys and URL state. Add downloads and accessible responsive panels. Test the actual deployed repository subpath.

## Following — evidence and export

Build one tested SQL dialect exporter. Generate synthetic data only after the business rules have executable tests. Turn the worked scenario into a reconciliation fixture. Add bad-data fixtures for refunds, ownership intervals, replacements and statement membership.

## Longer term

Statement reissues, fuller lifecycle transition rules, product migrations, provisional credits and a broader deposit-activity model. AI-assisted drafting is optional and must not replace deterministic structural checks or domain review.

## Scope rule

The one-day target is a polished educational explorer. Increasing entity count further should require a new business question, not a desire to make the graph larger. Public claims must distinguish specified, locally tested, and actually deployed features.
