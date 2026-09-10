# Processes Release Package : Reference Implementation

**Status:** Planned. Will be the process catalog's adoption example when `CR-DEA-PC-RP-01` lands.

## Outline

This directory will contain:

- `profile.yaml`; process catalog's profile.
- `excel-schema.yaml`; the canonical Excel flat-view schema for processes (with lineage + version columns).
- `booklet-template/`; process-specific booklet template overrides.
- `bpmn/`; the process-specific BPMN generator config (per `bpmn-profile.md`).

## Reference

- `CR-DEA-RP-01` §6.1 (Sub-system 1)
- `CR-DEA-RP-02` §6 (BPMN Profile)
- `release-package-shape.md` (canonical asset list)