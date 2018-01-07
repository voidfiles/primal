from unittest.mock import patch

import pytest

from marshmallow import ValidationError
from primal.contrib.flask.api import (api_create_metadata, get_json,
                                      handle_invalid_usage,
                                      handle_invalid_data,
                                      api_delete_metadata,
                                      api_create_entity,
                                      api_add_entity_metadata,
                                      api_delete_entity_metadata,
                                      api_delete_entity)
from primal.contrib.flask.exceptions import APIException
from primal.metadata.models import Metadata, Entity


def mock_metadata():
    return Metadata(id="123", kind="com.testing", data={"data": "data"})


def mock_entity(metadata=None):
    metadata = set(metadata) if metadata else set()
    return Entity(id="123", metadata=metadata)


class MockRequest(object):

    def __init__(self, is_json=True, data=dict):
        self.is_json = is_json
        self.data = data

    def get_json(self):
        return self.data()


def test_get_json():
    r = MockRequest(is_json=False)

    with pytest.raises(APIException) as e:
        get_json(r)
        assert e.status_code == 415

    def raises():
        raise ValueError()

    r = MockRequest(is_json=True, data=raises)

    with pytest.raises(APIException) as e:
        get_json(r)
        assert e.status_code == 422

    r = MockRequest(is_json=True, data=lambda: {"data": "data"})

    assert {"data": "data"} == get_json(r)


def test_handle_invalid_usage(app):
    e = APIException("Unsupported Media Type", status_code=415,
                     slug="unsupported")

    resp = handle_invalid_usage(e)

    assert resp.status_code == 415


def test_handle_invalid_data(app):
    e = ValidationError("test")

    resp = handle_invalid_data(e)

    assert resp.status_code == 400


def build_mock_request():
    return MockRequest(data=lambda: {"data": "data"})


@patch("primal.contrib.flask.api.validate_and_create")
@patch("primal.contrib.flask.api.request", new_callable=build_mock_request)
def test_api_create_metadata_normal(request_mock, validate_and_create_mock):
    validate_and_create_mock.return_value = mock_metadata()
    data = api_create_metadata()

    assert data['kind'] == 'com.testing'
    assert data['data']['data'] == 'data'
    assert data['id'] == '123'


def raise_exception(data):
    raise ValidationError("test")


@patch("primal.contrib.flask.api.delete_metadata")
def test_api_create_metadata_error(delete_mock):
    delete_mock.return_value = mock_metadata()
    resp = api_delete_metadata("123")
    delete_mock.assert_called_with("123")

    assert resp['kind'] == 'com.testing'
    assert resp['data']['data'] == 'data'
    assert resp['id'] == '123'


@patch("primal.contrib.flask.api.create_entity")
def test_api_create_entity(entity_mock):
    entity_mock.return_value = mock_entity()
    resp = api_create_entity()
    entity_mock.assert_called_with()

    assert resp['id'] == '123'
    assert resp['metadata'] == []


def build_mock_entity_request(metadata):
    data = {'metadata': metadata}

    def _inner():
        return MockRequest(data=lambda: data)

    return _inner


@patch("primal.contrib.flask.api.update_entity")
@patch("primal.contrib.flask.api.request",
       new_callable=build_mock_entity_request(['a']))
def test_api_add_entity_metadata(request_mock, entity_mock):
    entity_mock.return_value = mock_entity()
    resp = api_add_entity_metadata("123")
    entity_mock.assert_called_with("123", metadata_to_add=['a'])
    assert resp['id'] == '123'


@patch("primal.contrib.flask.api.update_entity")
@patch("primal.contrib.flask.api.request",
       new_callable=build_mock_entity_request(['a']))
def test_api_delete_entity_metadata(request_mock, entity_mock):
    entity_mock.return_value = mock_entity()
    resp = api_delete_entity_metadata("123")
    entity_mock.assert_called_with("123", metadata_to_delete=['a'])
    assert resp['id'] == '123'


@patch("primal.contrib.flask.api.delete_entity")
@patch("primal.contrib.flask.api.request",
       new_callable=build_mock_request)
def test_api_delete_entity(request_mock, entity_mock):
    entity_mock.return_value = mock_entity()
    resp = api_delete_entity("123")
    assert resp['id'] == '123'
