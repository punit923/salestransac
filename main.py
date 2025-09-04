import json   # built-in, no install needed
from jsonschema import validate, ValidationError

schema = {
  "$id": "https://example.com/address.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "description": "An address similar to http://microformats.org/wiki/h-card",
  "type": "object",
  "properties": {
    "postOfficeBox": {
      "type": "string"
    },
    "extendedAddress": {
      "type": "string"
    },
    "streetAddress": {
      "type": "string"
    },
    "locality": {
      "type": "string"
    },
    "region": {
      "type": "string"
    },
    "postalCode": {
      "type": "string"
    },
    "countryName": {
      "type": "string"
    }
  },
  "required": [ "locality", "region", "countryName" ],
  "dependentRequired": {
    "postOfficeBox": [ "streetAddress" ],
    "extendedAddress": [ "streetAddress" ]
  }
}

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
    print("✅ JSON is valid")
except ValidationError as e:
    print("❌ JSON validation error:", e.message)
