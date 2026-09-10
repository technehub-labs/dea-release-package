# Release Package Program : Planning Folder (historical)

This folder holds the **historical planning record** for the Release Package Program. The canonical artifacts now live in their proper homes in the repo:

- ADRs: [`../docs/adr/`](../docs/adr/)
- CRs: [`../change-requests/`](../change-requests/)
- README: [`../README.md`](../README.md)
- GOVERNANCE: [`../GOVERNANCE.md`](../GOVERNANCE.md)

This folder is preserved so reviewers can see the planning trajectory (drafts, superseded revisions, open questions). It is **not** the source of truth for any decision; it is a paper trail.

## What was drafted here

1. **`ADR-DEA-RP-01-program-architecture.md`** : design specification; migrated to `docs/adr/`.
2. **`CR-DEA-RP-01-release-package-program.md`** : umbrella CR; migrated to `change-requests/`.
3. **`CR-DEA-RP-02-federation-registry.md`** : Sub-system 2 CR; migrated to `change-requests/`.
4. **`CR-DEA-RP-03-federation-watchdog.md`** : Sub-system 3 CR; migrated to `change-requests/`.
5. **`CR-DEA-RP-04-visibility-surfaces.md`** : Sub-system 4 CR; migrated to `change-requests/`.

## Compatibility Vocabulary Anchor

The Release Package Program does **NOT** invent a new compatibility vocabulary.
It adopts the **CR-AM-02 §11 shape** (per-axis boolean, default-inherit,
immutable-once-published, independent axes) and defines four
release-package-specific axes alongside:

- `pin_alignment`
- `asset_presence`
- `peer_pin_satisfaction`
- `release_note_consistency`

## Canonical References Used

- **CR-9** : OpenDEA Runtime, Knowledge Graph & Interoperability Architecture
- **CR-11** : Interoperability, Federation & Ecosystem Conformance
- **CR-AM-02 §11** : Compatibility Vocabulary (assessment-metamodel)
- **CR-ECF-001..008** : Enterprise Concept Framework (ECF = Domain × Stage)
- **CR-CM-000A** : Terminology Alignment

## Decisions and Workarounds

The six recommendations and their workarounds (cross-repo auth phases, acknowledgement evidence types, BPMN profile embedding, etc.) are documented in the relevant CR/ADR sections. The planning-folder record predates those workarounds; the canonical artifacts include them as inline annotations.