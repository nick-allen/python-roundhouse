from collections import OrderedDict

import yaml
from roundhouse import Serializer

yaml.add_representer(OrderedDict, lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items()))


class YAMLSerializer(Serializer):
    """Handles serialization of YAML data"""

    format = 'yaml'
    extensions = ['.yml', '.yaml']

    def serialize(self, data_dict, stream):
        yaml.dump(data_dict, stream, default_flow_style=False)

        return stream

    def deserialize(self, stream):
        return yaml.safe_load(stream)
