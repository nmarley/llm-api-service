from flask import request, jsonify
import logging
from functools import wraps

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Filter health check route
class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return not ('"GET /healthz' in record.getMessage())


# Apply the filter to the werkzeug logger
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addFilter(HealthCheckFilter())


def log_request():
    logger.info(f"Received request at {request.path}")


# Helper function to check required fields
def check_required_fields(required_fields):
    missing_fields = [field for field in required_fields if field not in request.json]
    if missing_fields:
        return jsonify(
            {
                "error": "Bad Request",
                "message": f"Missing required field(s): {', '.join(missing_fields)}",
            }
        ), 400
    return None
