import json  # built-in
from jsonschema import validate, ValidationError

# Define schema globally (or load from a .json file)
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


def validate_address(data: dict) -> bool:
    """
    Validate an address JSON against the schema.
    Returns True if valid, raises ValidationError if not.
    """
    try:
        validate(instance=data, schema=schema)
        print("✅ JSON is valid")
        return True
    except ValidationError as e:
        print("❌ JSON validation error:", e.message)
        return False


# # Example usage
# if __name__ == "__main__":
#     incoming_json = {
#         "postOfficeBox": "123",
#         "streetAddress": "456 Main St",
#         "locality": "Cityville",
#         "region": "State",
#         "postalCode": "12345",
#         "countryName": "Country"
#     }

#     validate_address(incoming_json)
