import json

from roundhouse import Serializer


class JSONSerializer(Serializer):
    """Handles serialization of JSON data"""

    format = 'json'
    extensions = ['.json']

    def serialize(self, data_dict, stream):
        json.dump(data_dict, stream, indent=4)

        return stream

    def deserialize(self, stream):
        return json.load(stream)
