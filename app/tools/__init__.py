from .tool import Tool
from .registry import ToolRegistry
from .definitions import (
    email,
    message_rewrite,
    prompt_response,
    text_summary,
)

# Register tool configurations
tool_registry = ToolRegistry()

tool_registry.register(email)
tool_registry.register(message_rewrite)
tool_registry.register(prompt_response)
tool_registry.register(text_summary)

__all__ = [
    "Tool",
    "tool_registry",
]
