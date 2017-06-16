from __future__ import absolute_import

import toml

from roundhouse import Serializer


class TOMLSerializer(Serializer):

    format = 'toml'
    extensions = ['.toml']

    def serialize(self, data, stream):
        toml.dump(data, stream)

        return stream

    def deserialize(self, stream):
        return toml.load(stream)
