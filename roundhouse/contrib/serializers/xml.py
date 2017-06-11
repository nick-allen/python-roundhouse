import xmltodict

from roundhouse import Serializer


class XMLSerializer(Serializer):

    format = 'xml'
    extensions = ['.xml']

    def serialize(self, data_dict, stream):
        serialized = xmltodict.unparse(data_dict, pretty=True)

        stream.write(serialized)

        return stream

    def deserialize(self, stream):
        # Expects bytes internally, but accepts full string
        return xmltodict.parse(stream.read())
