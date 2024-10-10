from typing import Dict, Any, Type
from pydantic import BaseModel

"""
Tool is a class that stores the configurations for each tool, e.g. the input
schema and description of the tool
"""

__all__ = ["Tool"]


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        pydantic_model: Type[BaseModel],
        system_prompt: str,
        user_prompt_template: str,
    ):
        self.name = name
        self.description = description
        self.pydantic_model = pydantic_model
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template
        # Cache the JSON schema since it won't change
        self._json_schema = self.pydantic_model.model_json_schema()

    @property
    def json_schema(self) -> Dict[str, Any]:
        return self._json_schema

    # these are needed to make the Tool class hashable, so that it can be added
    # to a set
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
