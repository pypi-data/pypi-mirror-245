import argparse

from YamlSchemaAgent import generate, validation
from YamlSchemaAgent.logger import get_logger
from YamlSchemaAgent.tags_pkg import get_yaml


def main():
    parser = argparse.ArgumentParser(
        prog='Yaml Schema Generator',
        description='Generates a YAML schema with Validation capabilities',
        epilog='')
    parser.add_argument('-s', '--schema_file', required=False, default=None)
    parser.add_argument('-v', '--validate', required=False, default=None)
    parser.add_argument('-g', '--generate_from', required=False, default=None)
    parser.add_argument('-o', '--output', required=False, default=None)
    parser.add_argument('-vb', '--verbose', required=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('-rl', '--report_location', required=False, default='reports')
    parser.add_argument('-sr', '--simple_report', required=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    logger = get_logger(
        verbose=args.verbose,
        simple_report=args.simple_report,
        report_location=args.report_location
    )
    schema = None
    yaml_context = get_yaml()
    if args.schema_file:
        logger.info(f"---" * 30)
        logger.info(f"Loading schema from {args.schema_file}")
        schema = yaml_context.safe_load(open(args.schema_file).read())
        logger.info(f"Finished Loading schema")
        logger.info(f"---" * 30)
    if args.generate_from:
        logger.info(f"---" * 30)
        logger.info(f"Generating schema from {args.generate_from}")
        schema = generate.run(
            yaml_context=yaml_context,
            schema_loc=args.generate_from,
            output=args.output,
            logger=logger
        )
        logger.info(f"Finished generating schema")
        logger.info(f"---" * 30)
    if args.validate:
        logger.info(f"---" * 30)
        logger.info(f"Begin Validation")
        validation.run(
            yaml_context=yaml_context,
            validate_loc=args.validate,
            schema=schema,
            logger=logger
        )
        logger.info(f"End Validation")
        logger.info(f"---" * 30)


if __name__ == '__main__':
    main()
