from roundhouse.utils import import_submodules, get_recursive_subclasses


class Serializer(object):
    """Base serializer class"""

    format = None
    extensions = []

    def serialize(self, data_dict, stream):
        """Serialize dict to serializer's format

        Args:
            stream: Stream to write data to and return. Creates new stream if not provided

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


def discover_serializers():
    """Discover and return Serializer classes from all installed plugins"""
    from pluggy import PluginManager

    package_name = __name__.split('.')[0]
    pm = PluginManager(package_name)
    pm.load_setuptools_entrypoints(package_name)

    for mod in pm.get_plugins():
        import_submodules(mod)

    return {s.format: s for s in get_recursive_subclasses(Serializer)}
