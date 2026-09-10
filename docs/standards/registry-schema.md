# Registry Schema (registry-schema@v1)

This standard defines the canonical shape of a release manifest in the Federation Release Registry.

## Version

`v1`; defined by CR-DEA-RP-02 §4. Schema bumps are CRs; this document is the authoritative reference for `v1` until a new schema CR lands.

## Top-Level Shape

```yaml
registry_schema: v1                # REQUIRED: which schema version authored this manifest

release:
  repo: technehub-labs/dea-catalog-business-capabilities    # REQUIRED
  tag: v1-alpha.3                                            # REQUIRED
  commit_sha: <40-char>                                      # REQUIRED: full SHA, never abbreviated
  released_at: 2026-09-12T08:30:00Z                          # REQUIRED: ISO-8601 UTC

  ecf_pin: dea:ecf@1.0.0                                      # REQUIRED
  metamodel_pin: 1.0.0                                       # REQUIRED

  peer_pins:                                                  # OPTIONAL but recommended
    dea-catalog-processes: v0.4.2
    dea-catalog-business-objects: v0.2.0

  compatibility:                                              # REQUIRED: six axes
    schema: compatible                # CR-AM-02 §11 axis
    semantic: compatible              # CR-AM-02 §11 axis
    pin_alignment: unknown            # CR-DEA-RP-01 §7 axis
    asset_presence: unknown           # CR-DEA-RP-01 §7 axis
    peer_pin_satisfaction: unknown    # CR-DEA-RP-01 §7 axis
    release_note_consistency: unknown # CR-DEA-RP-01 §7 axis

  compatibility_claims:                # OPTIONAL: directed claims about specific peer tags
    - target_repo: technehub-labs/dea-catalog-processes
      target_tag: v0.4.2
      relationship: compatible         # enum: compatible | requires | breaks | unknown
      evidence: "BPMN plugin validates against the same ECF coordinates"
      source: CR-DEA-BC-08 §4

  asset_inventory:                     # REQUIRED: count of each asset type
    html: 1
    png_a0: 1
    png_a3: 1
    xlsx: 1
    booklet_long: 1
    booklet_short: 1
    release_notes: 1
    plugin_files: 1
    contributions_snapshot: 1

  asset_checksums:                     # REQUIRED for every present asset
    capability-map.html: <sha256>
    capability-map-a0.png: <sha256>
    catalog.xlsx: <sha256>
    capability-booklet.pdf: <sha256>
    quickstart-booklet.pdf: <sha256>
    release-notes.md: <sha256>
    processes.bpmn: <sha256>
    contributions-and-decisions.zip: <sha256>

  drift_flags: []                      # populated by the watchdog; empty on authoring
```

## Field Constraints

| Field | Constraint |
|---|---|
| `release.repo` | MUST match `<org>/<repo>` for a `technehub-labs/dea-catalog-*` repo. |
| `release.tag` | MUST match `vX[.Y[.Z]][-(alpha|beta|rc).N]` per OpenDEA SemVer. |
| `release.commit_sha` | MUST be exactly 40 lowercase hex chars. |
| `release.released_at` | MUST be ISO-8601 UTC. |
| `release.ecf_pin` | MUST match `dea:ecf@X.Y.Z` per the metaframework's ECF pinning rule. |
| `release.metamodel_pin` | MUST match `X.Y.Z` per the metamodel's versioning rule. |
| `release.compatibility.*` | MUST be one of `compatible`, `incompatible`, `unknown`. |
| `release.compatibility_claims[].relationship` | MUST be one of `compatible`, `requires`, `breaks`, `unknown`. |
| `release.asset_inventory` | MUST list every asset type expected by the catalog's adoption CR. |
| `release.asset_checksums` | MUST have one entry per present asset; SHA-256 hex string. |
| `registry_schema` | MUST be `v1` for manifests under this schema. |

## Tolerant Reading

When the schema evolves (`v1` → `v2`), the registry reader handles historical manifests:

- New fields in `v2` are absent in `v1` manifests and reported as `null`.
- Removed fields in `v2` are ignored in `v1` manifests.
- Renamed fields in `v2` map to their `v1` names via the reader's migration table.

## Strict Writing

The writer MUST conform to the current schema version. The `registry-validate.yml` workflow enforces this on every PR.

## Compatibility Vocabulary Alignment

The `release.compatibility.*` block is composed of two vocabularies:

- **CR-AM-02 §11 axes** (`schema`, `semantic`) : model-version compatibility, governed by `dea-metamodel/assessment-models/vocabulary/compatibility-types.yaml`.
- **CR-DEA-RP-01 §7 axes** (`pin_alignment`, `asset_presence`, `peer_pin_satisfaction`, `release_note_consistency`) : release-package-specific axes.

A manifest MAY carry additional CR-AM-02 §11 axes (`scoring`, `maturity`, `result`, `benchmark`) if the catalog participates in the assessment-metamodel program. These are optional under the release-package vocabulary but required under CR-AM-02 if the assessment axis applies.

## Validation

The `dea_release_package.registry.validate` module enforces this schema. Validation runs in:

- `registry-validate.yml` (PR-time on this repo);
- the catalog repo's `publish-versioned.yml` (release-time);
- the watchdog's `asset-drift` job (post-release audit).

## Schema Bump Process

1. Open a CR (`CR-DEA-RP-NN`) proposing the bump.
2. Add `federation-registry/schemas/registry-schema-vN.schema.json` with the new schema.
3. Update `dea_release_package.registry.writer` to emit `vN`.
4. Update `dea_release_package.registry.reader` to handle both `vN-1` and `vN` (tolerance).
5. Add a migration note at `federation-registry/schemas/MIGRATION-v(N-1)-to-vN.md`.
6. Existing manifests are NOT re-emitted; they remain authoritative historical evidence.