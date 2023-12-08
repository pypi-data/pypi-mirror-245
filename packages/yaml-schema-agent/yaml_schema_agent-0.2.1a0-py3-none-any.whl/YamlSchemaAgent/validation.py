import os

from jsonschema.validators import validate


def safe_validation(yaml_file, schema, yaml_context, logger):
    try:
        yaml_data = yaml_context.safe_load(open(yaml_file).read())
        validate(instance=yaml_data, schema=schema)
    except Exception as error:
        error_msg = '\n' + '!!!' * 10 + f' Failed while validating {yaml_file} ' + '!!!' * 10
        error_msg = error_msg + f'\nError: {type(error).__name__}: {error}'
        logger.error(error_msg)


def run(yaml_context, validate_loc, schema, logger=None):
    if os.path.isfile(validate_loc):
        logger.info(f"Validating yaml file: {validate_loc}")
        safe_validation(validate_loc, schema, yaml_context, logger)
    if os.path.isdir(validate_loc):
        logger.info(f"Validating yaml files in: {validate_loc}")
        files = os.listdir(validate_loc)
        for file in files:
            logger.info('>>>' * 10 + f' Validating: {file} ' + '<<<' * 10)
            safe_validation(f'{validate_loc}/{file}', schema, yaml_context, logger)
