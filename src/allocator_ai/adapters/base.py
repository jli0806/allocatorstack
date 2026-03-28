"""Abstract data adapter interface.

All data adapters implement this interface. Institutions implement the adapter
for their specific data source (Bloomberg, eVestment, Preqin, or CSV exports).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class DataAdapter(ABC):
    """Base class for all data source adapters."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source."""
        ...

    @abstractmethod
    def query_managers(self, criteria: dict) -> list[dict]:
        """Query managers matching the given criteria."""
        ...
