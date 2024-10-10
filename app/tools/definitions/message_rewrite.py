from ..tool import Tool
from typing import List, Optional
from pydantic import BaseModel, Field

__all__ = ["message_rewrite"]


class RewrittenMessage(BaseModel):
    rewritten_message: str = Field(
        ..., description="The professionally rewritten message"
    )


_name = "message_rewrite"
_description = (
    "Rewrite a message in a professional tone while preserving the main points."
)
_system = """
You are an expert at improving written communication. When rewriting messages, follow these guidelines:

- Maintain a professional and polite tone while preserving the original message's intent
- Focus on matching the tone and style of the original message
- Improve clarity and structure while keeping the authentic voice
- Ensure proper grammar and punctuation
- Keep the message concise and well-organized
- Preserve all key points and important details from the original message
- Do not add new information or change the meaning of the original message
- Try and avoid using filler words like "very", "really", etc. that don't add value to the message
"""

_user = "Please rewrite the following message in a more professional tone while maintaining all the key points: <message>{message_content}</message>"

message_rewrite = Tool(
    name=_name,
    description=_description,
    pydantic_model=RewrittenMessage,
    system_prompt=_system,
    user_prompt_template=_user,
)
