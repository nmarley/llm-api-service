from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from .routes import anthropic, openai, xai, common
from ..anthropic_api import AnthropicAPI
from ..openai_api import OpenAIAPI
from ..xai_api import xAIAPI


def create_app():
    app = Flask(__name__)

    from decimal import Decimal
    from flask.json.provider import DefaultJSONProvider

    class CustomJSONProvider(DefaultJSONProvider):
        def default(self, o):
            if isinstance(o, Decimal):
                return format(o, "f")
            return super().default(o)

    app.json = CustomJSONProvider(app)
    app.json.compact = True

    # Enable CORS
    # Option 1: Allow all origins
    CORS(app)

    # Option 2: Allow specific origins (uncomment to use instead)
    # CORS(app, resources={
    #     r"/*": {
    #         "origins": [
    #             "http://localhost:3000",  # React dev server
    #             "http://127.0.0.1:3000",
    #             "http://localhost:5173",  # Vite dev server
    #             "http://127.0.0.1:5173",
    #         ]
    #     }
    # })

    # Initialize APIs
    app.anthropic = AnthropicAPI()
    app.openai = OpenAIAPI()
    app.xai = xAIAPI()

    # Register error handlers
    common.register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(anthropic.bp)
    app.register_blueprint(openai.bp)
    app.register_blueprint(xai.bp)
    app.register_blueprint(common.bp)

    return app


__all__ = ["create_app"]
