"""Engine plugin generators.

Currently supports BPMN 2.0 (process catalog) and ArchiMate 3.2 (BC catalog).
Each plugin has a generator, a validator, and a profile definition.

Implementation: CR-DEA-RP-02 §6 (BPMN) and §7 (ArchiMate).
"""

from dea_release_package.plugins import bpmn, archimate

__all__ = ["bpmn", "archimate"]
__status__ = "scaffold"