from marshmallow import Schema, fields, validate

from primal.metadata.registry import MetadataController, metadata_controllers


class QuoteSchema(Schema):
    """Will validate a quote object"""
    author = fields.String(
        required=True,
        validate=[validate.Length(min=0, max=100)])
    source = fields.String(
        validate=[validate.Length(min=0, max=300)]
    )
    text = fields.String(
        validate=[validate.Length(min=0, max=1000)]
    )
    found = fields.String(
        validate=[validate.Length(min=0, max=1000)]
    )
    archive = fields.String(
        validate=[validate.Length(min=0, max=1000)]
    )


@metadata_controllers.register
class QuoteController(MetadataController):
    kind = "com.rumproarious.slide.quote"
    serializer = QuoteSchema(strict=True)
