import pytest
from marshmallow import ValidationError
from primal.metadata.schema import MetadataSchema, entity_schema

from unittest.mock import patch

metadata_schema = MetadataSchema(strict=True)


@patch("primal.metadata.registry.metadata_controllers.keys",
       return_value=["com.awesome"])
def test_metadata_schema(d):
    from primal.metadata.registry import metadata_controllers
    data = metadata_schema.load({
        "kind": "com.awesome",
        "data": {
            "a": "b"
        }
    })


def test_entity_schema():
    a = entity_schema.load({"metadata": ["a"]}).data
    assert a['metadata'] == ["a"]

    too_much = ["a" for x in range(0, 21)]

    with pytest.raises(ValidationError):
        a = entity_schema.load({"metadata": too_much}).data
