import json
import yaml
from yaml import Loader, ScalarNode


class YSGTag(yaml.YAMLObject):
    def __init__(self, yaml_tag, tag_type):
        self.yaml_tag = yaml_tag
        self.schema = dict(type=tag_type)

    def __repr__(self):
        return json.dumps(self.schema)

    def from_yaml(self, loader: Loader, node):
        if isinstance(node, ScalarNode) and node.value == '':
            return self.schema
        self.schema.update(loader.construct_mapping(node, deep=True))
        return self.schema

    def to_yaml(self, dumper, data):
        return dumper.represent_scalar(self.yaml_tag, data)


def get_yaml():
    string_tag = YSGTag(yaml_tag=u'!STRING', tag_type='string')
    number_tag = YSGTag(yaml_tag=u'!NUMBER', tag_type='number')
    integer_tag = YSGTag(yaml_tag=u'!INTEGER', tag_type='integer')
    array_tag = YSGTag(yaml_tag=u'!ARRAY', tag_type='array')
    yaml.SafeLoader.add_constructor(string_tag.yaml_tag, string_tag.from_yaml)
    yaml.SafeDumper.add_multi_representer(string_tag, string_tag.to_yaml)
    yaml.SafeLoader.add_constructor(number_tag.yaml_tag, number_tag.from_yaml)
    yaml.SafeDumper.add_multi_representer(number_tag, number_tag.to_yaml)
    yaml.SafeLoader.add_constructor(integer_tag.yaml_tag, integer_tag.from_yaml)
    yaml.SafeDumper.add_multi_representer(integer_tag, integer_tag.to_yaml)
    yaml.SafeLoader.add_constructor(array_tag.yaml_tag, array_tag.from_yaml)
    yaml.SafeDumper.add_multi_representer(array_tag, array_tag.to_yaml)
    return yaml
