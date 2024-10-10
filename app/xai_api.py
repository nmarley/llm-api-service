from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
import json
import logging
import openai
import os
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


class xAIAPI(BaseLLMAPI):
    PROVIDER = "xai"

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

        # xAI API initialization, uses XAI_API_KEY env var
        load_dotenv()
        XAI_API_KEY = os.getenv("XAI_API_KEY")
        self.client = openai.OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",
        )
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

            # Add the system message to the beginning of the messages list
            if messages is None:
                messages = []
            messages = [{"role": "system", "content": system}] + messages

            # xAI docs for producing structured data:
            # https://docs.x.ai/docs/guides/structured-outputs#defining-json-schema

            completion = self.client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=tool.pydantic_model,
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

            result_json_string = message.content
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
                timestamp=datetime.utcnow(),
                result=result_obj,
            )
            return result

        except openai.APIError as e:
            # provider API errors
            raise ServerError(str(e))
        except Exception as e:
            # Unexpected errors
            raise ServerError(f"Unexpected error: {str(e)}")
