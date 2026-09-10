# Change Requests : Release Package Program

This index lists the Change Requests (CRs) that govern the Release Package Program. CRs follow the OpenDEA CR template (decision statement, why necessary, drivers, architecture, consequences, rejected alternatives, non-decisions, decision summary, follow-ons).

## Index

| CR | Title | Status | Parent | Authoring Date |
|---|---|---|---|---|
| [CR-DEA-RP-01](./CR-DEA-RP-01-release-package-program.md) | Release Package Program (umbrella) | Proposed | CR-11; CR-9 | 2026-09-10 |
| [CR-DEA-RP-02](./CR-DEA-RP-02-federation-registry.md) | Federation Release Registry (Sub-system 2) | Proposed | CR-DEA-RP-01 | 2026-09-10 |
| [CR-DEA-RP-03](./CR-DEA-RP-03-federation-watchdog.md) | Federation Watchdog (Sub-system 3) | Proposed | CR-DEA-RP-02; CR-DEA-RP-01 | 2026-09-10 |
| [CR-DEA-RP-04](./CR-DEA-RP-04-visibility-surfaces.md) | Visibility Surfaces (Sub-system 4) | Proposed | CR-DEA-RP-02; CR-DEA-RP-03; CR-DEA-RP-01 | 2026-09-10 |

## Future CRs (planned, not yet drafted)

| Planned CR | Title | Depends on |
|---|---|---|
| CR-DEA-RP-05 | Cross-repo auth migration (Phase 1 → Phase 2) | CR-DEA-RP-01 acceptance |
| CR-DEA-RP-06 | Canonical CHANGELOG format across catalog repos | CR-DEA-RP-01 acceptance |
| CR-DEA-RP-07 | BPMN profile extension protocol | First process catalog adoption CR |
| CR-DEA-RP-08..NN | Per-catalog adoption CRs (one per `dea-catalog-*`) | CR-DEA-RP-01 acceptance |

## Companion ADRs

ADRs (Architecture Decision Records) are design specifications that inform the CRs. They live in [`../docs/adr/`](../docs/adr/).

| ADR | Title |
|---|---|
| [ADR-DEA-RP-01](../docs/adr/ADR-DEA-RP-01-program-architecture.md) | Program Architecture |
| ADR-DEA-RP-02 | Registry Schema (planned) |
| ADR-DEA-RP-03 | Visibility Surface Architecture (planned) |

## Status Definitions

- **Proposed** : drafted; under review.
- **Accepted** : approved by the architecture board; implementation authorized.
- **Implemented** : code landed on `main`; toolkit / registry / workflows operational.
- **Superseded** : replaced by a later CR; pointer + status flip preserved (not in-place edit).

## Compatibility Vocabulary Discipline

Every CR that touches the compatibility vocabulary (axes, claims, relationships) MUST cite CR-AM-02 §11 in its `Related:` field. Vocabulary changes are CR-AM-02's authority, not this program's.