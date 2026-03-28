"""Source tracking for every data point in agent outputs.

Every number, claim, or extracted value must trace back to its source:
file path, page number, row/column, extraction method, and confidence level.
"""

from __future__ import annotations


class ProvenanceRecord:
    """Tracks the origin of a single data point."""

    pass
