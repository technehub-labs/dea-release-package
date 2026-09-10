# Federation Registry

This directory is the **Federation Release Registry**: a git-managed, schema-versioned, PR-reviewed source of truth for cross-repo release metadata.

The registry is the producer-side counterpart to each catalog repo's consumer-side `dependencies.yaml`. It records what got released when against what pins, with what compatibility claims, with what asset checksums.

## Layout

```
federation-registry/
├── README.md                           # Registry Index Page (auto-generated; Sub-system 4)
├── releases/<year>/<month>/            # one manifest per release (append-only)
├── timeline/<year>-<quarter>.yaml      # generated timeline + dependency graph
└── schemas/                            # registry-schema versions
```

## Manifest Filename Convention

`<org>-<repo>-<tag>.yaml` with dots replaced by dashes.

Examples:
- `dea-catalog-business-capabilities-v1-alpha-3.yaml`
- `dea-catalog-processes-v0-4-2.yaml`

## Schema Versioning

The current schema version is `v1` (per `CR-DEA-RP-02`). Schema bumps are CRs.

## Append-Only Discipline

Manifests are immutable once committed. Corrections are made via:
- a new manifest at a new tag (preferred for substantive changes);
- a `drift_flags[]` entry recorded by the watchdog;
- a deprecation note in the registry README.

In-place edits are forbidden by the `registry-validate.yml` workflow.

## How to Add a Manifest

The catalog repo's `publish-versioned.yml` opens a PR to `federation-registry/releases/<year>/<month>/` on tag push. The PR is reviewed; `registry-validate.yml` checks the manifest against `schemas/registry-schema-v1.schema.json` and validates asset checksums against the GitHub Release.

## How to Read a Manifest

```python
from dea_release_package.registry import reader
release = reader.read("federation-registry/releases/2026/09/dea-catalog-business-capabilities-v1-alpha-3.yaml")
print(release.tag, release.compatibility.pin_alignment)
```

## Status Definitions

- **Scaffold** : directory layout in place; no manifests yet.
- **Active** : manifests populating; watchdog running.