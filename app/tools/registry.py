from typing import Dict

from .tool import Tool

__all__ = ["ToolRegistry"]


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get_tool_map(self) -> Dict[str, Tool]:
        return self.tools
