import unittest
from jsonschema import validate, ValidationError

# Define schema (could also be loaded from a .json file)
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


class TestAddressSchema(unittest.TestCase):

    def test_valid_json(self):
        """Test that a valid JSON passes schema validation"""
        incoming_json = {
            "postOfficeBox": "123",
            "streetAddress": "456 Main St",
            "locality": "Cityville",
            "region": "State",
            "postalCode": "12345",
            "countryName": "Country"
        }
        try:
            validate(instance=incoming_json, schema=schema)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for valid JSON")

    def test_missing_required_field(self):
        """Test that missing required field raises ValidationError"""
        incoming_json = {
            "region": "State",
            "countryName": "Country"
        }
        with self.assertRaises(ValidationError):
            validate(instance=incoming_json, schema=schema)

    def test_invalid_type(self):
        """Test that invalid type raises ValidationError"""
        incoming_json = {
            "streetAddress": "456 Main St",
            "locality": "Cityville",
            "region": "State",
            "postalCode": "12345",
            "countryName": 123  # ❌ should be string
        }
        with self.assertRaises(ValidationError):
            validate(instance=incoming_json, schema=schema)

    def test_dependent_required(self):
        """Test that dependentRequired condition is enforced"""
        incoming_json = {
            "postOfficeBox": "123",
            "locality": "Cityville",
            "region": "State",
            "countryName": "Country"
        }
        with self.assertRaises(ValidationError):
            validate(instance=incoming_json, schema=schema)


if __name__ == "__main__":
    unittest.main()
