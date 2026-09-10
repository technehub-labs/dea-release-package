# ADR-DEA-RP-01: Release Package Program Architecture

Status: Proposed
Program: dea-release-package
Parent: CR-DEA-RP-01 (Release Package Program); CR-11 (Interoperability, Federation & Ecosystem Conformance); CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture)
Related: CR-DEA-RP-02 (Federation Release Registry); CR-DEA-RP-03 (Federation Watchdog); CR-DEA-RP-04 (Visibility Surfaces); CR-AM-02 §11 (Compatibility Vocabulary); CR-ECF-001..008 (Enterprise Concept Framework); CR-CM-000A (Terminology Alignment)

---

## 1. Decision Statement

The Release Package Program establishes a **federation-wide release-package architecture** that governs how every catalog repo's release is shaped, validated, registered, watched, and surfaced to humans.

The governing principle is:

> **A release is not a tag; a release is a package. The package is the contract between the producer (the catalog repo) and the federation (consumers, watchdog, registry).**

The architecture therefore:

- defines the **Release Package Shape** : the union of human-readable assets, machine-consumable plugins, and federation metadata;
- defines the **Federation Release Registry** : a git-managed, schema-versioned, PR-reviewed source of truth for cross-repo release metadata;
- defines the **Federation Watchdog** : a continuous monitor for pin divergence, asymmetric compatibility, missing assets, and mandate mismatches;
- defines the **Visibility Surfaces** : generated artifacts that translate registry metadata and watchdog flags into human-legible summaries;
- provides a **shared toolkit** : Python modules for ECF-backdrop rendering, Excel flat-view, booklet rendering, engine-plugin generation, contributions-and-decisions snapshotting, and registry producer/consumer logic;
- mandates **CI enforcement** : release-package conformance is a required status check on every catalog repo's `main` branch.

The architecture does NOT:

- invent a compatibility vocabulary (it adopts the CR-AM-02 §11 shape and defines release-package-specific axes alongside);
- replace any existing per-repo release pipeline (it extends them via reusable workflows);
- introduce a new persistence technology (the registry is git-managed YAML);
- decide the contents of any specific catalog (those belong to per-catalog CRs).

---

## 2. Why This Decision Is Necessary

OpenDEA today operates as a federation of governed catalog repos. Each repo's release is independent: BC catalog ships its capability map; processes catalog ships its process catalog; business-objects catalog ships its objects. Three architectural gaps prevent the federation from operating coherently:

1. **The federation has no shared release shape.** Each catalog invents its own release assets. Cross-catalog reading requires learning each repo's conventions.

2. **The federation has no shared compatibility vocabulary.** Repos that depend on each other (BC catalog processes business objects; processes catalog references capabilities) communicate compatibility through unstructured release-note prose. Pin drift, asymmetric claims, and mandate mismatches are invisible.

3. **The federation has no shared watchdog.** No component monitors the federation for divergence. Drift is detected by accident, not by design.

Without a governed architecture:

- each catalog's release ships different assets in different formats with different naming conventions;
- cross-catalog compatibility decays over time without monitoring;
- bug fixes in shared tooling replicate per-repo;
- consumers (BPMN engines, ArchiMate, data-modelling tools) cannot rely on consistent plugin shapes.

---

## 3. Decision Drivers

The architecture addresses:

1. **Federation-wide release shape** : every catalog release ships the same asset classes;
2. **Producer-side compatibility metadata** : the registry is the counterpart to each repo's `dependencies.yaml`;
3. **Continuous federation monitoring** : pin divergence, asymmetric claims, missing assets, mandate mismatches caught within 24 hours;
4. **Human-legible visibility** : onboarding, release notes, quarterly reporting;
5. **Shared toolkit reuse** : one Python toolkit, called from N catalog repos;
7. **CI enforcement** : release-package conformance is a required status check;
8. **Compatibility vocabulary alignment** : adopts the CR-AM-02 §11 shape for the assessment subsystem; defines release-package-specific axes alongside;
9. **ECF and metamodel pin discipline** : every manifest carries its pins; the watchdog flags unacknowledged pin divergence;
10. **Append-only discipline** : historical manifests are immutable evidence;
11. **Schema versioning** : schema bumps don't invalidate historical manifests;
12. **Cross-repo auth discipline** : the registry is a sibling repo, not a runtime database;
13. **PR-review discipline** : every manifest lands through a review surface.

---

## 4. The Four Sub-Systems

The architecture decomposes into four peer sub-systems, each with its own CR, its own CI surface, and its own governance weight:

### 4.1 Sub-system 1 : Per-repo package gate

Lives in each catalog repo as `validate-release-package.yml` + extensions to `publish-versioned.yml`. Three enforcement surfaces:

- **Pre-merge gate** : every PR with path filter; runs `build_release_package.py --dry-run --check` to assert assets would build cleanly;
- **Pre-release gate** : tag push; runs the real build with `--strict`; blocks `publish-versioned.yml` until all assets validate;
- **Post-release audit** : on-demand or cron; downloads the GitHub Release and validates every asset against the registry's `asset_checksums`.

Emits the release manifest on tag push via `dea-release-package/.github/reusable-workflows/emit-release-manifest.yml`.

Specified in CR-DEA-RP-01 §8.

### 4.2 Sub-system 2 : Federation Release Registry

Lives in `dea-release-package/federation-registry/`. Git-managed YAML, one manifest per release, PR-reviewed. Schema-versioned (`registry-schema@v1`).

Manifest schema fields:
- `release.repo`, `release.tag`, `release.commit_sha`, `release.released_at`
- `release.ecf_pin`, `release.metamodel_pin`
- `release.peer_pins` : peer catalog repos pinned at tags
- `release.compatibility` : six boolean axes (CR-DEA-RP-01 §7)
- `release.compatibility_claims` : directed claims about specific peer tags
- `release.asset_inventory` : count of each asset type
- `release.asset_checksums` : SHA-256 of each asset
- `release.drift_flags` : populated by the watchdog
- `release.registry_schema` : which schema version authored the manifest

Storage layout: `releases/<year>/<month>/<org>-<repo>-<tag>.yaml`.

Specified in CR-DEA-RP-02.

### 4.3 Sub-system 3 : Federation Watchdog

Lives in `dea-release-package/.github/workflows/watchdog.yml`. Three jobs:

- **Pin coherence watchdog** : flags ECF pin or metamodel pin divergence across releases in the last 90 days that is unacknowledged in the newer release's CHANGELOG;
- **Cross-version compatibility watchdog** : flags asymmetric claims, pinned-to-deleted-tag, mandate mismatches;
- **Asset drift watchdog** : flags checksum mismatch, missing checksums, registry drift.

Plus a derived **release timeline + dependency graph** updated nightly (`timeline/<year>-<quarter>.yaml`).

Specified in CR-DEA-RP-03.

### 4.4 Sub-system 4 : Visibility Surfaces

Two surfaces:

- **Registry Index Page** : `federation-registry/README.md` (generated); federation pin map, recent releases, compatibility state, watchdog issue summary, quarterly timeline pointer;
- **Release Note Compatibility Annex** : auto-generated appendix attached to each catalog repo's `release-notes.md`.

Specified in CR-DEA-RP-04.

---

## 5. The Compatibility Vocabulary (Release-Package-Specific Axes)

### 5.1 Adoption of the CR-AM-02 §11 shape

The architecture does NOT invent a new compatibility vocabulary. It adopts the **CR-AM-02 §11 shape**:

- per-axis boolean (`compatible` / `incompatible`);
- default-inherit (silent axes are treated as compatible against the previous version);
- immutable-once-published (a release's compatibility declaration is frozen at tag time);
- independent axes (a model can be schema/semantic/scoring/maturity/result/benchmark compatible independently).

### 5.2 Release-package-specific axes

Four axes are defined for the release-package concern:

| Axis | Meaning |
|---|---|
| `pin_alignment` | ECF pin and metamodel pin are aligned with the federation's current pins OR divergence is acknowledged in CHANGELOG. |
| `asset_presence` | Every asset listed in the catalog's release-package CR is present in the GitHub Release with non-zero size and validated checksum. |
| `peer_pin_satisfaction` | Every repo listed in `peer_pins` exists at the named tag; the peer release exists in the registry. |
| `release_note_consistency` | Every compatibility mandate in this release's notes is reciprocated in the target release's notes OR has a clear expiry. |

### 5.3 Compatibility claims (directed)

The `compatibility_claims` field uses a separate vocabulary, distinct from the axes:

| Relationship | Meaning |
|---|---|
| `compatible` | This release works correctly with the target release at the target tag. |
| `requires` | This release cannot operate without the target release being at or beyond the target tag. |
| `breaks` | This release does NOT work with the target release at the target tag (the consumer must update). |
| `unknown` | The relationship has not been investigated. |

`unknown` is the default. Authors are not required to investigate every peer; the watchdog flags `unknown` claims older than 90 days.

### 5.4 Distinction from CR-AM-02 §11 axes

The CR-AM-02 axes (`schema`, `semantic`, `scoring`, `maturity`, `result`, `benchmark`) are *model-version* axes; they describe whether a model artifact (assessment, schema, scoring rule) is compatible with its previous version.

The release-package axes are *cross-repo* axes; they describe whether a release composes correctly with the rest of the federation.

Both vocabularies MAY appear in a release manifest; a release that participates in both the assessment-metamodel program and the release-package program carries both sets.

---

## 6. The Shared Toolkit

### 6.1 Module layout

```
dea-release-package/toolkit/src/dea_release_package/
├── ecf_map/                    # ECF-backdrop rendering (HTML + PNG)
│   ├── renderer.py
│   ├── html_template/
│   └── png_renderer.py        # A0 + A3 raster
├── excel_flat_view/            # Catalog-specific Excel schemas
│   ├── schema.py
│   ├── writer.py
│   └── profiles/                # one per catalog type
├── booklet/                    # Pandoc/WeasyPrint templates
│   ├── long_booklet.py          # one entry per page
│   ├── short_booklet.py         # orientation guide
│   └── templates/
├── plugins/                    # Engine plugin generators
│   ├── bpmn/
│   │   ├── generator.py
│   │   ├── profile.py
│   │   └── validator.py
│   ├── archimate/
│   └── ...
├── snapshot/                   # contributions-and-decisions
│   ├── contributions.py
│   └── decisions.py
├── registry/                   # Federation Registry producer/consumer
│   ├── emit.py
│   ├── validate.py
│   ├── reader.py
│   └── writer.py
├── watchdog/                   # Sub-system 3
│   ├── pin_coherence.py
│   ├── cross_version.py
│   ├── asset_drift.py
│   ├── timeline.py
│   └── resolve.py
├── visibility/                 # Sub-system 4
│   ├── index.py
│   ├── annex.py
│   └── templates/
└── cli.py                       # entry points
```

### 6.2 Profiles

For per-catalog extension points (Excel schemas, booklet templates, plugin generators), the toolkit uses a **profile** pattern:

- A profile is a directory under `dea_release_package.<module>.profiles/` with a `profile.yaml` describing the catalog-specific schema;
- The default profile ships a working configuration for the BC catalog;
- Each catalog's adoption CR adds a profile directory (or extends the default).

This avoids the "fork the toolkit per catalog" trap.

---

## 7. The BPMN Profile

For process catalog releases, the BPMN plugin file conforms to a published profile defined as a subset of OMG BPMN 2.0:

| Element | Status |
|---|---|
| `<bpmn:definitions>` | Required |
| `<bpmn:process>` | Required; one per process entity |
| `<bpmn:lane>` | Optional |
| `<bpmn:task>` | Required |
| `<bpmn:startEvent>`, `<bpmn:endEvent>` | Required; one per process |
| `<bpmn:sequenceFlow>` | Required; from process lineage |
| `<bpmn:dataObject>` | Optional |
| `<bpmn:documentation>` | Required; carries definition + ECF coords |

Profile definition: `dea-release-package/standards/bpmn-profile.md`. Profile versioned alongside the toolkit.

### 7.1 Profile validator

`dea_release_package.plugins.bpmn.validate()` walks the XML tree and asserts every element present is in the profile. The validator runs in:

- per-repo pre-merge gate;
- pre-release gate;
- post-release watchdog's asset drift check.

---

## 8. The ArchiMate Profile

For business-capability catalog releases, the ArchiMate plugin file conforms to the Open Exchange XML format. Profile:

- one `<element>` per BC entity;
- ECF coordinates carried in `<property>` elements;
- the profile is intentionally minimal.

Profile definition: `dea-release-package/standards/archimate-profile.md`. Full spec deferred to the BC catalog's per-repo adoption CR.

---

## 9. Cross-Repo Auth

Three-phase model:

### Phase 1 (transition): PAT-based dispatch

Each catalog repo has a `REGISTRY_TOKEN` PAT scoped to `dea-release-package` with `Contents: Write`. Stored as a repo secret on the catalog repo. The catalog repo's `publish-versioned.yml` uses the PAT to push the manifest.

### Phase 2 (steady state): GitHub App

A `dea-federation-bot` GitHub App installed on both source and registry repos. The App's permissions are narrower than PATs and can be audited centrally. Per-repo PATs are deprecated.

### Phase 3 (long term): PR-from-source

The catalog repo opens a PR against `dea-release-package` with the new manifest on tag push. No special auth; uses the standard `GITHUB_TOKEN`. The watchdog's tamper-evidence invariant is unchanged either way.

Each catalog repo's adoption CR names which phase it lands under.

---

## 10. CI / GitHub Actions Enforcement

### 10.1 Per-repo gates (Sub-system 1)

| Surface | Trigger | Failure mode |
|---|---|---|
| Pre-merge gate | PR with path filter | Drift between data and rendered assets |
| Pre-release gate | Tag push, blocks publish | Asset completeness |
| Post-release audit | Cron or dispatch | Tamper-evidence; published artifact matches CI-built |

### 10.2 Federation gates (Sub-system 3)

| Surface | Trigger | Failure mode |
|---|---|---|
| Pin coherence watchdog | Nightly + dispatch | ECF / metamodel pin divergence unacknowledged |
| Cross-version watchdog | Nightly + dispatch | Asymmetric compatibility, mandate mismatch |
| Asset drift watchdog | Nightly + dispatch | Checksum mismatch, missing assets |

### 10.3 Branch protection

Each catalog repo's release-package validation SHALL be a required status check on `main`.

---

## 11. Versioning and Lifecycle

| Component | Versioning | Backward-compat window |
|---|---|---|
| `dea-release-package` (program) | SemVer | 2 minor cycles |
| Toolkit | CalVer (YYYY.MM.PATCH) | 2 minor cycles |
| Registry schema | Integer (v1, v2...) | 2 schema versions |
| Reusable workflow | Tag-pinned (`@v1`, `@v2`) | Major version retained indefinitely |

Historical releases (pre-program) are grandfathered; the watchdog flags them with `asset_presence: incompatible` but does not open high-severity issues for them.

---

## 12. The Repository Layout

```
dea-release-package/
├── README.md
├── GOVERNANCE.md
├── LICENSE
├── NOTICE
├── CITATION.cff
├── CHANGELOG.md
├── change-requests/
│   ├── README.md
│   ├── CR-DEA-RP-01..04-*.md
│   └── future-CRs/
├── docs/
│   ├── adr/
│   │   ├── ADR-DEA-RP-01..NN-*.md
│   │   └── ...
│   └── standards/
│       ├── bpmn-profile.md
│       ├── archimate-profile.md
│       └── ...
├── toolkit/
│   ├── pyproject.toml
│   ├── src/dea_release_package/
│   ├── tests/
│   └── ...
├── templates/
├── federation-registry/
│   ├── README.md
│   ├── releases/<year>/<month>/
│   ├── timeline/<year>-<quarter>.yaml
│   └── schemas/
├── .github/
│   ├── workflows/
│   │   ├── watchdog.yml
│   │   ├── registry-validate.yml
│   │   ├── toolkit-ci.yml
│   │   ├── visibility.yml
│   │   └── audit-catalog-releases.yml
│   └── reusable-workflows/
│       ├── release-package.yml
│       └── emit-release-manifest.yml
└── examples/
    ├── bc-release-package/
    └── processes-release-package/
```

---

## 13. Consequences

### Positive

- Federation-wide release shape: every catalog ships the same asset classes with consistent naming;
- Producer-side compatibility metadata: the registry is the counterpart to `dependencies.yaml`;
- Continuous federation monitoring: pin divergence, asymmetric claims, missing assets, mandate mismatches caught within 24 hours;
- Human-legible visibility: onboarding, release notes, quarterly reporting;
- Shared toolkit: one Python codebase, called from N catalog repos via reusable workflows;
- CI enforcement: release-package conformance is a required status check;
- Compatibility vocabulary alignment: adopts CR-AM-02 §11 shape, defines release-package-specific axes alongside;
- ECF and metamodel pin discipline: every manifest carries its pins; the watchdog flags unacknowledged divergence.

### Negative

- New repo (`dea-release-package`) with full governance weight;
- Cross-repo auth (Phase 1 PAT) introduces N credentials to manage; Phase 2 GitHub App installation is org-wide work;
- Append-only discipline means corrections are clumsier than in-place edits;
- Schema bumps require coordinated reader/writer updates;
- The watchdog's first week will surface a lot of pre-existing divergence;
- Each catalog repo grows 2 new workflows and a thin wrapper script.

---

## 14. Rejected Alternatives

### A : Per-catalog decentralized

Each `dea-catalog-*` ships its own toolkit.

Rejected because: drift is guaranteed; bug fixes replicate N times; cross-repo compatibility is invisible.

### B : `dea-metaframework` sub-directory

The program lives as a sub-directory of `dea-metaframework`.

Rejected because: the program is a federation-level peer concern; reusable workflows cross-repo convention favors a dedicated repo; cross-repo auth is simpler between sibling repos.

### C : External database for the registry

The federation registry uses a managed Postgres instance.

Rejected because: breaks the "everything is a CR" discipline; loses free PR review; introduces operational dependency.

### D : Single compatibility vocabulary

Adopt CR-AM-02 §11 axes directly for cross-repo release compatibility.

Rejected because: the CR-AM-02 axes are model-version axes; they don't capture release-package concerns (pin alignment, asset presence, peer pin satisfaction, release-note consistency).

### E : Mandatory compatibility claim authorship per release

Every release MUST author claims for every known peer.

Rejected because: many releases have no peer relationship to claim against; better to flag stale `unknown` claims after a grace period.

### F : Hard-fail enforcement in watchdog

The watchdog blocks merges on divergence.

Rejected because: merges are a per-repo concern; the watchdog is a federation concern; acknowledged divergence is sometimes intentional.

### G : Real-time event-driven watchdog

Watchdog fires on every registry PR merge, not on a cron.

Rejected because: race conditions with concurrent merges; harder timeline aggregates; 24h latency is acceptable.

---

## 15. Explicit Non-Decisions

This ADR does NOT decide:

- The specific toolkit API surface (deferred to toolkit design);
- The exact cross-repo auth model per catalog repo (each adoption CR names Phase 1/2/3);
- The GitHub Pages enablement for `dea-release-package`;
- The federation dashboard UI (if any);
- The migration path for pre-program releases (grandfathered).

---

## 16. Decision Summary

The Release Package Program Architecture:

- decomposes into four sub-systems (per-repo gate, federation registry, watchdog, visibility surfaces);
- adopts the CR-AM-02 §11 compatibility vocabulary shape and defines four release-package-specific axes;
- provides a shared Python toolkit called from N catalog repos via reusable workflows;
- enforces release-package conformance as a required status check;
- lives in `technehub-labs/dea-release-package` as a new component repo with full governance weight.

The architecture makes the federation legible, monitorable, and self-correcting.

---

## 17. Required Follow-On ADRs / CRs

- **ADR-DEA-RP-02** : Registry Schema; design specification.
- **ADR-DEA-RP-03** : Visibility Surface Architecture; design specification.
- **CR-DEA-RP-01..04** : Released as the four implementation CRs.
- **Per-catalog adoption CRs** : one per catalog repo.

---

*Status: Proposed. Parent: CR-DEA-RP-01 (Release Package Program); CR-11 (Interoperability, Federation & Ecosystem Conformance); CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture). Compatibility shape adopted from CR-AM-02 §11.*