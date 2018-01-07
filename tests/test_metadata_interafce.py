"""Tests the metadata interface."""
from datetime import datetime, timezone
from unittest.mock import patch
from marshmallow import Schema, fields, ValidationError

from primal.metadata.exceptions import ConditionalUpdateException
from primal.metadata.models import Entity
from primal.metadata.interface import (create_entity, create_metadata,
                                       delete_metadata, unique_id,
                                       validate_and_create,
                                       _choose_operation,
                                       _check_update_entity_args,
                                       update_entity,
                                       delete_entity)


from primal.metadata.registry import (MetadataController, metadata_controllers)

import pytest


def test_unique_id():
    """Tests unique_id function."""
    blah = unique_id()
    assert isinstance(blah, str)
    assert len(blah) == 36


@patch("primal.metadata.models.Entity.save", return_value=True)
def test_create_entity(save_mock):
    """Will test create_entity."""
    e = create_entity()
    assert e
    assert e.version

    save_mock.assert_called_once()


@patch("primal.metadata.models.Metadata.save", return_value=True)
def test_create_metadata(save_mock):
    """Will test create_metadata."""
    kind = "com.aweseom"
    data = {
        "test": "data",
    }
    m = create_metadata(kind, data)
    assert m.kind == kind
    assert m.data == data
    assert m.version

    save_mock.assert_called_once()


def test_choose_operation():
    op, metadata = _choose_operation(['a'], None)
    assert op == Entity.metadata.add
    assert metadata == ['a']

    op, metadata = _choose_operation(None, ['b'])
    assert op == Entity.metadata.delete
    assert metadata == ['b']

    op, metadata = _choose_operation(['a'], ['b'])
    assert op == Entity.metadata.delete
    assert metadata == ['b']


def test_check_update_entity_args():
    with pytest.raises(ValueError):
        _check_update_entity_args(None, None)

    with pytest.raises(ValueError):
        _check_update_entity_args(['a'], ['b'])

    assert _check_update_entity_args(['a'], None) is None


@pytest.mark.ddblocal
def test_update_entity():
    e = create_entity()

    e = update_entity(e.id, ['a'])

    assert e.metadata == {'a'}

    e = update_entity(e.id, metadata_to_add=['b'])

    assert e.metadata == {'a', 'b'}

    e = update_entity(e.id, metadata_to_delete=['a'])

    assert e.metadata == {'b'}

    e = update_entity(e.id, metadata_to_add=[
        'x%s' % (x) for x in range(0, 100)])
    with pytest.raises(ConditionalUpdateException):
        e = update_entity(e.id, metadata_to_add=['b'])


@pytest.mark.ddblocal
def test_delete_metadata(dynamodb_tables):
    kind = "com.aweseom"
    data = {
        "test": "data",
    }
    now_dt = datetime.now().replace(tzinfo=timezone.utc)
    m = create_metadata(kind, data)
    m2 = delete_metadata(m.id)
    assert m2.delete_after > now_dt


@pytest.mark.ddblocal
def test_validate_and_create(dynamodb_tables):
    class TestSchema(Schema):
        name = fields.Str()

    @metadata_controllers.register
    class TestMetadataController(MetadataController):
        kind = "com.testing"
        serializer = TestSchema()

    m = validate_and_create({
        "kind": "com.testing",
        "data": {
            "name": "testing"
        }
    })

    assert m.data["name"] == "testing"

    with pytest.raises(ValidationError):
        validate_and_create({
            "kind": "com.not",
            "data": {
                "name": "testing"
            }
        })


@pytest.mark.ddblocal
def test_delete_entity(dynamodb_tables):
    e = create_entity()
    e2 = delete_entity(e.id)
    now_dt = datetime.now().replace(tzinfo=timezone.utc)
    assert e2.delete_after > now_dt
