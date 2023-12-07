import argparse

from YamlSchemaAgent import generate
from YamlSchemaAgent.tags_pkg import get_yaml
from jsonschema.validators import validate


def main():
    parser = argparse.ArgumentParser(
        prog='Yaml Schema Generator',
        description='Generates a YAML schema with Validation capabilities',
        epilog='')
    parser.add_argument('-s', '--schema_file', required=False, default=None)
    parser.add_argument('-v', '--validate', required=False, default=None)
    parser.add_argument('-g', '--generate_from', required=False, default=None)
    parser.add_argument('-o', '--output', required=False, default=None)
    args = parser.parse_args()
    schema = None
    yaml_context = get_yaml()
    if args.schema_file:
        schema = yaml_context.safe_load(args.schema_file)
    if args.generate_from:
        schema = generate.run(yaml_context=yaml_context, schema_loc=args.generate_from, output=args.output)
    if args.validate:
        input = yaml_context.safe_load(open(args.validate).read())
        assert validate(instance=input, schema=schema) is None
        print("All Done")


if __name__ == '__main__':
    main()
