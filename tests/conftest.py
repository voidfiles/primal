"""Fixtures for tests."""
from primal.metadata.interface import unique_id
from primal.metadata.models import Entity

import pytest


@pytest.fixture(scope="session")
def dynamodb_tables():
    """Will create the dynamodb tables for each test."""
    from primal.operations.create_tables import operation

    operation()


@pytest.fixture()
def entity():
    """Will create an entity for testing."""
    return Entity(id=unique_id())
