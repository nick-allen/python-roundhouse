from __future__ import absolute_import

import json

from roundhouse import Serializer


class JSONSerializer(Serializer):
    """Handles serialization of JSON data"""

    format = 'json'
    extensions = ['.json']

    def serialize(self, data, stream):
        # json.dump with ensure_ascii=False yields both bytes and unicode instances as it dumps
        # Must return full unicode output, then write to stream to avoid TypeError during dump
        stream.write(json.dumps(
            data,
            ensure_ascii=False,
            indent=4 if self.pretty else None
        ))

        return stream

    def deserialize(self, stream):
        return json.load(stream)
