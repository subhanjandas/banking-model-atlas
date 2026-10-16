# Model contract, version 1.0.0

The explorer will read `model/banking.model.json`. This document and `scripts/validate_model.py` define the current contract. There is no external JSON Schema dependency in this checkpoint. The validator covers the supported contract; it is not an arbitrary untrusted-JSON sanitizer.

## Root structure

| Property | Meaning |
|---|---|
| schema_version | Metadata format version. Breaking structural changes require a new major version. |
| model_version | Banking content release, independent of the metadata format. |
| id, title, description | Stable model identifier and human-readable context. |
| status | `foundation_draft` until the next reviewed checkpoint. |
| scenario | Name and scope of the fictional institution. |
| business_timezone | America/Toronto; timestamps remain UTC instants. |
| supported_currencies | CAD only in this release. |
| domains | ID, label, description, and display colour. |
| entities | Definitions, grains, columns, keys, notes, and rule references. |
| relationships | Explicit column-level foreign-key relationships. |
| rules | Business specifications with honest implementation status. |
| journeys | Connected graph selections with explanatory steps. |

## Entity and column fields

Each entity has a stable snake_case `id`, a `label`, a valid `domain`, a `description`, a `grain`, `columns`, `primary_key`, `unique_keys`, `notes`, and `rule_ids`. Version 1 supports single-column primary keys and foreign keys. Composite unique keys are supported as metadata.

Each column has an entity-local ID, logical type, boolean nullability, description, and classification. Optional `allowed_values` contains a nonempty list of strings. Types are `string`, `integer`, `boolean`, `date`, `timestamp`, and `decimal(18,2)`. The DuckDB exporter maps these logical types to executable DDL.

Classifications are `identifier`, `personal`, `financial`, and `internal`. A synthetic identifier could link to a person in a real system and should not be treated as anonymous merely because it is not a name. Classification is explanatory; no policy enforcement is implied.

## Relationship direction

`source_entity.source_column` is the referencing side; `target_entity.target_column` is the unique referenced side. `source_to_target` is `exactly_one` for a non-null foreign key or `zero_or_one` for a nullable one. `target_to_source` is `zero_or_many`, unless a single-column unique constraint on the source limits it to `zero_or_one`.

This notation describes the schema's structural maximum. For example, a credit-card account must have a facility by business rule, but the account table includes deposit accounts too. The reverse relationship is structurally zero-or-one, with the conditional minimum specified in R04.

Relationship IDs must remain stable when labels change. The UI must never use a display label as the identity of a node or edge. Self-references are valid for card replacements, refunds, and entry reversals; cycle restrictions are data rules.

## Journeys

A journey contains a stable ID, title, question, ordered explanatory steps, selected relationship IDs, and a caveat. The selected edges must remain inside the selected entity set and connect it as an undirected graph. Steps tell a story; they are not guaranteed to be a linear directed join chain.

The viewer should highlight exactly those edges, not every edge between all selected nodes. Other relationships may be available through a separate neighbourhood action.

## Rules and enforcement

Rules have IDs, entity references, a category, a statement, an enforcement plan, and implementation status. All rules currently use `specified_not_implemented`. Metadata validation confirms their links. A separate validation_checks.json file records selected executable checks, linked rule IDs and coverage limits; full rule enforcement is still incomplete.

The `enforcement` text on relationships is descriptive. It does not create database constraints. SQL exporters must declare what they can enforce, what remains informational, and which rules require row, cross-row, temporal, or aggregate checks.

## Editing safely

1. Change the JSON model, including all affected journey and rule references.
2. Run `python3 scripts/validate_model.py`.
3. Run `python3 scripts/render_docs.py`.
4. Run the tests and generated-document check.
5. Record semantic changes in the changelog and design decisions.

Renaming a stable ID is a breaking change for future bookmarked URLs. Changing a label is not. UI-only display preferences should remain separate from the banking semantics.
