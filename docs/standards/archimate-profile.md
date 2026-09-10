# ArchiMate Profile

**Status:** Planned. Will be drafted when the BC catalog's adoption CR (`CR-DEA-BC-RP-01`) lands.

## Outline

- Conforms to ArchiMate 3.2 Open Exchange XML.
- One `<element>` per BC entity; ECF coordinates carried in `<property>` elements.
- Minimal profile (full spec deferred to BC catalog's adoption CR).
- Validator mirrors `dea_release_package.plugins.bpmn.validate()` shape.
- Engine compatibility matrix mirrors `bpmn-engine-compatibility.yaml`.

## Reference

- `CR-DEA-RP-02` §7 (ArchimMate Profile)
- `bpmn-profile.md` (sister standard for the process catalog)