from .xai import XAI
from .anthropic import ANTHROPIC
from .openai import OPENAI

MODELS = {
    "xai": XAI,
    "openai": OPENAI,
    "anthropic": ANTHROPIC,
}

__all__ = ["MODELS"]
