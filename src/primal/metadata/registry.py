from class_registry import ClassRegistry, ClassRegistryInstanceCache

metadata_controllers = ClassRegistry('kind')

cached_metadata_controllers = ClassRegistryInstanceCache(metadata_controllers)


class MetadataController(object):
    """Metadata Controller class represents a kind of metadata."""

    @property
    def kind(self):
        """Kind is a reverse domain id for a metadata."""
        raise NotImplementedError()

    @property
    def serializer(self):
        """Serializer is an instantiated serializer."""
        raise NotImplementedError()
