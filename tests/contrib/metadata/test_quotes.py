from marshmallow import ValidationError

from primal.contrib.metadata.quote import (QuoteController, QuoteSchema)

import pytest


def build_quote(**kwargs):

    default = {
        "author": "testing",
        "source": "testing",
        "text": "testing",
        "found": "testing",
        "archive": "testing",
    }

    default.update(kwargs)

    return {key: val for key, val in default.items() if val}


def test_quote_schema_dump():
    schema = QuoteSchema()

    assert build_quote() == schema.dump(build_quote()).data


def test_quote_schema_load():
    schema = QuoteSchema(strict=True)

    result = schema.load({"author": "testing"})
    assert result.data == {"author": "testing"}

    with pytest.raises(ValidationError):
        schema.load({"source": "testing"})

    with pytest.raises(ValidationError):
        schema.load({"found": "a" * 1001})

    with pytest.raises(ValidationError):
        schema.load({"found": ""})


def test_quote_schema_ctrl():
    assert QuoteController.kind
    assert QuoteController.serializer
