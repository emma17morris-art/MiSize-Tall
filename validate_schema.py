import json, sys
from jsonschema import validate

schema_file, data_file = sys.argv[1], sys.argv[2]

with open(schema_file) as f:
    schema = json.load(f)

with open(data_file) as f:
    data = json.load(f)

validate(instance=data, schema=schema)
print("Schema validation OK")
