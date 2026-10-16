# Validation record

Date: 2026-10-16. Checkpoint: 0.1.0.

## Passed locally

- Metadata integrity: eight domains, 30 entities, 161 columns, 45 relationships.
- All entity, column, rule and journey references resolved.
- Foreign-key type and declared cardinality consistency checks passed.
- Both selected journey subgraphs were connected.
- Eighteen unittest cases passed, including deliberate duplicate IDs, missing references, invalid key types, incorrect cardinalities, a disconnected journey, and an unjustified business-rule enforcement claim.
- Five generated reference documents matched fresh generation byte for byte.
- Relative Markdown file links were checked for existing targets.

## Not tested or claimed

- No actual banking records were generated or validated.
- No SQL dialect was executed.
- No interactive UI was implemented or browser-tested.
- GitHub Actions is configured but has not run remotely.
- No repository or website was published from this environment.
- Business semantics remain an educational design draft, not an independently reviewed production model.

## Replay

Run `python3 replay.py` from the extracted project directory. Run `python3 verify_package.py` to verify the release manifest before editing. The manifest covers the release files other than itself; edits naturally change checksums.
