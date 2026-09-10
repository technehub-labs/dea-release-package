# Release Package Program

> A federation sub-system that governs how every catalog repo's release is shaped, validated, registered, watched, and surfaced to humans.

**Component type:** Federation program (peer of catalog repos, not a catalog itself) · **Parent governance:** [CR-11 (Interoperability, Federation & Ecosystem Conformance)](https://github.com/technehub-labs/dea-metaframework/blob/main/change-requests/CR-011.md), [CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture)](https://github.com/technehub-labs/dea-metaframework/blob/main/change-requests/CR-009.md) · **Status:** Scaffold (program CRs in `change-requests/` are `Status: Proposed`)

## What this is

The canonical home of the **Release Package Program**: the rules, toolkit, registry, watchdog, and visibility surfaces that govern how every OpenDEA catalog repo's release is published.

The program answers one question:

> When a catalog repo cuts a tag, what ships with it, where does it land, how is its cross-federation compatibility verified, and how do humans find out?

The program does NOT answer the contents of any specific catalog. Each catalog repo (`dea-catalog-business-capabilities`, `dea-catalog-processes`, etc.) is the authority for its own entities. This repo is the authority for *how those entities are released*.

## What this program is not

| Not this | Because |
|---|---|
| A catalog of entities | It governs release shape, not catalog content. |
| A documentation site | The visibility surfaces (CR-DEA-RP-04) are generated; this repo is the source. |
| A runtime service | The registry is git-managed YAML; the watchdog is GitHub Actions; no servers run. |
| A replacement for per-repo release pipelines | Each catalog's existing pipeline is extended, not replaced. |

## Status

**Scaffold.** Program CRs in `change-requests/` establish the four sub-systems:

- `CR-DEA-RP-01-release-package-program.md` (umbrella; Status: Proposed)
- `CR-DEA-RP-02-federation-registry.md` (Sub-system 2; Status: Proposed)
- `CR-DEA-RP-03-federation-watchdog.md` (Sub-system 3; Status: Proposed)
- `CR-DEA-RP-04-visibility-surfaces.md` (Sub-system 4; Status: Proposed)

The toolkit (`toolkit/`), federation registry (`federation-registry/`), GitHub Actions workflows (`.github/workflows/`), and reusable workflows (`.github/reusable-workflows/`) are scaffold-only; implementation lands when the umbrella CR is accepted.

Design specifications:

- [`docs/adr/ADR-DEA-RP-01-program-architecture.md`](docs/adr/ADR-DEA-RP-01-program-architecture.md)

## Repository Structure

Current (scaffold):

```
dea-release-package/
├── README.md                              # this file
├── GOVERNANCE.md                           # governance + decision authority
├── LICENSE                                # Apache-2.0 (canonical org license)
├── NOTICE                                 # attributions
├── CITATION.cff                           # software citation metadata
├── CHANGELOG.md                           # program changelog
├── change-requests/                       # CRs for the program itself
│   ├── README.md                          # CR index
│   ├── CR-DEA-RP-01..04-*.md              # the four sub-system CRs
│   └── future-CRs/                        # planned follow-ons (RP-05..NN)
├── docs/
│   ├── adr/                               # ADRs (design specifications)
│   │   └── ADR-DEA-RP-01-program-architecture.md
│   └── standards/                         # Toolkit usage, plugin profiles
├── toolkit/                               # Framework Python (Sub-system 1 producer)
│   └── src/dea_release_package/
│       ├── ecf_map/                       # ECF-backdrop rendering
│       ├── excel_flat_view/               # Catalog-specific Excel schemas
│       ├── booklet/                       # PDF booklet generators
│       ├── plugins/                       # Engine plugin generators
│       │   ├── bpmn/
│       │   └── archimate/
│       ├── snapshot/                      # contributions-and-decisions
│       ├── registry/                      # Sub-system 2 producer/consumer
│       ├── watchdog/                      # Sub-system 3
│       └── visibility/                    # Sub-system 4
├── templates/                             # Pandoc/WeasyPrint booklet templates
├── federation-registry/                   # git-managed YAML registry (Sub-system 2 storage)
│   ├── README.md                          # generated Registry Index Page (Sub-system 4)
│   ├── releases/<year>/<month>/           # one manifest per release
│   ├── timeline/<year>-<quarter>.yaml     # generated timeline + dependency graph
│   └── schemas/                           # registry-schema versions
├── .github/
│   ├── workflows/
│   │   ├── watchdog.yml                   # Sub-system 3 (nightly cron + dispatch)
│   │   ├── registry-validate.yml          # PR-time validation on federation-registry/
│   │   ├── toolkit-ci.yml                 # Python tests for the toolkit
│   │   ├── visibility.yml                 # Sub-system 4 generator
│   │   └── audit-catalog-releases.yml     # nightly federation audit
│   └── reusable-workflows/
│       ├── release-package.yml            # consumed by each catalog repo
│       └── emit-release-manifest.yml      # catalog-side manifest emitter
└── examples/                              # Reference implementations
    ├── bc-release-package/                # BC catalog adoption example
    └── processes-release-package/         # Process catalog adoption example
```

Planned (post `CR-DEA-RP-01` acceptance, indicative): populated toolkit modules; first registry entries; first watchdog run. The final structure is reconciled with the umbrella CR before any PR lands.

## How a release flows through this program

1. A catalog repo (`dea-catalog-business-capabilities`) cuts a tag (`v1-alpha.3`).
2. The catalog's `publish-versioned.yml` calls the reusable workflow `release-package.yml` from this repo.
3. The toolkit builds the package: HTML, A0 PNG, A3 PNG, Excel, booklet PDFs, BPMN/ArchiMate plugin, contributions-and-decisions snapshot.
4. The toolkit emits a release manifest as a PR to `dea-release-package/federation-registry/releases/<year>/<month>/`.
5. The manifest lands through PR review; `registry-validate.yml` runs.
6. `publish-versioned.yml` ships the GitHub Release with the full package zip.
7. The watchdog (`watchdog.yml`) reads the new manifest on its next run (nightly cron or dispatch); flags any unacknowledged divergence.
8. The visibility surface (`visibility.yml`) regenerates `federation-registry/README.md` with the new release.

## Compatibility Vocabulary

The Release Package Program adopts the **CR-AM-02 §11 compatibility vocabulary shape** (per-axis boolean, default-inherit, immutable-once-published, independent axes) and defines four release-package-specific axes alongside:

| Axis | Meaning |
|---|---|
| `pin_alignment` | ECF pin and metamodel pin alignment with the federation. |
| `asset_presence` | Every asset in inventory is present in the GitHub Release with validated checksum. |
| `peer_pin_satisfaction` | Every repo in `peer_pins` exists at the named tag. |
| `release_note_consistency` | Every compatibility mandate in this release's notes is reciprocated. |

A release manifest MAY also carry the CR-AM-02 §11 axes (`schema`, `semantic`, `scoring`, `maturity`, `result`, `benchmark`) when the catalog participates in the assessment-metamodel program. The two sets are layered, not exclusive.

## Change Control

| Change | Requirement |
|---|---|
| Program scope, sub-system architecture | Change Request (CR-DEA-RP-NN) |
| Registry schema version | CR-DEA-RP-NN (schema bump is itself a CR) |
| Compatibility vocabulary change | CR referencing CR-AM-02 §11 vocabulary |
| Toolkit API surface | ADR-DEA-RP-NN |
| Cross-repo auth phase change (Phase 1 → 2 → 3) | CR per transition |

## Contributing

Until `CR-DEA-RP-01` is accepted, contributions take the form of CR review, vocabulary critique, and adoption CR drafts (one per catalog repo) rather than code. See [`change-requests/`](change-requests/) and [`docs/adr/`](docs/adr/).