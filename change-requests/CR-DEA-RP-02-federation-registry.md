# CR-DEA-RP-02: Federation Release Registry

Status: Proposed
Program: dea-release-package
Parent: CR-DEA-RP-01 (Release Package Program)
Related: CR-AM-02 §11 (Compatibility Vocabulary); CR-11 (Interoperability, Federation & Ecosystem Conformance); CR-9 (OpenDEA Runtime, Knowledge Graph & Interoperability Architecture)
Decision Type: Architectural (Sub-System Implementation)
Implementation: Implemented by the toolkit module `dea_release_package/registry/` plus the `registry-validate.yml` workflow

---

## 1. Decision Statement

The Release Package Program establishes a **Federation Release Registry** as the single source of truth for cross-repo release metadata.

The governing principle is:

> **Every release of every governed catalog repo SHALL emit a release manifest to the federation registry. The registry is git-managed, schema-versioned, PR-reviewed, and is the producer-side counterpart to each repo's consumer-side `dependencies.yaml`.**

The Federation Release Registry therefore:

- lives in `dea-release-package/federation-registry/`, a directory of git-managed YAML files;
- stores one manifest per release, organised by `releases/<year>/<month>/<repo>-<tag>.yaml`;
- is append-only; existing manifests are immutable once published;
- is schema-versioned (`registry-schema@v1`); schema bumps are themselves CRs;
- is PR-reviewed; no manifest lands without a human or automated review;
- exposes a derived timeline (`timeline/<year>-<quarter>.yaml`) computed by the watchdog;
- is consumed by the Federation Watchdog (CR-DEA-RP-03) and the visibility surfaces (CR-DEA-RP-04).

The registry does NOT:

- replace any existing per-repo release pipeline (it extends them);
- store asset content (assets remain in the GitHub Release; the registry stores only metadata + checksums);
- act as a runtime data source for catalog consumers (consumers continue to use GitHub Releases);
- introduce a new persistence technology (it is plain git).

---

## 2. Why This Decision Is Necessary

A governed catalog repo's `dependencies.yaml` records its *consumer-side* view: "I depend on ECF pin X, metamodel pin Y, peer catalog Z at tag T." This is necessary but insufficient. The federation needs the *producer-side* counterpart: "On date D, repo R released tag T at commit C against pins X and Y, claiming compatibility with peer catalog Z at tag T." Without a producer-side registry:

- pin drift across sibling repos is invisible until a watchdog happens to look;
- asymmetric compatibility claims decay silently;
- release-note mandates are never reconciled against the target release's acknowledgement;
- the federation has no queryable history of "what was released when against what";

Today, no source of truth fills this role. Each catalog repo's GitHub Release is the only durable artifact, and Release pages are not designed for federation-wide relational queries.

---

## 3. Decision Drivers

The Federation Release Registry addresses:

1. **Producer-side relational integrity** : a single source of truth for "what got released when against what pins";
2. **Drift detection substrate** : the watchdog's pin-coherence and cross-version jobs read the registry;
3. **Mandate reconciliation** : release-note mandates can be audited against the target release's manifest;
4. **Federation history** : the registry IS the federation's release history;
5. **Append-only discipline** : once a release is published, its manifest is immutable historical evidence;
6. **Schema versioning** : schema bumps don't invalidate historical manifests (tolerant reading);
7. **PR-review discipline** : every manifest lands through a review surface;
8. **Storage discipline** : git-managed YAML keeps the registry on the same substrate as everything else in OpenDEA.

---

## 4. The Manifest Schema (registry-schema@v1)

### 4.1 Top-level shape

```yaml
# registry-schema: v1
# This file is immutable once committed under its tag.
release:
  repo: technehub-labs/dea-catalog-business-capabilities
  tag: v1-alpha.3
  commit_sha: <40-char>                 # the merge commit SHA; full, never abbreviated
  released_at: 2026-09-12T08:30:00Z
  ecf_pin: dea:ecf@1.0.0
  metamodel_pin: 1.0.0
  peer_pins:
    dea-catalog-processes: v0.4.2
    dea-catalog-business-objects: v0.2.0
  compatibility:
    schema: compatible
    semantic: compatible
    pin_alignment: compatible            # release-package-specific (RP-01 §7)
    asset_presence: compatible
    peer_pin_satisfaction: compatible
    release_note_consistency: compatible
  compatibility_claims:                 # authored by the releasing repo
    - target_repo: technehub-labs/dea-catalog-processes
      target_tag: v0.4.2
      relationship: compatible           # enum: compatible | requires | breaks | unknown
      evidence: "BPMN plugin validates against the same ECF coordinates"
      source: CR-DEA-BC-08 §4
    - target_repo: technehub-labs/dea-catalog-business-objects
      target_tag: v0.2.0
      relationship: requires
      evidence: "Business Capability v1-alpha.3 references 14 Business Objects"
      source: CATALOG.yaml#references
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
  asset_checksums:                       # SHA-256 of each asset in the GitHub Release
    capability-map.html: <sha256>
    capability-map-a0.png: <sha256>
    catalog.xlsx: <sha256>
    capability-booklet.pdf: <sha256>
    quickstart-booklet.pdf: <sha256>
    release-notes.md: <sha256>
    processes.bpmn: <sha256>
    contributions-and-decisions.zip: <sha256>
  drift_flags: []                        # populated by the watchdog
  registry_schema: v1                   # which schema version authored this manifest
  authoring_repo: technehub-labs/dea-catalog-business-capabilities
  authoring_workflow: publish-versioned.yml@<sha>
```

### 4.2 Compatibility claim vocabulary

The `compatibility_claims[].relationship` field uses a separate, smaller vocabulary than the `compatibility.*` axes. The axes (CR-DEA-RP-01 §7) are *axes* of self-declared compatibility; the claims are *directed* statements about a specific peer.

| Relationship | Meaning |
|---|---|
| `compatible` | This release works correctly with the target release at the target tag. |
| `requires` | This release cannot operate without the target release being at or beyond the target tag. |
| `breaks` | This release does NOT work with the target release at the target tag (the consumer must update). |
| `unknown` | The relationship has not been investigated. |

`unknown` is the default. Authors are not required to investigate every peer; the watchdog flags `unknown` claims older than 90 days.

### 4.3 Asset inventory

The `asset_inventory` field lists the count of each asset type in the GitHub Release. Counts of zero are valid (a catalog may not yet have a BPMN plugin); missing keys are invalid (every catalog's adoption CR defines its expected asset list; the manifest must enumerate them all).

The `asset_checksums` field is required for every asset present. Empty checksum value is invalid.

---

## 5. Storage Layout

```
dea-release-package/federation-registry/
├── README.md                                       # registry index (generated)
├── releases/
│   └── 2026/
│       └── 09/
│           ├── dea-catalog-business-capabilities-v1-alpha.3.yaml
│           ├── dea-catalog-processes-v0.4.2.yaml
│           └── dea-catalog-business-objects-v0.2.0.yaml
├── timeline/
│   └── 2026-Q3.yaml                                # generated by watchdog
└── schemas/
    ├── registry-schema-v1.schema.json
    └── registry-schema-v1.example.yaml
```

### 5.1 Filename convention

`<org>-<repo>-<tag>.yaml`, with all dots replaced by dashes to be filesystem-safe.

Examples:
- `dea-catalog-business-capabilities-v1-alpha-3.yaml`
- `dea-catalog-processes-v0-4-2.yaml`

### 5.2 Append-only invariant

Once a manifest is committed, its content is immutable. Corrections are made by:
- a new manifest at a new tag (the preferred path for substantive changes);
- a separate `drift_flags[]` entry recorded by the watchdog;
- a deprecation note in the registry README (only for schema-versioned corrections).

In-place edits are forbidden by the registry-validate workflow.

---

## 6. The BPMN Profile (Release-Plugin Profile)

For process catalog releases, the BPMN plugin file conforms to a published profile. The profile is a *subset* of OMG BPMN 2.0, defined to cover what the process catalog's data shape requires and no more.

| BPMN element | Profile status |
|---|---|
| `<bpmn:definitions>` | Required; one per file |
| `<bpmn:process>` | Required; one per process entity |
| `<bpmn:lane>` | Optional; mapped from process.specialization |
| `<bpmn:task>` | Required; mapped from process.steps |
| `<bpmn:startEvent>` | Required; one per process |
| `<bpmn:endEvent>` | Required; one per process |
| `<bpmn:sequenceFlow>` | Required; mapped from process.lineage |
| `<bpmn:dataObject>` | Optional; mapped from process.business_object_refs |
| `<bpmn:documentation>` | Required; carries the OpenDEA process definition + ECF coords |

Elements outside the profile (sub-processes, gateways, message flows, etc.) are rejected by the profile validator. The profile is published at `dea-release-package/standards/bpmn-profile.md` and versioned alongside the toolkit.

### 6.1 Profile validator

A standalone Python module, `dea_release_package.plugins.bpmn.validate()`, loads the BPMN file, walks the XML tree, and asserts that every element present is in the profile. The validator runs in:
- the per-repo pre-merge gate;
- the pre-release gate;
- the post-release watchdog's asset drift check.

---

## 7. The ArchiMate Profile (Release-Plugin Profile)

For business-capability catalog releases, the ArchiMate plugin file conforms to the Open Exchange XML format. The profile is intentionally minimal: one `<element>` per BC entity, with the ECF coordinates carried in `<property>` elements.

Profile definition: `dea-release-package/standards/archimate-profile.md`. Deferred to the BC catalog's per-repo adoption CR for full spec.

---

## 8. Cross-Repo Auth (Registry Writes)

Each catalog repo needs to write to `dea-release-package` on tag push. Three options were evaluated:

### Option A: PAT-based dispatch

Each catalog repo has a `REGISTRY_TOKEN` PAT scoped to `dea-release-package` with `Contents: Write`. Stored as a repo secret on the catalog repo. Reusable, low friction.

### Option B: GitHub App

A `dea-federation-bot` GitHub App installed on both source and registry repos. The app has narrow permissions. Best-practice auth model.

### Option C: PR-from-source

The catalog repo opens a PR against `dea-release-package` with the new manifest on tag push. No special auth; uses the standard `GITHUB_TOKEN`.

### Decision

**Phase 1 (transition): Option A** : PAT-based dispatch. Quick to ship; per-repo `REGISTRY_TOKEN` secret. Each catalog repo's `publish-versioned.yml` uses the PAT to push the manifest directly.

**Phase 2 (steady state): Option B** : GitHub App. The App is installed org-wide; per-repo PATs are deprecated. The App's permissions are narrower than PATs and can be audited centrally.

**Phase 3 (long term): Option C** : PR-from-source if and only if the PR-review latency is acceptable. The watchdog's tamper-evidence invariant is unchanged either way; the choice is about operational simplicity.

The transition from A → B → C is driven by CRs in `dea-release-package/change-requests/`. Each catalog repo's adoption CR names which phase it lands under.

---

## 9. Schema Versioning

### 9.1 Tolerant reading

When the registry schema evolves (`v1` → `v2`), the registry reader is **tolerant**:

- manifests authored against `v1` are still queryable;
- new fields in `v2` are absent in `v1` manifests and reported as `null` (or as "not declared");
- removed fields in `v2` are ignored in `v1` manifests;
- the `registry_schema` field on every manifest records which schema version authored it.

### 9.2 Strict writing

When the registry writer emits a new manifest, it MUST conform to the *current* schema version. The `registry-validate.yml` workflow enforces this on every PR to `federation-registry/`.

### 9.3 Schema bump process

Schema bumps are themselves CRs:
- propose the new schema in `federation-registry/schemas/registry-schema-v2.schema.json`;
- update the writer in `toolkit/src/dea_release_package/registry/writer.py`;
- update the reader in `toolkit/src/dea_release_package/registry/reader.py` to handle both `v1` and `v2`;
- add a migration note to `federation-registry/schemas/MIGRATION-v1-to-v2.md`;
- backfill: existing `v1` manifests are NOT re-emitted; they remain authoritative historical evidence.

---

## 10. CI Workflows

### 10.1 `registry-validate.yml`

Triggered on PRs that touch `federation-registry/releases/`, `federation-registry/timeline/`, or `federation-registry/schemas/`.

```yaml
on:
  pull_request:
    paths:
      - 'federation-registry/**'

jobs:
  validate:
    steps:
      - checkout (fetch-depth: 0)
      - setup python
      - run: python -m dea_release_package.registry.validate --strict
              # Validates each touched manifest against the current schema
              # Asserts filename matches the manifest's release.repo + release.tag
              # Asserts no in-place edits to existing manifests (append-only)
              # Asserts asset_checksums matches the GitHub Release's checksums
      - run: python -m dea_release_package.registry.lint
              # Lints for missing fields, malformed timestamps, etc.
```

### 10.2 Reusable workflow for catalog repos

`.github/reusable-workflows/emit-release-manifest.yml` in `dea-release-package`, consumed by each catalog repo's `publish-versioned.yml`.

```yaml
# dea-release-package/.github/reusable-workflows/emit-release-manifest.yml
on:
  workflow_call:
    inputs:
      repo:
      tag:
      commit_sha:
      ...

jobs:
  emit-manifest:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup python
      - run: python -m dea_release_package.registry.emit \
          --repo ${{ inputs.repo }} \
          --tag ${{ inputs.tag }} \
          --commit-sha ${{ inputs.commit_sha }}
              # Pulls asset_checksums from the GitHub Release,
              # constructs the manifest, opens a PR against
              # dea-release-package/federation-registry/releases/<year>/<month>/
```

The catalog repo pins this reusable to a specific tag (`@v1.2.0`) and updates via bump PRs.

---

## 11. Consequences

### Positive

- A single source of truth records every release and its peer relationships.
- The watchdog has a substrate to query.
- PR review of every manifest catches authoring errors before they land.
- Schema versioning allows the registry to evolve without invalidating historical records.
- Git-managed YAML keeps the registry consistent with OpenDEA's "everything is a CR" discipline.

### Negative

- A new repo (`dea-release-package`) is bootstrapped in this CR's lifecycle.
- Cross-repo auth (Phase 1 PAT) introduces N credentials to manage; Phase 2 GitHub App installation is org-wide work.
- Append-only discipline means corrections are clumsier than in-place edits.
- Schema bumps require coordinated reader/writer updates; a careless bump can break consumers.

---

## 12. Rejected Alternatives

### A : External database

Use Postgres or another external DB for the registry.

Rejected because:

- Breaks the "everything is a CR" discipline.
- Introduces operational dependency (DB availability).
- Loses free PR review.

### B : Strict schema versioning

Old manifests must be re-emitted against the new schema before they're queryable.

Rejected because:

- Every historical release becomes a permanent maintenance burden.
- Historical manifests are evidence; rewriting them is rewriting history.

### C : Mandatory compatibility claim authorship per release

Every release MUST author claims for every known peer.

Rejected because:

- Many releases have no peer relationship to claim against.
- Forces busywork; better to flag stale `unknown` claims after a grace period.

### D : Single-file registry (one giant YAML)

All releases in a single file.

Rejected because:

- Merge conflicts on every release.
- PR review impossible for a single file with hundreds of entries.

### E : Registry writes via repository_dispatch event

Catalog repo fires `repository_dispatch` event; the registry repo has a listener workflow that creates the PR.

Rejected because:

- Requires the registry repo to have a workflow listening for the event.
- Same secret-management burden as PAT-based dispatch, with more moving parts.

---

## 13. Explicit Non-Decisions

This CR does NOT decide:

- The specific toolkit API surface (deferred to toolkit design);
- The exact cross-repo auth model per catalog repo (each adoption CR names Phase 1/2/3);
- The registry README's auto-generated index layout (deferred to Sub-system 4);
- The watchdog's specific jobs (CR-DEA-RP-03);
- The compatibility annex format in release notes (CR-DEA-RP-04).

---

## 14. Decision Summary

The Federation Release Registry:

- lives in `dea-release-package/federation-registry/`;
- stores one git-managed YAML manifest per release;
- is append-only, schema-versioned, PR-reviewed;
- feeds the watchdog (CR-DEA-RP-03) and visibility surfaces (CR-DEA-RP-04);
- adopts the CR-AM-02 §11 compatibility-axis shape with four release-package-specific axes;
- uses cross-repo auth that transitions from PAT (Phase 1) to GitHub App (Phase 2) to PR-from-source (Phase 3, optional).

---

## 15. Required Follow-On CRs

- **CR-DEA-RP-03** : Federation Watchdog; consumes the registry.
- **CR-DEA-RP-04** : Visibility Surfaces; consumes the registry for the index page and release-note annexes.
- **ADR-DEA-RP-02** : Registry Schema; design specification for the schema.
- **Per-catalog adoption CRs** : each catalog repo's manifest emit flow.

---

*Status: Proposed. Parent: CR-DEA-RP-01 (Release Package Program). Compatibility axes adopted from CR-AM-02 §11.*