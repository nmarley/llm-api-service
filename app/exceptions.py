class LLMAPIError(Exception):
    """Base exception for LLM API errors"""

    pass


class ClientError(LLMAPIError):
    """Errors caused by invalid client input (4xx)"""

    pass


class LLMRefusalError(ClientError):
    """LLM refused to process the request (e.g. content policy violation)"""

    pass


class ServerError(LLMAPIError):
    """Errors caused by API/server issues (5xx)"""

    pass


class InvalidModelError(ClientError):
    """Invalid model specified"""

    pass


class ConfigurationError(ServerError):
    """Missing or invalid configuration"""

    pass
