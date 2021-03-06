"""metadata is a place to store metadata about entities."""
import os
from datetime import datetime, timezone

from pynamodb.attributes import (JSONAttribute, UTCDateTimeAttribute,
                                 UnicodeAttribute, UnicodeSetAttribute,
                                 NumberAttribute)
from pynamodb.settings import get_settings_value
from pynamodb.constants import STREAM_NEW_AND_OLD_IMAGE
from pynamodb.models import Model


def utcnow():
    """utcnow_unaware creats a timezone unaware utc dateime."""
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)

    return dt


class Metadata(Model):
    """Metadata mediates data storage to dynamodb."""

    class Meta:
        """MetadataModel Meta class for config."""

        table_name = "Metadata"
        host = os.environ.get("DYNAMODB_HOST", get_settings_value('host'))
        region = os.environ.get("AWS_REGION", get_settings_value('region'))
        stream_view_type = STREAM_NEW_AND_OLD_IMAGE

    id = UnicodeAttribute(hash_key=True)
    version = NumberAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=utcnow)
    updated_at = UTCDateTimeAttribute(default=utcnow)
    kind = UnicodeAttribute(null=True)
    data = JSONAttribute(default={})
    # Used to mark for delete
    delete_after = UTCDateTimeAttribute(null=True)


class Entity(Model):
    """Entity represents a thing: person, place, paper, etc."""

    class Meta:
        """MetadataModel Entity class for config."""

        table_name = "Entity"
        host = os.environ.get("DYNAMODB_HOST", get_settings_value('host'))
        region = os.environ.get("AWS_REGION", get_settings_value('region'))
        stream_view_type = STREAM_NEW_AND_OLD_IMAGE

    id = UnicodeAttribute(hash_key=True)
    version = NumberAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=utcnow)
    updated_at = UTCDateTimeAttribute(default=utcnow)
    metadata = UnicodeSetAttribute(default=set)
    delete_after = UTCDateTimeAttribute(null=True)
