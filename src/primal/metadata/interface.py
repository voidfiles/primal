"""primal.metadata.interface is the public api for metadta."""
from datetime import datetime, timedelta
from uuid import uuid4
import time

from pynamodb.expressions.condition import size, NotExists

from primal.contrib.pynamodb.conditional import raise_for_conditional_failure

from primal.metadata.models import Entity, Metadata
from primal.metadata.registry import cached_metadata_controllers
from primal.metadata.schema import MetadataSchema
from primal.metadata.exceptions import ConditionalUpdateException


def unique_id():
    """unique_id will generate a uuid encoded as a string."""
    return str(uuid4())


def timestamp():
    return int(time.time())


def create_entity():
    """Will create a fresh entity."""
    e = Entity(
        id=unique_id(),
        version=timestamp(),
    )
    e.save()
    return e


def _choose_operation(metadata_to_add, metadata_to_delete):

    if metadata_to_delete:
        operation = Entity.metadata.delete
        metadata = metadata_to_delete
    else:
        operation = Entity.metadata.add
        metadata = metadata_to_add

    return operation, metadata


def _check_update_entity_args(metadata_to_add, metadata_to_delete):
    if not (metadata_to_add or metadata_to_delete):
        raise ValueError("Must pass metadata_to_add or metadata_to_remove")

    if metadata_to_add and metadata_to_delete:
        raise ValueError(("Pass only one of metadata_to_add"
                          " or metadata_to_remove"))


def update_entity(entity_id, metadata_to_add=None, metadata_to_delete=None):
    """Will update an entity."""

    _check_update_entity_args(metadata_to_add, metadata_to_delete)

    e = Entity.get(entity_id)

    operation, metadata = _choose_operation(
        metadata_to_add, metadata_to_delete)
    with raise_for_conditional_failure(ConditionalUpdateException):
        e.update(actions=[
            Entity.version.set(timestamp()),
            operation(metadata),
        ], condition=(
            (Entity.version == e.version) &
            (Entity.metadata.does_not_exist() |
             (size(Entity.metadata) <= 100))
        ))

    return e


def delete_entity(entity_id):
    """Will delete an entity."""

    e = Entity.get(entity_id)
    dt = datetime.utcnow()
    dt += timedelta(days=10)
    with raise_for_conditional_failure(ConditionalUpdateException):
        e.update(actions=[
            Entity.version.set(timestamp()),
            Entity.delete_after.set(dt),
        ], condition=(
            Entity.version == e.version
        ))

    return e


def create_metadata(kind, data):
    """Will create a new metadata object."""
    m = Metadata(
        id=unique_id(),
        kind=kind,
        data=data,
        version=timestamp(),
    )
    m.save()
    return m


def delete_metadata(id):
    m = Metadata.get(id)
    dt = datetime.utcnow()
    dt += timedelta(days=10)

    with raise_for_conditional_failure(ConditionalUpdateException):
        m.update(actions=[
            Metadata.delete_after.set(dt),
            Metadata.version.set(timestamp()),
        ], condition=(
            Metadata.version == m.version
        ))

    return m


metadata_schema = MetadataSchema(strict=True)


def validate_and_create(data):

    result = metadata_schema.load(data)

    kind = result.data['kind']
    controller = cached_metadata_controllers[kind]

    result = controller.serializer.load(result.data['data'])

    return create_metadata(kind, result.data)
