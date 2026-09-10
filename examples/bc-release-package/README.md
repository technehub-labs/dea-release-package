# BC Release Package : Reference Implementation

**Status:** Planned. Will be the BC catalog's adoption example when `CR-DEA-BC-RP-01` lands.

## Outline

This directory will contain:

- `profile.yaml`; BC catalog's profile (Excel column schema, booklet template overrides, plugin generator config).
- `excel-schema.yaml`; the canonical Excel flat-view schema for BC.
- `booklet-template/`; any BC-specific booklet template overrides.
- `bpmn/` (N/A; BC doesn't ship a BPMN plugin).
- `archimate/`; the BC-specific ArchiMate generator config (per `archimate-profile.md`).

## Reference

- `CR-DEA-RP-01` §6.1 (Sub-system 1)
- `CR-DEA-RP-02` §7 (ArchiMate Profile)
- `bpmn-profile.md` (sister standard for the process catalog)
- `release-package-shape.md` (canonical asset list)