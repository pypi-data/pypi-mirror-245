import json
from logging import Logger

from YamlSchemaAgent import schema_types

logger_obj: Logger = None

def decode_base_types(k, v):
    logger_obj.debug(f'{k} : {v} - decoded type: {type(v).__name__.lower()}')
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
            jsonschema[k] = decode_base_types(k, v)


def run(yaml_context, schema_loc, output=None, logger=None):
    global logger_obj
    logger_obj = logger
    schema = yaml_context.safe_load(open(schema_loc).read())
    json_schema = {
        "type": "object",
        "properties": {
        },
    }
    walk_and_decode(schema, json_schema['properties'])
    msg = "\n" + "***" * 10 + " GENERATED JSON SCHEMA " + "***" * 10
    logger.debug(msg + '\n' + json.dumps(json_schema, indent=2))
    output = output or 'ysg_' + schema_loc.split('/')[-1]
    logger.info(f'Writing generated schema to: {output}')
    with open(output, 'w') as gen_schema:
        gen_schema.write(json.dumps(json_schema, indent=4))
    return json_schema
