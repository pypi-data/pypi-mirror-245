# yaml-schema-gen

## Quick Guide

`pip install .`

### Generate only JSON schema
`ysg --generate_from YamlSchemaGen/schema.yaml`

### Generate and Validate
`ysg --generate_from YamlSchemaGen/schema.yaml --validate YamlSchemaGen/input.yaml`

### Give a custom name to the generated schema file
`ysg --generate_from YamlSchemaGen/schema.yaml --output my_schema.yaml`

