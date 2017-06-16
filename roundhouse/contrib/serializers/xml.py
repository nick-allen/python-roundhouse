import xmltodict

from roundhouse import Serializer, serialize, deserialize


class XMLSerializer(Serializer):

    format = 'xml'
    extensions = ['.xml']

    # FIXME: Number types being returned as strings

    def serialize(self, data, stream):
        serialized = xmltodict.unparse(data, pretty=self.pretty)

        stream.write(serialized)

        return stream

    def deserialize(self, stream):
        # FIXME: Hack to remove OrderedDicts from parse results
        data = xmltodict.parse(stream.read())

        # JSON serialization builtin to core
        intermediate_format = 'json'

        return deserialize(serialize(data, intermediate_format), intermediate_format)
