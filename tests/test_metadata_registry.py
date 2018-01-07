from class_registry.registry import RegistryKeyError
import pytest
from marshmallow import Schema, fields, pprint

from primal.metadata.registry import (cached_metadata_controllers,
                                      MetadataController, metadata_controllers)


class NewMetadataController(MetadataController):
    pass


def test_register():

    for b in (MetadataController(), NewMetadataController()):

        with pytest.raises(NotImplementedError):
            b.kind

        with pytest.raises(NotImplementedError):
            b.serializer


def test_metadata_controllers():

    class TestSchema(Schema):
        name = fields.Str()

    @metadata_controllers.register
    class TestMetadataController(MetadataController):
        kind = "com.testing"
        serializer = TestSchema()

    metadata_controllers.get("com.testing") is None

    with pytest.raises(RegistryKeyError):
        metadata_controllers["com.not.testing"]

    a = metadata_controllers["com.testing"]
    b = metadata_controllers["com.testing"]
    assert a != b

    c = cached_metadata_controllers['com.testing']
    b = cached_metadata_controllers['com.testing']

    assert c == b
