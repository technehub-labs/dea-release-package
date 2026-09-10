"""Federation Registry producer/consumer.

`emit()` produces a release manifest from a tag-push event.
`validate()` validates a manifest against `registry-schema@v1`.
`reader.read()` is tolerant: handles `v1` (and future) manifests.

Implementation: CR-DEA-RP-02 §4, §10.

Status: scaffold; implementation lands when CR-DEA-RP-01 is accepted.
"""

__status__ = "scaffold"