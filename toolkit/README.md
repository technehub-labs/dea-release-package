# dea-release-package toolkit

The shared Python toolkit that produces release-package assets and validates them.

## Module Index

| Module | Purpose | CR |
|---|---|---|
| `ecf_map` | ECF-backdrop rendering (HTML + A0 PNG + A3 PNG) | CR-DEA-RP-01 §4.1 |
| `excel_flat_view` | Catalog-specific Excel schemas | CR-DEA-RP-01 §4.1 |
| `booklet` | Pandoc/WeasyPrint booklet generators | CR-DEA-RP-01 §4.1 |
| `plugins.bpmn` | BPMN 2.0 generator + validator + profile | CR-DEA-RP-02 §6 |
| `plugins.archimate` | ArchiMate 3.2 generator + profile | CR-DEA-RP-02 §7 |
| `snapshot` | contributions-and-decisions snapshotter | CR-DEA-RP-01 §4.1 |
| `registry` | Federation Registry producer/consumer | CR-DEA-RP-02 §4 |
| `watchdog` | Pin coherence, cross-version, asset drift | CR-DEA-RP-03 |
| `visibility` | Registry Index Page + Release Note Annex | CR-DEA-RP-04 |

## CLI Entry Points

```python
# Build a release package (catalog repo side)
python -m dea_release_package.cli build-package <repo> <tag>

# Validate a release package (catalog repo CI)
python -m dea_release_package.cli validate-package <repo> <tag> [--strict]

# Emit a release manifest (catalog repo on tag push)
python -m dea_release_package.cli emit-manifest <repo> <tag> <commit-sha>

# Watchdog jobs (dea-release-package CI)
python -m dea_release_package.cli watchdog pin-coherence
python -m dea_release_package.cli watchdog cross-version
python -m dea_release_package.cli watchdog asset-drift
python -m dea_release_package.cli watchdog timeline
python -m dea_release_package.cli watchdog resolve

# Visibility surfaces (dea-release-package CI)
python -m dea_release_package.cli visibility index
python -m dea_release_package.cli visibility annex --repo <repo> --tag <tag>
```

## Status

**Scaffold** : module structure in place; implementation lands when `CR-DEA-RP-01` is accepted.