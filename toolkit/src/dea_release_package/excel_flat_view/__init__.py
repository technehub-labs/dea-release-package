"""Catalog-specific Excel flat-view generator.

Produces the Excel workbook for a catalog repo's release package. Each
catalog has its own profile (column schema, sheet structure); profiles
live under `dea_release_package.excel_flat_view.profiles`.

Implementation: CR-DEA-RP-01 §4.1.

Status: scaffold; implementation lands when CR-DEA-RP-01 is accepted.
"""

__status__ = "scaffold"