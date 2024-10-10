from ..tool import Tool
from typing import Literal
from pydantic import BaseModel

__all__ = ["email"]


class EmailResponse(BaseModel):
    subject: str
    body: str
    tone: Literal["formal", "semi-formal", "casual", "friendly"]
    enthusiasm_level: Literal["low", "medium", "high"]


_name = "email"
_description = "Parse an email and generate an appropriate response."
_system = """
You are an expert at parsing emails and crafting professional responses. When processing this task, ensure all fields are properly formatted as JSON. For arrays always use proper JSON array notation, even if there's only one item. If a piece of information is unknown, use null for optional fields or an empty string for required string fields.

Follow these guidelines:

- Accurately extract key information from the email.
- Generate a response that matches the tone, length, and depth of the original email.
- Maintain a positive and professional tone in the response.
- Keep the response concise and conversational, avoiding formal language or buzzwords.
- Address key points and questions raised in the original email without being exhaustive.
- Express interest and enthusiasm without over-committing or appearing desperate.
- If multiple items are mentioned, acknowledge them briefly.
- Do not invent or assume any information not provided in the original email.

Pay special attention to all names, dates and contact information, and remember not to make anything up.
"""

_user = """
Please parse the following body of an email and generate a suitable professional response, paying special attention to the tone and content of the original email. You MAY NOT make up information that is not found in the input.

<email_body>
{email_body}
</email_body>
"""

email = Tool(
    name=_name,
    description=_description,
    pydantic_model=EmailResponse,
    system_prompt=_system,
    user_prompt_template=_user,
)
