from functools import wraps
from flask import current_app, g, request


def with_provider_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the provider from the blueprint name
        provider_name = request.blueprint
        # Store provider_api in Flask's g context
        g.provider_api = getattr(current_app, provider_name)
        return f(*args, **kwargs)

    return decorated_function
