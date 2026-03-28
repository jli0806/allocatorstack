"""Verification gates between pipeline steps.

Gates check agent outputs against configurable rules:
- Required fields populated
- Numerical values within plausible ranges
- Cross-referenced values match across sources

Gates can be blocking (stop pipeline) or advisory (flag for human review).
Implements CPP Investments' five-gate verification model.
"""

from __future__ import annotations


class VerificationGate:
    """Configurable check between pipeline steps."""

    pass
