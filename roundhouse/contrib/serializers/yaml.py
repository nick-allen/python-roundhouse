from __future__ import absolute_import

from collections import OrderedDict

import yaml
import six

from roundhouse import Serializer

yaml.add_representer(
    OrderedDict,
    lambda self, data: self.represent_mapping(u'tag:yaml.org,2002:map', six.iteritems(data))
)

yaml.SafeLoader.add_constructor(
    u'tag:yaml.org,2002:python/unicode',
    lambda self, data: data.value
)
yaml.SafeLoader.add_constructor(
    u'tag:yaml.org,2002:str',
    lambda self, data: self.construct_scalar(data)
)


class YAMLSerializer(Serializer):
    """Handles serialization of YAML data"""

    format = 'yaml'
    extensions = ['.yml', '.yaml']

    def serialize(self, data, stream):
        dumped_data = yaml.safe_dump(
            data,
            allow_unicode=True,
            default_flow_style=not self.pretty
        )

        if isinstance(dumped_data, self.BYTES):
            dumped_data = dumped_data.decode(self.encoding)

        stream.write(dumped_data)

        return stream

    def deserialize(self, stream):
        return yaml.safe_load(stream)
