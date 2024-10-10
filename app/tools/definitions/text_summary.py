from ..tool import Tool
from typing import List, Optional
from pydantic import BaseModel, Field

__all__ = ["text_summary"]


class TextSummary(BaseModel):
    text_summary: str = Field(..., description="The summary of the given text")


_name = "text_summary"
_description = "Summarize a given text into a concise and informative summary."
_system = """
You are an expert at summarizing long bodies of text into concise and informative summaries, using bullet points if necessary.
"""

_user = """
Please read and summarize the following text, maintaining all the key points and general gist of the text: <text_body>{text_body}</text_body>
"""

text_summary = Tool(
    name=_name,
    description=_description,
    pydantic_model=TextSummary,
    system_prompt=_system,
    user_prompt_template=_user,
)
