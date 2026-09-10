# Release Package Shape

**Status:** Planned. Will be drafted as the detailed reference for `CR-DEA-RP-01` §4.

## Outline

Canonical asset list and naming convention for every release package:

1. Human-readable assets
 - ECF-backdrop map (HTML)
 - ECF-backdrop poster (A0 PNG, 300 DPI)
 - ECF-backdrop print (A3 PNG, 300 DPI)
 - Catalog flat-view (Excel)
 - Pamphlet booklet (PDF, A5)
 - Release guide (PDF, A5, 4-8 pages)
 - Release notes (Markdown)

2. Machine-consumable plugins
 - Engine-plugin file per consuming engine (BPMN, ArchiMate, etc.)

3. Federation metadata
 - Release manifest (in the federation registry)

Naming convention: `<catalog>-<asset-type>.<ext>` (e.g. `processes-map-a0.png`, `processes.bpmn`, `processes-catalog.xlsx`).

## Reference

- `CR-DEA-RP-01` §4
- `registry-schema.md` (sister standard for the manifest shape)