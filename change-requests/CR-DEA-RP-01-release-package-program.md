# CR-DEA-RP-01: Release Package Program

Status: Proposed
Program: dea-release-package
Parent: CR-11 (Interoperability, Federation & Ecosystem Conformance); CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture)
Related: CR-AM-01 (Assessment Metamodel Evolution); CR-AM-02 §11 (Compatibility Vocabulary); CR-ECF-001..008 (Enterprise Concept Framework); CR-CM-000A (Terminology Alignment)
Decision Type: Program (Federation Sub-System)
Implementation: Not authorized by this CR alone; implemented by CR-DEA-RP-02..04 and per-catalog adoption CRs

---

## 1. Decision Statement

The OpenDEA body of work establishes a **Release Package Program** as a federation sub-system under the governance of `technehub-labs/dea-release-package`.

The governing principle is:

> **Every release of every governed catalog repo SHALL ship as a Release Package: a versioned, validated, self-contained bundle of human-readable assets, machine-consumable plugins, and federation metadata, whose cross-repo relationships are recorded in a federation registry that the program watches.**

The Release Package Program therefore:

- establishes a new component repository, `technehub-labs/dea-release-package`, with its own CR index, ADRs, and governance surface;
- defines a canonical Release Package shape (asset list, naming conventions, file formats) that every catalog repo's release MUST conform to;
- establishes a **Federation Release Registry** as the single source of truth for cross-repo release metadata;
- establishes a **Federation Watchdog** that flags drift in real time (pin divergence, asymmetric compatibility claims, missing assets, mandatemismatch between release notes);
- provides a shared toolkit (ECF-backdrop rendering, Excel flat-view, booklet rendering, engine-plugin generation, contributions-and-decisions snapshotting) that every catalog repo consumes via reusable workflows;
- mandates that release-package conformance is enforced as a required status check on every catalog repo's `main` branch.

The Release Package Program does NOT:

- decide the contents of any specific catalog (those belong to per-catalog CRs);
- replace any existing per-repo release pipeline (it extends them);
- invent a new compatibility vocabulary (it adopts the CR-AM-02 §11 shape and defines release-package-specific axes alongside);
- introduce a new registry technology (the registry is git-managed YAML, PR-reviewed, following the OpenDEA "everything is a CR, everything is a commit" discipline).

---

## 2. Why This Decision Is Necessary

A governed catalog repo on its own is a **machine-readable surface**. Useful to engines, opaque to humans, illegible across the federation. Today, four irreducible gaps prevent OpenDEA from operating as a coherent federation:

1. **Human-readability gap.** No catalog repo currently ships a print-ready poster, an Excel flat-view, a pamphlet, or a short release guide. Stakeholders who arrive after a release re-derive context from scratch.

2. **Engine-handoff gap.** Catalogs do not live in one engine. BCs are imported into ArchiMate; processes are imported into BPMN engines; business objects are imported into data-modelling tools. Each engine consumes a different flat view; today, no catalog ships that view.

3. **Federation integrity gap.** No source of truth records "repo X released tag Y against ECF pin Z, claiming compatibility with peer repo P at tag Q." Today, each repo's `dependencies.yaml` is its own self-description, but cross-repo relational integrity is invisible.

4. **Compatibility-mandate gap.** When a release ships with a release-note compatibility mandate ("consumers on <v0.4 must update to v0.5 by Q4"), no watchdog audits whether the mandate was acknowledged by the consuming repo's next release. Asymmetric mandates go unnoticed.

Without a governed Release Package Program:

- stakeholders cannot orient themselves to a release without re-deriving context;
- engine consumers must hand-construct their own import files;
- pin drift between sibling repos goes undetected for weeks;
- compatibility mandates decay silently;
- every catalog repo eventually reinvents the same scripts in seven divergent ways.

---

## 3. Decision Drivers

The Release Package Program addresses:

1. **Human orientation** : stakeholders need a 1-page map of every release;
2. **Printable distribution** : conference posters, board handouts, training packs, audit binders;
3. **Cross-engine handoff** : every catalog has a consuming engine that needs a flat-view import;
5. **OpenDEA position visibility** : every release must show where it sits in the OpenDEA landscape (ECF pin, metamodel pin, peer catalog map);
6. **Snapshot integrity** : releases are immutable; the package preserves the published state legibly;
7. **Decision archaeology** : votes, rejected alternatives, and contributions that fed a cut must ship with the release;
9. **Cross-repo relational integrity** : a single registry records every release and its peer relationships;
10. **Drift detection** : pin divergence, asymmetric compatibility, missing assets, mandate mismatches are caught within 24 hours;
11. **Federation-wide timeline** : quarterly release-coordination reports summarize dependency graphs;
12. **Toolkit reuse** : a shared Python toolkit prevents seven divergent implementations of "what an ECF-backdrop poster looks like";
13. **Enforcement** : release-package conformance is a required status check, not an advisory gate;
14. **Schema discipline** : the registry uses git-managed YAML with explicit schema versioning, following the CR-AM-02 §11 vocabulary shape.

---

## 4. The Release Package Shape

A Release Package is the union of three asset classes:

### 4.1 Human-readable assets

Every catalog release SHALL include:

| Asset | Format | Purpose |
|---|---|---|
| ECF-backdrop map (HTML) | Interactive HTML + JS | On-screen reference, drill-down |
| ECF-backdrop poster (A0 PNG) | A0 landscape @ 300 DPI | Conference poster, board-room wall |
| ECF-backdrop print (A3 PNG) | A3 landscape @ 300 DPI | On-screen reference + desk print |
| Catalog flat-view (Excel) | One row per entry, columns = catalog-specific schema | Pivot, filter, audit |
| Pamphlet booklet (PDF) | A5 portrait, one entry per page | Per-entry deep reference |
| Release guide (PDF) | A5 portrait, 4-8 pages | Orientation, what's new, how to consume |
| Release notes (Markdown) | Per-cut diff narrative | What changed, what superseded what |

### 4.2 Machine-consumable plugins

Every catalog release SHALL include an engine-plugin file when the consuming machine for that catalog has a standard interchange. The plugin file is generated, validated against a published profile, and listed in the release manifest.

| Catalog | Consuming engine | Plugin format | Profile |
|---|---|---|---|
| Business Capabilities | ArchiMate | Open Exchange XML | ArchiMate 3.2 profile |
| Processes | BPMN engine | BPMN 2.0 XML | OMG BPMN 2.0 subset (this CR §6) |
| Business Objects | Data-modelling tool | XMI / ER diagram | TBD per CR |
| Actors | HR / IAM | LDAP/CSV | TBD per CR |
| Stakeholders | IAM | LDAP/CSV | TBD per CR |
| Organizational Units | HR / Org-chart | CSV / Open Exchange | TBD per CR |

### 4.3 Federation metadata

Every catalog release SHALL emit a **release manifest** to the federation registry (`dea-release-package/federation-registry/releases/`). The manifest is git-managed YAML, PR-reviewed, schema-versioned.

```yaml
release:
  repo: technehub-labs/dea-catalog-business-capabilities
  tag: v1-alpha.3
  commit_sha: <40-char>
  released_at: 2026-09-12T08:30:00Z
  ecf_pin: dea:ecf@1.0.0
  metamodel_pin: 1.0.0
  peer_pins:
    dea-catalog-processes: v0.4.2
    dea-catalog-business-objects: v0.2.0
  compatibility:
    schema: compatible
    semantic: compatible
    pin_alignment: compatible        # release-package-specific axis (see §7)
    asset_presence: compatible       # release-package-specific axis
    peer_pin_satisfaction: compatible # release-package-specific axis
    release_note_consistency: compatible # release-package-specific axis
  asset_inventory:
    html: 1
    png_a0: 1
    png_a3: 1
    xlsx: 1
    booklet_long: 1
    booklet_short: 1
    release_notes: 1
    plugin_files: 1
    contributions_snapshot: 1
```

---

## 5. The Repository: `technehub-labs/dea-release-package`

A new component repository with full governance weight. The repo SHALL contain:

```
dea-release-package/
├── README.md
├── GOVERNANCE.md
├── LICENSE
├── NOTICE
├── CITATION.cff
├── CHANGELOG.md
├── change-requests/                  # CR index for the program itself
├── docs/
│   ├── adr/                          # ADRs for the program
│   └── standards/                    # Toolkit usage, registry schema, profiles
├── toolkit/                          # Framework Python: ECF map, Excel, booklet, plugins
│   ├── pyproject.toml
│   ├── src/dea_release_package/
│   │   ├── ecf_map/
│   │   ├── excel_flat_view/
│   │   ├── booklet/
│   │   ├── plugins/
│   │   │   ├── bpmn/
│   │   │   └── archimate/
│   │   ├── snapshot/
│   │   └── registry/                 # federation-registry producer/consumer
│   ├── tests/
│   └── ...
├── templates/                          # Pandoc/WeasyPrint booklet templates
├── federation-registry/                # git-managed YAML registry
│   ├── README.md
│   ├── releases/<year>/<month>/
│   ├── timeline/<year>-<quarter>.yaml
│   └── schemas/
├── .github/
│   ├── workflows/
│   │   ├── watchdog.yml
│   │   ├── registry-validate.yml
│   │   ├── toolkit-ci.yml
│   │   └── audit-catalog-releases.yml
│   └── reusable-workflows/
│       └── release-package.yml        # consumed by each catalog repo
└── examples/                         # reference implementations
```

---

## 6. The Four Sub-Systems

### 6.1 Sub-system 1 : Per-repo package gate

Lives in each catalog repo as `validate-release-package.yml` + extensions to `publish-versioned.yml`. Triggered on PR (path filter) and on tag push. Emits release manifest on tag push. Specified in detail in CR-DEA-RP-02.

### 6.2 Sub-system 2 : Federation Release Registry

Lives in `dea-release-package/federation-registry/`. Git-managed YAML, one file per release, PR-reviewed. Schema-versioned (registry-schema@v1). Each catalog repo's publish workflow PRs a new manifest on tag push. Specified in CR-DEA-RP-02.

### 6.3 Sub-system 3 : Federation Watchdog

Lives in `dea-release-package/.github/workflows/watchdog.yml`. Three jobs:

- **Pin coherence watchdog** : flags ECF pin or metamodel pin divergence across releases in the last 90 days that is unacknowledged in the newer release's CHANGELOG.
- **Cross-version compatibility watchdog** : flags asymmetric compatibility claims (R claims compatible with T; T does not reciprocate), pinned-to-deleted-tag, and mandate mismatches.
- **Asset drift watchdog** : flags asset-presence divergence between GitHub Release artifact and workflow-built artifact, checksum mismatch, and registry record divergence from reality.

Plus a derived **release timeline + dependency graph** updated nightly.

Specified in CR-DEA-RP-03.

### 6.4 Sub-system 4 : User-facing visibility

Two surfaces:

- **Registry index page** : generated by a workflow, summarizing every release with compatibility status, last-known-good combinations, current ECF/metamodel pin map.
- **Release note compatibility annex** : auto-generated from the registry at release build time, merged into each catalog repo's release notes.

Specified in CR-DEA-RP-04.

---

## 7. Compatibility Vocabulary (Release-Package-Specific Axes)

This CR does NOT invent a new compatibility vocabulary. It adopts the **CR-AM-02 §11 shape** (per-axis boolean, default-inherit, immutable-once-published) and defines **four release-package-specific axes**:

| Axis | Meaning |
|---|---|
| `pin_alignment` | The release's ECF pin and metamodel pin are aligned with the federation's current pins OR the divergence is explicitly acknowledged in the release's CHANGELOG. |
| `asset_presence` | Every asset listed in the catalog's release-package CR is present in the GitHub Release with non-zero size and validated checksum. |
| `peer_pin_satisfaction` | Every repo listed in `peer_pins` exists at the named tag; the peer release exists in the federation registry. |
| `release_note_consistency` | Every compatibility mandate named in this release's notes is reciprocated in the target release's notes OR the mandate has a clear expiry. Empty mandates are valid. |

Each axis is `compatible` or `incompatible`. The default for a fresh release is `incompatible` (no evidence has been gathered yet); axes are upgraded to `compatible` by the watchdog once it has verified them.

This vocabulary is layered alongside (not in place of) the CR-AM-02 §11 axes used for assessment-metamodel compatibility. A release manifest MAY include both sets if the repo participates in both programs.

---

## 8. CI / GitHub Actions Enforcement

### 8.1 Per-repo gates (Sub-system 1)

| Surface | When | What it catches |
|---|---|---|
| Pre-merge gate | PR with path filter | Drift between data and rendered assets before merge |
| Pre-release gate | Tag push, blocks publish | Asset completeness; the package that ships matches what the tag claims |
| Post-release audit | On-demand or cron | Tamper-evidence; published artifact matches CI-built artifact |

### 8.2 Federation gates (Sub-system 3)

| Surface | When | What it catches |
|---|---|---|
| Pin coherence watchdog | Nightly cron + on dispatch | ECF / metamodel pin divergence unacknowledged in CHANGELOG |
| Cross-version watchdog | Nightly cron + on dispatch | Asymmetric compatibility, pinned-to-deleted-tag, mandate mismatch |
| Asset drift watchdog | Nightly cron + on dispatch | Asset checksum mismatch, missing assets, registry drift |

All flags open GitHub Issues on `dea-release-package` with structured bodies. Issues auto-resolve when the divergence is acknowledged.

### 8.3 Branch protection

Each catalog repo's release-package validation SHALL be a required status check on `main`. Configured via `gh api` or settings.

---

## 9. Versioning and Lifecycle

The program itself follows SemVer. The toolkit, the schemas, the reusable workflows, and the registry schema each have their own versions.

| Component | Versioning | Backward-compat window |
|---|---|---|
| `dea-release-package` (program) | SemVer | 2 minor cycles |
| Toolkit | CalVer (YYYY.MM.PATCH) | 2 minor cycles |
| Registry schema | Integer (v1, v2...) | 2 schema versions |
| Reusable workflow | Tag-pinned (`@v1`, `@v2`) | Major version retained indefinitely |

Historical releases: pre-program releases are grandfathered; the watchdog flags them with `asset_presence: incompatible` but does not open high-severity issues for them.

---

## 10. Consequences

### Positive

- Every catalog release ships with a print-ready poster, an Excel flat-view, a pamphlet, a release guide, and a federation manifest; orientation, distribution, and audit become one operation.
- Cross-repo relational integrity is observable; pin drift and asymmetric compatibility are caught within 24 hours.
- The toolkit eliminates seven divergent per-repo implementations of the same concern.
- The registry provides a queryable history of the federation; release planning meetings have a real artifact to discuss.
- Consumers (BPMN engines, ArchiMate, data-modelling tools) receive validated plugin files at every release.
- The watchdog provides clear user understanding and visibility into cross-repo compatibility state.

### Negative

- New repo = new governance burden: README, GOVERNANCE.md, CR discipline, CI on the repo itself.
- Each catalog repo grows 2 new workflows and a thin wrapper script.
- The federation registry grows with every release; storage is git-managed, so the history is immutable but append-only.
- The watchdog's signal-vs-noise rule depends on CHANGELOG discipline in each catalog repo; silent pin drift is harder to flag than acknowledged drift.
- Compatibility claim authorship is per-repo; asymmetric or stale claims require human review to resolve.

---

## 11. Rejected Alternatives

### A : Per-catalog decentralized (each repo ships its own toolkit)

Each `dea-catalog-*` ships its own `build_release_package.py`, its own templates, its own CI gates.

Rejected because:

- Drift is guaranteed; seven repos diverge within two release cycles.
- Bug fixes replicate seven times.
- Cross-repo compatibility is invisible to any single repo.

### B: `dea-metaframework` sub-directory (Option D in earlier analysis)

The program lives as a sub-directory of `dea-metaframework`.

Rejected because:

- The program is a federation-level peer concern, not a meta-framework sub-system.
- Reusable workflows cross-repo convention favors a dedicated repo.
- Cross-repo auth (registry writes) is simpler when source and destination are sibling repos under the same org App installation.

### C : External database for the registry

The federation registry uses a managed Postgres instance instead of git-managed YAML.

Rejected because:

- Breaks the "everything is a CR, everything is a commit" discipline.
- Loses free PR review on every release manifest.
- Introduces an operational dependency (DB availability) orthogonal to git availability.

### D : Single compatibility vocabulary covering all programs

Adopt CR-AM-02 §11 axes directly for cross-repo release compatibility, with no release-package-specific axes.

Rejected because:

- The CR-AM-02 axes (`schema`, `semantic`, `scoring`, `maturity`, `result`, `benchmark`) are model-version axes; they do not capture release-package concerns (pin alignment, asset presence, peer pin satisfaction, release-note consistency).
- Forcing release compatibility into those axes loses information and conflates concerns.

### E : Mandatory compatibility claim authorship per release

Every release MUST author explicit compatibility claims against every peer.

Rejected because:

- Forces busywork; many releases have no peer relationship to claim against.
- Better: claims are optional, empty claims are valid, the watchdog flags missing evidence after a configurable grace period (7 days).

---

## 12. Explicit Non-Decisions

This CR does NOT decide:

- Specific BPMN profile subset (deferred to CR-DEA-RP-02 §6);
- Specific ArchiMate profile (deferred to per-catalog adoption CR);
- Specific Excel flat-view column schema per catalog (deferred to per-catalog adoption CR);
- Specific booklet layout / typography (deferred to toolkit design, with a default template shipped in `examples/`);
- Cross-repo auth mechanism (PAT vs GitHub App vs PR-from-source) ; deferred to CR-DEA-RP-02 §8;
- Federation dashboard UI (if any) ; deferred to a future CR after the registry is populated;
- Migration path for pre-program releases; grandfathered; per-catalog retroactive adoption is optional.

---

## 13. Decision Summary

The OpenDEA establishes a Release Package Program that:

- ships every catalog release as a self-contained package of human-readable assets, machine-consumable plugins, and federation metadata;
- tracks cross-repo relationships in a git-managed federation registry with explicit schema versioning;
- watches for drift (pin divergence, asymmetric compatibility, missing assets, mandate mismatches) within 24 hours;
- provides a shared toolkit that prevents seven divergent implementations of the same concern;
- enforces conformance as a required status check on every catalog repo's `main` branch.

The program lives in `technehub-labs/dea-release-package`, a new component repository with its own CR index, ADRs, governance surface, and CI workflows.

---

## 14. Required Follow-On CRs

- **CR-DEA-RP-02** : Federation Release Registry (Sub-system 2); registry schema, ingestion flow, versioning rules.
- **CR-DEA-RP-03** : Federation Watchdog (Sub-system 3); pin coherence, cross-version compatibility, asset drift, release timeline.
- **CR-DEA-RP-04** : Visibility Surfaces (Sub-system 4); registry index page, release-note compatibility annex.
- **ADR-DEA-RP-01** : Program Architecture; design specification.
- **ADR-DEA-RP-02** : Registry Schema; schema design specification.
- **Per-catalog adoption CRs** (one per catalog repo); adapt the program to each catalog's data shape.

---

*Status: Proposed. Parent: CR-11 (Interoperability, Federation & Ecosystem Conformance); CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture). Compatibility shape adopted from CR-AM-02 §11.*