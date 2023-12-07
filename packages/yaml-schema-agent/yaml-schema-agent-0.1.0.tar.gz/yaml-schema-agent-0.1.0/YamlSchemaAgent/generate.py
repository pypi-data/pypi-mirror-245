import json

from YamlSchemaAgent import schema_types


def decode_base_types(v):
    print(f'add_{type(v).__name__.lower()}')
    if hasattr(schema_types, f'add_{type(v).__name__.lower()}'):
        return getattr(schema_types, f'add_{type(v).__name__.lower()}')()


def walk_and_decode(data, jsonschema):
    for k, v in data.items():
        if isinstance(v, dict):
            if 'type' not in v:
                jsonschema[k] = {
                    "type": "object",
                    "properties": {}
                }
                walk_and_decode(v, jsonschema[k]['properties'])
            else:
                jsonschema[k] = v
        else:
            jsonschema[k] = decode_base_types(v)


def run(yaml_context, schema_loc, output=None):
    schema = yaml_context.safe_load(open(schema_loc).read())
    json_schema = {
        "type": "object",
        "properties": {
        },
    }
    walk_and_decode(schema, json_schema['properties'])
    print("***"*20 + "GENERATED JSON SCHEMA" + "***"*20 )
    print(json.dumps(json_schema, indent=2))
    with open(output or 'ysg_'+ schema_loc.split('/')[-1], 'w') as gen_schema:
        gen_schema.write(json.dumps(json_schema, indent=4))
    return json_schema
