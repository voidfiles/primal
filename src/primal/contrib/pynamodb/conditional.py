from contextlib import contextmanager

from botocore.exceptions import ClientError
from pynamodb.exceptions import PutError, UpdateError


def is_conditional_check(e):
    if isinstance(e.cause, ClientError):
        code = e.cause.response['Error'].get('Code')
        if code == "ConditionalCheckFailedException":
            return True

    return False


@contextmanager
def raise_for_conditional_failure(exception_cls):
    try:
        yield
    except (PutError, UpdateError) as e:
        if is_conditional_check(e):
            raise exception_cls(e)

        raise
