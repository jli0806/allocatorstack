"""Shared workflow context with provenance tracking.

The WorkflowContext flows through the pipeline. Each agent reads from it and writes
to it. Every write includes a ProvenanceRecord (source file, page/row, extraction
method, confidence level).
"""

from __future__ import annotations


class WorkflowContext:
    """Central state object passed between pipeline agents."""

    pass
