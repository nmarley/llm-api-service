from ..tool import Tool
from typing import List, Optional
from pydantic import BaseModel, Field

__all__ = ["prompt_response"]


class Response(BaseModel):
    summary: str = Field(
        ...,
        description="Response to the user's prompt",
    )


_name = "prompt_response"
_description = "Respond to the prompt"
_system = "You are an LLM responding to a user's prompt"
_user = "{prompt}"

prompt_response = Tool(
    name=_name,
    description=_description,
    pydantic_model=Response,
    system_prompt=_system,
    user_prompt_template=_user,
)
