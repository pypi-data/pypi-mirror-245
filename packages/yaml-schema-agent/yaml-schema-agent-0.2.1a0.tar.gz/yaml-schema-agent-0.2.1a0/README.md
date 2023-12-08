# yaml-schema-gen

## Quick Guide

`pip install yaml-schema-agent`

### Generate only JSON schema
`ysg --generate_from YamlSchemaGen/schema.yaml`

### Generate and Validate
`ysg --generate_from YamlSchemaGen/schema.yaml --validate YamlSchemaGen/input.yaml`

### Give a custom name to the generated schema file
`ysg --generate_from YamlSchemaGen/schema.yaml --output my_schema.yaml`

### Logs
Use `--report_location` to init the log directory  
`ysg --generate_from YamlSchemaGen/schema.yaml --output my_schema.yaml --report_location reports/` 

### verbose and simple_report

`verbose` - prints detailed log on console (default: False)  
`simple_report` - The report generated in the report_location will be concise (default: False).    

`ysg --generate_from YamlSchemaGen/schema.yaml --output my_schema.yaml --report_location reports/ --verbose --simple_report`  
