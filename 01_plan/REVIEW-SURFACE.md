# CR-DEA-RP-01: Release Package Program (umbrella CR)

## What is being reviewed

CR-DEA-RP-01 establishes the **Release Package Program** as a federation sub-system under the governance of `technehub-labs/dea-release-package`. The umbrella defines four sub-systems (per-repo package gate, federation registry, federation watchdog, visibility surfaces), adopts the CR-AM-02 §11 compatibility-vocabulary shape with four release-package-specific axes, and provides a shared Python toolkit consumed by every `dea-catalog-*` repo via reusable workflows.

## Files under review

| File | Purpose |
|---|---|
| [CR-DEA-RP-01](./change-requests/CR-DEA-RP-01-release-package-program.md) | The umbrella CR (decision statement, drivers, architecture, consequences, rejected alternatives, non-decisions, follow-ons). |
| [ADR-DEA-RP-01](./docs/adr/ADR-DEA-RP-01-program-architecture.md) | Program architecture design specification (the 4 sub-systems, the toolkit, the CI enforcement model). |
| [CR-DEA-RP-02](./change-requests/CR-DEA-RP-02-federation-registry.md) | Sub-system 2: Federation Release Registry. |
| [CR-DEA-RP-03](./change-requests/CR-DEA-RP-03-federation-watchdog.md) | Sub-system 3: Federation Watchdog. |
| [CR-DEA-RP-04](./change-requests/CR-DEA-RP-04-visibility-surfaces.md) | Sub-system 4: Visibility Surfaces. |
| [docs/standards/registry-schema.md](./docs/standards/registry-schema.md) | The canonical manifest schema (`registry-schema@v1`). |
| [docs/standards/bpmn-profile.md](./docs/standards/bpmn-profile.md) | The BPMN 2.0 subset for process catalog plugin files. |
| [README.md](./README.md) | The program overview. |
| [GOVERNANCE.md](./GOVERNANCE.md) | Decision authority + cross-repo coordination rules. |

## Status

- **CR-DEA-RP-01:** `Status: Proposed` in the file header; awaiting architecture-board acceptance.
- **Sub-system CRs (RP-02..04):** also `Status: Proposed`; review depends on RP-01 acceptance.
- **Toolkit:** scaffold only (`toolkit/src/dea_release_package/`); no implementation until RP-01 is accepted.
- **CI workflows:** scaffold only (`.github/workflows/`); referenced by CR but not yet executed.

## Review checklist

Please review against these questions and leave inline comments on the specific file + section:

### Scope and program shape

- [ ] Is the four-sub-system decomposition (per-repo gate, registry, watchdog, visibility) the right partition for a federation program? Alternative partitions to consider: single-gateway vs federated-toolkit; centralized vs per-repo.
- [ ] Are the four release-package-specific compatibility axes (`pin_alignment`, `asset_presence`, `peer_pin_ass`, `release_note_consistency`) the right axes for *cross-repo release* compatibility? Should there be more (e.g. `consumer_compatibility`)? Should any be dropped?
- [ ] Is the layered compatibility shape (CR-AM-02 §11 axes + RP-specific axes) the right way to coexist with the assessment-metamodel compatibility vocabulary? Could the RP axes be a strict subset / extension / orthogonal?

### Cross-repo authority and auth

- [ ] Is the three-phase auth model (PAT → GitHub App → PR-from-source) the right evolution path for registry writes? Are the phases sequenced correctly?
- [ ] Is the watchdog's "flag unacknowledged divergence" rule the right signal-vs-noise policy? Acknowledgement is currently narrow (CHANGELOG sections or manifest `acknowledgements:` block); should it be wider?
- [ ] Is `dea-release-package` the right home for the program, vs a sub-directory of `dea-metaframework`?

### Toolkit and consumer model

- [ ] Is the toolkit scope right (ECF map rendering, Excel flat-view, booklet, engine plugins, snapshot, registry producer/consumer, watchdog, visibility)? Anything missing? Anything over-scoped?
- [ ] Is the per-catalog profile mechanism the right way to avoid drift across 7 catalog repos?
- [ ] Is the BPMN 2.0 profile subset correct for process catalog plugin files? Should it include gateways / sub-processes?

### Governance and process

- [ ] Are the parent CR references correct (`CR-11`, `CR-9`)? Does CR-11 actually authorize federation sub-systems of this kind?
- [ ] Is the relationship to CR-AM-02 §11 (assessment-metamodel compatibility vocabulary) correct? Should the RP-specific axes be moved into CR-AM-02's vocabulary instead?
- [ ] Are the per-catalog adoption CRs (RP-08..NN) sequenced correctly? Should BC or Processes be the pilot?

### Implementation plan

- [ ] Is the Phase 2 pilot choice (BC first, Processes second) the right sequencing? Per your earlier selection, BC is the pilot.
- [ ] Are the pre-program releases grandfathered correctly? Should there be a retroactive-adoption path?

## How to leave comments

- Inline comments on the specific file via GitHub's commit view (e.g. `B2FD3524..HEAD` on `main`).
- Comments on this issue for cross-cutting concerns.
- Suggested edits via PR against `main` (label them `[CR-DEA-RP-01 review]` so they cluster).

## Acceptance criteria

A CR-DEA-RP-01 acceptance decision (from the architecture board) will consider:

1. All 12 review-checklist questions addressed (or marked out-of-scope with rationale).
2. The four sub-system CRs (RP-02..04) are confirmed as the right decomposition.
3. The compatibility-vocabulary alignment with CR-AM-02 §11 is approved.
4. The toolkit scope is approved (with any additions/drops from the review).
5. The pilot choice (BC first) is approved.

After acceptance: the CR's `Status:` header flips to `Accepted`; the four sub-system CRs land as follow-on reviews; toolkit implementation begins.

## Cross-references

- Compatibility vocabulary shape: see `dea-metamodel/assessment-models/vocabulary/compatibility-types.yaml` (CR-AM-02 §11).
- ECF grounding: see `dea-metaframework/docs/adr/ADR-ECF-002.md` (Domain semantic integrity) and `dea-metaframework/specification/ecf-coordinates.md`.
- Bringing up a new technehub-labs repo: see the `dea-catalog-repo-bringup` skill.
- Tag signing + GPG verification: see `~/.hermes/profiles/coder/secure-notes/gpg-signing-setup.md`.