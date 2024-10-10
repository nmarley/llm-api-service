from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
import anthropic
import json
import logging
import sys

from .exceptions import InvalidModelError, ConfigurationError, ServerError
from .llm_interface import BaseLLMAPI
from .models import MODELS
from .tools import tool_registry, Tool
from .types import Usage, Costs, CallAPIResult


class AnthropicAPI(BaseLLMAPI):
    PROVIDER = "anthropic"

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

        # Anthropic API initialization, uses ANTHROPIC_API_KEY env var
        load_dotenv()
        self.client = anthropic.Anthropic()
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

            if not all([costs.get("input"), costs.get("output")]):
                raise ConfigurationError(
                    f"Cost information incomplete for model '{model}'"
                )

            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                tools=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.json_schema,
                    }
                ],
                tool_choice={"type": "tool", "name": f"{tool.name}"},
                system=system,
                messages=messages,
            )

            # usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # costs
            input_cost = Decimal(input_tokens) * Decimal(costs.get("input"))
            output_cost = Decimal(output_tokens) * Decimal(costs.get("output"))
            total_cost = input_cost + output_cost

            # result object
            result = CallAPIResult(
                model=response.model,
                usage=Usage(input_tokens=input_tokens, output_tokens=output_tokens),
                costs=Costs(
                    input_token_cost=Decimal(costs.get("input")),
                    output_token_cost=Decimal(costs.get("output")),
                    input_cost=input_cost,
                    output_cost=output_cost,
                    total_cost=total_cost,
                ),
                timestamp=datetime.utcnow(),
                result=response.content[0].input,
            )
            return result

        except anthropic.APIError as e:
            # provider API errors
            raise ServerError(str(e))
        except Exception as e:
            # Unexpected errors
            raise ServerError(f"Unexpected error: {str(e)}")
