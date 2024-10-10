from flask import Blueprint, jsonify

bp = Blueprint("common", __name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"errors": ["Not found"]}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"errors": ["Internal server error"]}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"errors": [str(error)]}), 400


@bp.route("/healthz", methods=["GET"])
def health_check():
    try:
        return jsonify({"data": "OK"}), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500
