from flask import Blueprint, request, current_app, g, jsonify
import sys
from ..middleware import log_request, check_required_fields
from ..decorators import with_provider_api
from ...exceptions import ClientError, ServerError, LLMRefusalError
from ...types import CallAPIResult


def create_provider_blueprint(provider_name):
    """
    Factory function to create a blueprint for an API provider
    """
    bp = Blueprint(provider_name, __name__, url_prefix=f"/{provider_name}")
    bp.before_request(log_request)

    def jsonify_success(result: CallAPIResult) -> str:
        return jsonify({"data": result.model_dump()})

    # TODO: Handle all routes the same way, DRY this up some more, e.g.:

    # - return jsonify_success for result
    # - try/catch for ClientError, ServerError and handle those the same

    @bp.route("/email", methods=["POST"])
    @with_provider_api
    def email_endpoint():
        try:
            error_response = check_required_fields(["email"])
            if error_response:
                return error_response
            email_body = request.json["email"]
            model = request.json.get("model")
            result = g.provider_api.generate_email_response(email_body, model)
            return jsonify_success(result)
        except ClientError as e:
            return jsonify({"errors": [str(e)]}), 400
        except ServerError as e:
            return jsonify({"errors": [str(e)]}), 500

    @bp.route("/rewrite", methods=["POST"])
    @with_provider_api
    def message_rewrite_endpoint():
        try:
            error_response = check_required_fields(["message"])
            if error_response:
                return error_response

            message = request.json["message"]
            model = request.json.get("model")

            result = g.provider_api.rewrite_message(message, model)
            return jsonify_success(result)

        except LLMRefusalError as e:
            return jsonify({"errors": [str(e)], "type": "refusal"}), 400
        except ClientError as e:
            return jsonify({"errors": [str(e)]}), 400
        except ServerError as e:
            return jsonify({"errors": [str(e)]}), 500

    # note: valid_models call does not return a CallAPIResult object
    @bp.route("/models", methods=["GET"])
    @with_provider_api
    def models_endpoint():
        error_response = check_required_fields([])
        if error_response:
            return error_response
        result = g.provider_api.valid_models()
        return jsonify({"data": result})

    @bp.route("/prompt_response", methods=["POST"])
    @with_provider_api
    def prompt_response_endpoint():
        try:
            error_response = check_required_fields(["message"])
            if error_response:
                return error_response
            prompt = request.json["message"]
            model = request.json.get("model")
            result = g.provider_api.basic_prompt_response(prompt, model)
            return jsonify_success(result)
        except ClientError as e:
            return jsonify({"errors": [str(e)]}), 400
        except ServerError as e:
            return jsonify({"errors": [str(e)]}), 500

    @bp.route("/summarize", methods=["POST"])
    @with_provider_api
    def text_summary_endpoint():
        try:
            error_response = check_required_fields(["text"])
            if error_response:
                return error_response

            message = request.json["text"]
            model = request.json.get("model")

            result = g.provider_api.summarize_text(message, model)
            return jsonify_success(result)

        except LLMRefusalError as e:
            return jsonify({"errors": [str(e)], "type": "refusal"}), 400
        except ClientError as e:
            return jsonify({"errors": [str(e)]}), 400
        except ServerError as e:
            return jsonify({"errors": [str(e)]}), 500

    return bp
