# BPMN Profile

This standard defines the BPMN 2.0 subset used by the Release Package Program for process catalog plugin files. The profile is intentionally minimal: it covers what the process catalog's data shape requires and no more.

## Version

`1.0.0`; defined by `CR-DEA-RP-02` §6. Profile bumps are CRs.

## Profile Elements

| Element | Status | Mapping |
|---|---|---|
| `<bpmn:definitions>` | Required | One per file; carries the namespace declarations and `dea:bpmnProfile` attribute. |
| `<bpmn:process>` | Required | One per process entity; `id` = process entity id. |
| `<bpmn:lane>` | Optional | Mapped from process.specialization. |
| `<bpmn:task>` | Required | Mapped from process.steps; one per step. |
| `<bpmn:startEvent>` | Required | One per process; single entry point. |
| `<bpmn:endEvent>` | Required | One per process; single exit point. |
| `<bpmn:sequenceFlow>` | Required | Mapped from process.lineage. |
| `<bpmn:dataObject>` | Optional | Mapped from process.business_object_refs. |
| `<bpmn:documentation>` | Required | Carries the OpenDEA process definition + ECF coords. |

## Profile Version Embedding

Every BPMN file carries a `dea:bpmnProfile` attribute on `<bpmn:definitions>`:

```xml
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  xmlns:dea="http://technehub-labs.github.io/dea/bpmn/1.0"
                  dea:bpmnProfile="1.0.0"
                  id="dea-catalog-processes-v0-4-2"
                  targetNamespace="http://technehub-labs.github.io/dea/catalog/processes/v0.4.2">
```

Consumers and the watchdog read this attribute to verify the profile version.

## Validator

`dea_release_package.plugins.bpmn.validate()` walks the XML tree and asserts every element present is in the profile. Validation runs in:

- the per-repo pre-merge gate;
- the pre-release gate;
- the watchdog's asset drift check.

The validator emits a structured report:

```yaml
profile_version: 1.0.0
elements_present:
  - bpmn:definitions
  - bpmn:process
  - bpmn:startEvent
  - bpmn:endEvent
  - bpmn:task
  - bpmn:sequenceFlow
  - bpmn:documentation
elements_out_of_profile: []
status: pass
```

## Profile Extension Protocol

When the process catalog's data shape needs a new BPMN element (e.g. `<bpmn:exclusiveGateway>`), the extension follows a CR (`CR-DEA-RP-07` or similar) that:

1. Bumps the profile to `1.1.0` (or appropriate minor).
3. Updates the validator to recognise the new element.
4. Documents the extension in this standard.
5. Adds the new element to the engine compatibility matrix (`bpmn-engine-compatibility.yaml`).

Old releases remain valid against the new profile. Consumers can opt into the new profile at their own pace.

## BPMN Engine Compatibility Matrix

The toolkit ships `toolkit/src/dea_release_package/plugins/bpmn/engine-compatibility.yaml`:

```yaml
profile_version: 1.0.0
engines:
  - engine: camunda-7
    support: full
    notes: "All profile elements supported; sub-processes not used."
  - engine: bpmn.io
    support: full
    notes: "Viewer renders all profile elements."
  - engine: flowable
    support: full
    notes: "All profile elements supported."
```

The matrix is updated when the profile changes or when new engines are tested.

## Reference BPMN Example

```xml
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  xmlns:dea="http://technehub-labs.github.io/dea/bpmn/1.0"
                  dea:bpmnProfile="1.0.0"
                  id="manage-customer-relationship"
                  targetNamespace="http://technehub-labs.github.io/dea/catalog/processes/manage-customer-relationship">

  <bpmn:process id="manage-customer-relationship" name="Manage Customer Relationship" isExecutable="false">
    <bpmn:documentation>
      <![CDATA[
        OpenDEA Process: Manage Customer Relationship
        Definition: The process by which an enterprise establishes, maintains, and concludes
        its commercial relationships with customers.
        ECF Coordinates: ecf:agencyAndOrganization.manage
        Process ID: dea:process-manage-customer-relationship
      ]]>
    </bpmn:documentation>

    <bpmn:startEvent id="start" name="Customer Enters Relationship"/>
    <bpmn:task id="identify" name="Identify Customer"/>
    <bpmn:task id="onboard" name="Onboard Customer"/>
    <bpmn:task id="maintain" name="Maintain Relationship"/>
    <bpmn:endEvent id="end" name="Customer Exits Relationship"/>

    <bpmn:sequenceFlow id="s1" sourceRef="start" targetRef="identify"/>
    <bpmn:sequenceFlow id="s2" sourceRef="identify" targetRef="onboard"/>
    <bpmn:sequenceFlow id="s3" sourceRef="onboard" targetRef="maintain"/>
    <bpmn:sequenceFlow id="s4" sourceRef="maintain" targetRef="end"/>
  </bpmn:process>
</bpmn:definitions>
```

## Status

**Scaffold** : the profile is defined in `CR-DEA-RP-02` §6; this standard is the detailed reference. The reference example above is illustrative; the toolkit's BPMN generator ships with the production reference.