import io
import logging

import six

from roundhouse.utils import import_submodules, get_recursive_subclasses, get_full_qualname

logger = logging.getLogger(__name__)


class Serializer(object):
    """Base serializer class"""

    BYTES = six.binary_type
    UNICODE = six.text_type

    input_data_type = UNICODE
    output_data_type = UNICODE
    encoding = 'utf-8'

    format = None
    extensions = []

    def __init__(self, pretty=False):
        self.pretty = pretty

    def __ensure_string_type(self, string, target):
        """Ensure string is of correct type, encoding/decoding as needed according to serializer type and encoding"""
        # String is of expected type
        if isinstance(string, target):
            return string

        # String is bytes, make unicode
        if target is self.UNICODE:
            return string.decode(self.encoding, 'xmlcharrefreplace')

        # String is unicode, make bytes
        return string.encode(self.encoding, 'xmlcharrefreplace')

    def _do_serialize(self, data, stream):
        """Internal top-level call kicking off serialization

        Handles ensuring data is of appropriate type and encoding before executing core public serialize method
        """
        # TODO: Pre-process strings in data to unicode
        if self.input_data_type is self.BYTES:
            target_stream = io.BytesIO()
        else:
            target_stream = stream

        output_stream = self.serialize(data, target_stream)

        if self.input_data_type is self.BYTES:
            output_stream.seek(0)
            stream.write(self.__ensure_string_type(output_stream.read(), self.UNICODE))

        stream.seek(0)

        return stream

    def serialize(self, data, stream):
        """Serialize dict to serializer's format

        Args:
            data (dict): Target data to be serialized into stream
            stream: Stream to write data to and return

        Returns:
            Stream providing serialized data
        """
        raise NotImplementedError

    def _do_deserialize(self, serialized_data):
        """Internal top-level call kicking off deserialization

        Wraps stream in translator to ensure data is in correct type and encoding
        """
        if hasattr(serialized_data, 'read'):
            serialized_data.seek(0)
            serialized_data = serialized_data.read()

        serialized_data = self.__ensure_string_type(serialized_data, self.input_data_type)
        stream_class = io.StringIO if self.input_data_type is self.UNICODE else io.BytesIO

        return self.deserialize(stream_class(serialized_data))
        # TODO: Post-process strings in returned data to unicode

    def deserialize(self, stream):
        """Deserialize data in serializer's format to dict

        Returns:
            dict: Deserialized python representation of the data provided by input stream
        """
        raise NotImplementedError


_serializer_cache = None


def get_serializers(refresh_cache=False):
    """Discover and return Serializer classes from all installed plugins

    Serializers are cached and are not repeatedly loaded in future calls

    Args:
        refresh_cache (bool): If True, ignore any existing serializer cache and discover serializers as normal

    Returns:
        dict: Keys are the formats provided by and pointing to their respective Serializers
    """
    global _serializer_cache

    if _serializer_cache is None or refresh_cache:
        from pluggy import PluginManager

        package_name = __name__.split('.')[0]
        pm = PluginManager(package_name)
        pm.load_setuptools_entrypoints(package_name + '.serializers')

        for mod in pm.get_plugins():
            import_submodules(mod)

        _serializer_cache = {}

        for serializer_class in get_recursive_subclasses(Serializer):
            if not serializer_class.format:
                logger.warning('Serializer "{}" does not provide a format, can only be used manually directly'.format(
                    get_full_qualname(serializer_class)
                ))
                continue

            _serializer_cache[serializer_class.format] = serializer_class

    return _serializer_cache


def get_serializer(format_):
    """Return serializer handling the provided format"""
    return get_serializers()[format_]


def serialize(data, format_, **kwargs):
    """Serialize data to given format

    Args:
        data: Data to be pushed through serializer
        format_ (str): Format of serializer to use

    Returns:
        Serialized data
    """
    serializer_class = get_serializer(format_)
    serializer = serializer_class(**kwargs)

    return serializer._do_serialize(data, io.StringIO()).getvalue()


def deserialize(serialized_data, format_, **kwargs):
    """Deserialize data into internal representation

    Notes:
        serialized_data is encoded and wrapped in a stream automatically as needed

    Args:
        serialized_data (str or stream): A string or stream to be deserialized
        format_ (str): Format of serializer to use

    Returns:
        Deserialized data
    """
    serializer_class = get_serializer(format_)
    serializer = serializer_class(**kwargs)

    return serializer._do_deserialize(serialized_data)
