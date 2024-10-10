from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from .tools import Tool
from .exceptions import ConfigurationError


class LLMInterface(ABC):
    DEFAULT_MODEL: str
    VALID_MODELS: frozenset

    @abstractmethod
    def call_api(
        self,
        max_tokens: int,
        model: str,
        tools: list,
        system: str,
        messages: list,
        **kwargs,
    ) -> Dict[str, Any]:
        pass


class BaseLLMAPI(LLMInterface):
    def __init__(self):
        self.tool_map = None
        self.logger = None

    def valid_models(self) -> List[str]:
        return list(self.VALID_MODELS)

    def is_valid_model(self, model: str) -> bool:
        return model in self.VALID_MODELS

    def _get_tool(self, name: str) -> Tool:
        tool = self.tool_map.get(name)
        if not tool:
            raise ConfigurationError(f"Tool '{name}' not found")
        return tool

    def _prepare_api_call(
        self, tool_name: str, content: Dict[str, str], model: Optional[str] = None
    ) -> Dict[str, Any]:
        if model is None or not self.is_valid_model(model):
            if model is not None:
                self.logger.warning(
                    f"Invalid model '{model}' specified, using default model '{self.DEFAULT_MODEL}'"
                )
            model = self.DEFAULT_MODEL

        tool = self._get_tool(tool_name)
        system = tool.system_prompt
        user_prompt = tool.user_prompt_template.format(**content)

        # TODO: Pydantic type
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                ],
            },
        ]

        # TODO: Pydantic type
        return {
            "max_tokens": 2048,
            "model": model,
            "tool": tool,
            "system": system,
            "messages": messages,
        }

    def generate_email_response(
        self,
        email_body: str,
        model: Optional[str] = None,
    ) -> str:
        api_params = self._prepare_api_call(
            "email",
            {
                "email_body": email_body,
            },
            model,
        )
        api_params["max_tokens"] = 4096
        return self.call_api(**api_params)

    def rewrite_message(
        self,
        message_content: str,
        model: Optional[str] = None,
    ) -> str:
        api_params = self._prepare_api_call(
            "message_rewrite",
            {
                "message_content": message_content,
            },
            model,
        )
        api_params["max_tokens"] = 4096
        return self.call_api(**api_params)

    def basic_prompt_response(self, prompt: str, model: Optional[str] = None) -> str:
        api_params = self._prepare_api_call(
            "prompt_response",
            {"prompt": prompt},
            model,
        )
        api_params["max_tokens"] = 4096
        return self.call_api(**api_params)

    def summarize_text(self, text_body: str, model: Optional[str] = None) -> str:
        api_params = self._prepare_api_call(
            "text_summary",
            {"text_body": text_body},
            model,
        )
        api_params["max_tokens"] = 4096
        return self.call_api(**api_params)


__all__ = ["BaseLLMAPI"]
