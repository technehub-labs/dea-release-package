# Governance

This document establishes the decision authority and contribution rules for the Release Package Program.

## Decision Authority

The Release Package Program operates under the federation governance established by:

- **CR-11** : Interoperability, Federation & Ecosystem Conformance (parent governance)
- **CR-9** : OpenDEA Runtime, Knowledge Graph & Interoperability Architecture (parent governance)
- **CR-DEA-RP-01..NN** : the program's own CRs (in `change-requests/`)
- **ADR-DEA-RP-01..NN** : the program's own design specifications (in `docs/adr/`)

Decisions on program scope, sub-system architecture, vocabulary, and registry schema are made by the program's CRs. Toolkit API decisions are made by ADRs.

## Compatibility Vocabulary Discipline

The program adopts the CR-AM-02 §11 compatibility vocabulary shape. Any change to the vocabulary used in this program MUST cite CR-AM-02 §11 and follow its evolution protocol.

## Cross-Repo Coordination

The Release Package Program coordinates with:

- `technehub-labs/dea-metaframework`; parent governance; ECF and metamodel pin sources
- `technehub-labs/dea-metamodel`; assessment-metamodel compatibility vocabulary (CR-AM-02 §11)
- `technehub-labs/dea-architecture-framework`; root model fan-out; metamodel-pointer regeneration
- All `technehub-labs/dea-catalog-*` repos; consumers of the program (each via its own adoption CR)

## Contribution Rules

1. No code lands in this repo without an accepted CR or ADR.
2. Every CR follows the template in `change-requests/README.md`.
3. Every ADR follows the technical-spec-drafting skill's 21-section template.
4. Compatibility vocabulary changes require a paired CR against CR-AM-02 §11 in `dea-metamodel`.
5. The watchdog never modifies registry manifests; the registry is append-only.

## Pre-Program Releases

Releases that predate `CR-DEA-RP-01` acceptance are grandfathered (per `CR-DEA-RP-03` §5.3). They are flagged low-severity by the watchdog; retroactive adoption is opt-in per catalog.

## Versioning

- **Program** (this repo): SemVer
- **Toolkit**: CalVer (YYYY.MM.PATCH)
- **Registry schema**: Integer (v1, v2, ...)
- **Reusable workflows**: Tag-pinned (`@v1`, `@v2`)

Backwards-compatibility windows are documented in `ADR-DEA-RP-01` §11.