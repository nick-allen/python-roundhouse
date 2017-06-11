import io
import logging

from roundhouse.utils import import_submodules, get_recursive_subclasses, get_full_qualname

logger = logging.getLogger(__name__)


class Serializer(object):
    """Base serializer class"""

    format = None
    extensions = []

    def __init__(self, pretty=False):
        self.pretty = pretty

    def serialize(self, data, stream):
        """Serialize dict to serializer's format

        Args:
            data (dict): Target data to be serialized into stream
            stream: Stream to write data to and return

        Returns:
            Stream providing serialized data
        """
        raise NotImplementedError

    def deserialize(self, stream):
        """Deserialize data in serializer's format to dict

        Returns:
            dict: Deserialized python representation of the data provided by input stream
        """
        raise NotImplementedError


_serializer_cache = None


def get_serializers():
    """Discover and return Serializer classes from all installed plugins

    Serializers are cached and are not repeatedly loaded in future calls

    Returns:
        dict: Keys are the formats provided by and pointing to their respective Serializers
    """
    global _serializer_cache
    if _serializer_cache is None:
        from pluggy import PluginManager

        package_name = __name__.split('.')[0]
        pm = PluginManager(package_name)
        pm.load_setuptools_entrypoints(package_name)

        for mod in pm.get_plugins():
            import_submodules(mod)

        _serializer_cache = {}

        for serializer_class in get_recursive_subclasses(Serializer):
            if not serializer_class.format:
                logger.warning('Serializer "{}" does not provide a format, will not be auto-discovered'.format(
                    get_full_qualname(serializer_class)
                ))
                continue

            _serializer_cache[serializer_class.format] = serializer_class

    return _serializer_cache


def get_serializer(format_):
    """Return serializer handling the provided format"""
    return get_serializers()[format_]


def serialize(data, format_, pretty=False):
    serializer_class = get_serializer(format_)
    serializer = serializer_class(pretty)

    stream = io.StringIO()

    serializer.serialize(data, stream)

    return stream.read()


def deserialize(stream, format_):
    serializer_class = get_serializer(format_)
    serializer = serializer_class()

    return serializer.deserialize(stream)
