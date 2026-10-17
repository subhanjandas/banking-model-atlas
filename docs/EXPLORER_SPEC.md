# Explorer specification

Status: implemented in application 1.0.0. This is the original interaction contract; observed test results are recorded in VALIDATION.md.

## Main task

Help a visitor understand a banking entity, inspect its attributes, and follow a meaningful connection without reading the whole model first. Start with the full banking model, not an industry picker containing one choice.

## Screen structure

- Header: Banking Model Atlas, model version, journey picker, view mode, downloads.
- Left panel: domain list, entity counts, search results and visibility controls.
- Graph canvas: domain colours, labeled entity nodes, relationship edges, pan/zoom and reset controls.
- Right inspector: selected entity or relationship, with plain-language definitions and technical details.

Desktop uses all three panels. On narrow screens, navigation and details become accessible drawers. The table list remains a usable alternative to the graph. Controls need visible keyboard focus, meaningful labels and sufficient contrast; colour alone must not encode a relationship type.

## Interaction contract

| Action | Expected result |
|---|---|
| Select entity | Highlight it, update inspector and URL selection. |
| Select relationship | Show both endpoint columns, nullability, cardinality and business description. |
| Search entity or column | Display matching entity and, when relevant, column; selecting reveals and centres it. |
| Filter domain | Show its entities; clearly indicate omitted external relationships. |
| Focus neighbours | Include the selected table and its immediate linked tables, even across domains. |
| Choose journey | Highlight exactly the journey's entities and selected edges; display explanatory steps. |
| Reset view | Clear search, filters, focus and journey; fit the full graph. |
| Switch overview/detail | Preserve selection where possible; overview groups domains, detail shows entities. |
| Load shared URL | Restore domain/entity/journey where valid; unknown IDs show a friendly fallback. |
| Download JSON | Return the exact version of metadata shown in the viewer. |
| Download dictionary | Return definitions generated from that same metadata. |
| Download SQL | Download the generated, tested DuckDB schema. |

Search must reveal a hidden match rather than silently selecting an invisible node. Selecting a new journey clears conflicting domain filters. Node dragging affects presentation only, not the underlying banking model. Self-references must be visible and selectable without obscuring table names.

## Technical direction

React + TypeScript + Vite for the application, Cytoscape.js for graph interaction. Use stable entity and relationship IDs. Keep model parsing, graph adaptation, view state, inspector rendering and export logic separate. Package dependencies only when implementation begins; Hour 1 does not invent tested package versions.

The first layout should be deterministic and grouped by domain. Avoid constantly running a force layout while the visitor is reading. Fit and centre actions must account for open side panels. Rendering every field inside every node is not a requirement; full definitions belong in the inspector.

## Definition of done for the first interactive release

1. All 80 entities and 128 relationships derive from the JSON, with no duplicate hard-coded model.
2. Search, domain filtering, neighbour focus and reset work together.
3. Both journey presets select connected, meaningful subgraphs.
4. Every entity and edge has a readable inspector; self-references work.
5. Zoom and pan remain usable without text overlap at the default view.
6. Deep links survive a refresh on the deployment's repository subpath.
7. JSON and dictionary downloads match the displayed version.
8. Keyboard navigation supports search, lists, drawers and controls.
9. Automated model tests pass and browser interaction checks are recorded.
10. README links to an actually deployed demonstration, not an assumed URL.

SQL export and synthetic data are separate acceptance items. They must not be marked complete because the graph looks finished.
