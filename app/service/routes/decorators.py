from functools import wraps
from flask import current_app, g


def with_provider_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the provider from the blueprint name
        provider_name = f.__globals__["bp"].name
        # Store provider_api in Flask's g context
        g.provider_api = getattr(current_app, provider_name)
        return f(*args, **kwargs)

    return decorated_function
