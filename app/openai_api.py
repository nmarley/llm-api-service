from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
import json
import logging
import openai
import sys

from .exceptions import (
    ConfigurationError,
    InvalidModelError,
    LLMRefusalError,
    ServerError,
)
from .llm_interface import BaseLLMAPI
from .models import MODELS
from .tools import tool_registry, Tool
from .types import Usage, Costs, CallAPIResult


def get_message_content(message) -> Optional[str]:
    if message.content:
        return message.content
    if message.function_call:
        return message.function_call.arguments
    return None


class OpenAIAPI(BaseLLMAPI):
    PROVIDER = "openai"

    def __init__(self):
        super().__init__()

        provider_models = MODELS.get(self.PROVIDER, {})
        if not provider_models:
            raise ConfigurationError(f"No models found for provider {self.PROVIDER}")

        self.DEFAULT_MODEL = provider_models.get("default_model", None)
        if not self.DEFAULT_MODEL:
            raise ConfigurationError(
                f"No default model found for provider {self.PROVIDER}"
            )

        self.models = provider_models.get("models", {})
        self.VALID_MODELS = frozenset(self.models.keys())

        # OpenAI API initialization, uses OPENAI_API_KEY env var
        load_dotenv()
        self.client = openai.OpenAI()
        self.tool_map = tool_registry.get_tool_map()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

    def call_api(
        self,
        max_tokens: int,
        model: str,
        tool: Tool,
        system: str,
        messages: list,
        **kwargs,
    ) -> Dict[str, Any]:
        model = model or self.DEFAULT_MODEL
        if model not in self.VALID_MODELS:
            raise InvalidModelError(
                f"Invalid model: '{model}' for provider '{self.PROVIDER}'"
            )

        try:
            model_info = self.models[model]
            costs = model_info.get("costs", {})
            capabilities = model_info.get("capabilities", {})

            if not all([costs.get("input"), costs.get("output")]):
                raise ConfigurationError(
                    f"Cost information incomplete for model '{model}'"
                )

            # Add the system message to the beginning of the messages list
            if messages is None:
                messages = []
            messages = [{"role": "system", "content": system}] + messages

            completion = None
            has_structured_outputs = capabilities.get("structured_outputs", False)

            if has_structured_outputs:
                completion = self.client.beta.chat.completions.parse(
                    model=model,
                    messages=messages,
                    max_completion_tokens=max_tokens,
                    response_format=tool.pydantic_model,
                )
            else:
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    functions=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.json_schema,
                        }
                    ],
                    function_call={"name": tool.name},
                    max_completion_tokens=max_tokens,
                )

            # usage
            input_tokens = completion.usage.prompt_tokens
            output_tokens = completion.usage.completion_tokens

            # costs
            input_cost = Decimal(input_tokens) * Decimal(costs.get("input"))
            output_cost = Decimal(output_tokens) * Decimal(costs.get("output"))
            total_cost = input_cost + output_cost

            message = completion.choices[0].message
            if message.refusal:
                raise LLMRefusalError(message.refusal)

            result_json_string = get_message_content(message)
            if result_json_string is None:
                raise ServerError(f"Unexpected response from OpenAI API: {message}")

            # load the JSON string into a Python object so we can serialize it
            # back later in the larger result object, without double-encoding
            # the JSON
            result_obj = json.loads(result_json_string)

            # result object
            result = CallAPIResult(
                model=completion.model,
                usage=Usage(input_tokens=input_tokens, output_tokens=output_tokens),
                costs=Costs(
                    input_token_cost=Decimal(costs.get("input")),
                    output_token_cost=Decimal(costs.get("output")),
                    input_cost=input_cost,
                    output_cost=output_cost,
                    total_cost=total_cost,
                ),
                result=result_obj,
                timestamp=datetime.utcnow(),
            )
            return result

        except openai.APIError as e:
            # provider API errors
            raise ServerError(str(e))
        except Exception as e:
            # Unexpected errors
            raise ServerError(f"Unexpected error: {str(e)}")
