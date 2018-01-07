import pytest
from botocore.exceptions import ClientError

from pynamodb.exceptions import PutError

from primal.contrib.pynamodb.conditional import (is_conditional_check,
                                                 raise_for_conditional_failure)


def build_client_error(action="UpdateItem",
                       code="ConditionalCheckFailedException",
                       headers=None):

    return ClientError({
        'Error': {
            'Code': code,
            'Message': ''
        },
        'ResponseMetadata': {
            'HTTPHeaders': headers if headers else {}
        }
    }, action)


class MockPutError(PutError):
    def __init__(self, cause=None, *args, **kwargs):
        Exception.__init__(self)
        self.cause = cause


def test_is_conditional_check():

    tests = [
        (MockPutError(cause=build_client_error()), True),
        (MockPutError(), False),
    ]

    for test in tests:
        assert is_conditional_check(test[0]) is test[1]


def test_raise_for_conditional_failure():

    with pytest.raises(PutError):
        with raise_for_conditional_failure(ValueError):
            raise MockPutError()

    with pytest.raises(ValueError):
        with raise_for_conditional_failure(ValueError):
            raise MockPutError(cause=build_client_error())
