"""Agent registry and discovery.

Agents register themselves by name. The pipeline resolves agent references
in YAML configs to actual agent classes via the registry.
"""

from __future__ import annotations


class AgentRegistry:
    """Maps agent names to agent classes."""

    pass
