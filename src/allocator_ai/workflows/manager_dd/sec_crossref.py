"""SEC/FINRA cross-referencing.

Checks manager claims from DDQs and pitch books against public data:
SEC EDGAR ADV filings, FINRA BrokerCheck, enforcement actions.
Flags discrepancies between self-reported and public data.
"""

from __future__ import annotations
