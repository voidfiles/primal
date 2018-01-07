from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from primal.contrib.flask.exceptions import APIException, format_error_message
from primal.metadata.interface import (metadata_schema, validate_and_create,
                                       delete_metadata, create_entity,
                                       update_entity, delete_entity)
from primal.metadata.schema import entity_schema

metadata_api = Blueprint('metadata_api', __name__)


def get_json(request):
    if not request.is_json:
        raise APIException("Unsupported Media Type", status_code=415,
                           slug="unsupported")

    try:
        data = request.get_json()
    except ValueError:
        raise APIException("Invalid JSON", status_code=422,
                           slug="invalid-json")

    return data


@metadata_api.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@metadata_api.errorhandler(ValidationError)
def handle_invalid_data(error):
    response = jsonify(format_error_message(
        "Validation errors",
        error.messages,
        "invalud",
    ))

    response.status_code = 400

    return response


@metadata_api.route('/metadata/', methods=['POST'])
def api_create_metadata():
    data = get_json(request)

    metadata = validate_and_create(data)

    return metadata_schema.dump(metadata).data


@metadata_api.route('/metadata/<metadata_id>/', methods=['DELETE'])
def api_delete_metadata(metadata_id):
    metadata = delete_metadata(metadata_id)

    return metadata_schema.dump(metadata).data


@metadata_api.route('/entity/', methods=['POST'])
def api_create_entity():
    entity = create_entity()

    return entity_schema.dump(entity).data


def _get_and_validate_entity_metadata():
    data = get_json(request)
    print(data)
    return entity_schema.load(data).data


@metadata_api.route('/entity/<entity_id>/metadata/', methods=['PUT'])
def api_add_entity_metadata(entity_id):
    data = _get_and_validate_entity_metadata()
    entity = update_entity(entity_id, metadata_to_add=data['metadata'])

    return entity_schema.dump(entity).data


@metadata_api.route('/entity/<entity_id>/metadata/', methods=['DELETE'])
def api_delete_entity_metadata(entity_id):
    data = _get_and_validate_entity_metadata()
    entity = update_entity(entity_id, metadata_to_delete=data['metadata'])

    return entity_schema.dump(entity).data


@metadata_api.route('/entity/<entity_id>/', methods=['DELETE'])
def api_delete_entity(entity_id):
    entity = delete_entity(entity_id)

    return entity_schema.dump(entity).data
