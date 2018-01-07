from marshmallow import Schema, fields, validate, ValidationError, validates

from primal.metadata.registry import metadata_controllers


def check_kind(value):
    if value not in metadata_controllers.keys():
        raise ValidationError("not a valid choice")


class MetadataSchema(Schema):
    """Will validate a metadata object"""
    id = fields.String()
    kind = fields.String(
        required=True,
        validate=[check_kind, validate.Length(min=0, max=500)])
    data = fields.Dict(
        required=True,
    )


class EntitySchema(Schema):
    id = fields.String()
    metadata = fields.List(fields.String())

    @validates('metadata')
    def validate_metadata(self, value):
        if len(value) > 20:
            raise ValidationError('Quantity must be less than 20.')


entity_schema = EntitySchema(strict=True)
