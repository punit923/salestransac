import functions_framework
import json  # built-in
from flask import jsonify, Request
from jsonschema import validate, ValidationError

# Define schema globally (better performance than redefining in each call)
schema = {
    "$id": "https://example.com/address.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "An address similar to http://microformats.org/wiki/h-card",
    "type": "object",
    "properties": {
        "postOfficeBox": {"type": "string"},
        "extendedAddress": {"type": "string"},
        "streetAddress": {"type": "string"},
        "locality": {"type": "string"},
        "region": {"type": "string"},
        "postalCode": {"type": "string"},
        "countryName": {"type": "string"}
    },
    "required": ["locality", "region", "countryName"],
    "dependentRequired": {
        "postOfficeBox": ["streetAddress"],
        "extendedAddress": ["streetAddress"]
    }
}


@functions_framework.http
def validate_address(request: Request):
    """
    Cloud Function entry point.
    Expects JSON in the request body and validates it against the schema.
    """
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"status": "error", "message": "Invalid or missing JSON"}), 400

        # Validate against schema
        validate(instance=data, schema=schema)
        return jsonify({"status": "success", "message": "JSON is valid"}), 200

    except ValidationError as e:
        return jsonify({"status": "error", "message": e.message}), 400
