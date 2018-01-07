from primal.metadata.exceptions import ConditionalUpdateException


def test_conditional_update_exception():
    e = ConditionalUpdateException('a')
    assert e.cause == 'a'
