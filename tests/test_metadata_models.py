"""Metadata model tests requires dynamodb local."""
from datetime import datetime

from primal.metadata.models import Entity, Metadata

import pytest


@pytest.mark.ddblocal
def test_metadata_model(dynamodb_tables):
    """Tests metadata model."""
    m = Metadata(id="123", kind="com.awesome")
    m.save()
    assert isinstance(m.created_at, datetime)
    assert isinstance(m.updated_at, datetime)
    assert isinstance(m.data, dict)
    assert m.kind == "com.awesome"
    assert m.id == "123"
    assert m.data == {}
    m2 = Metadata.get('123', consistent_read=True)
    assert m2.id == m.id
    assert m2.created_at == m.created_at
    assert m2.updated_at == m.updated_at
    assert m2.data == m.data
    assert m2.kind == m.kind


@pytest.mark.ddblocal
def test_entity_model(dynamodb_tables):
    """Tests entity model."""
    e = Entity(id="123", metadata=set("123:com.awesome"))
    e.save()
    assert isinstance(e.created_at, datetime)
    assert isinstance(e.updated_at, datetime)
    assert isinstance(e.metadata, set)
    assert e.metadata == set("123:com.awesome")
    assert e.id == "123"
    e2 = Entity.get('123', consistent_read=True)
    assert e2.id == e.id
    assert e2.created_at == e.created_at
    assert e2.updated_at == e.updated_at
    assert e2.metadata == e.metadata
