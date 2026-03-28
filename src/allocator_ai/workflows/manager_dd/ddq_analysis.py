"""Step 3: DDQ ingestion and analysis agent.

The highest-value, most complex module. Tiered extraction approach:
- Tier 1 (rule-based): ILPA/AIMA template DDQs with standard numbering
- Tier 2 (LLM-assisted): Semi-structured DDQs with non-standard numbering
- Tier 3 (LLM-heavy): Free-form narrative DDQs, confidence-scored

Produces structured Q&A pairs mapped to the ILPA/AIMA taxonomy,
side-by-side comparison views, and gap detection.
"""

from __future__ import annotations
