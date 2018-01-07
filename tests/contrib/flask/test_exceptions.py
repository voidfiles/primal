from primal.contrib.flask.exceptions import APIException, format_error_message


def test_format_error_message():
    assert format_error_message("a", "b", "c") == {
        "error_message": "a",
        "error_info": "b",
        "error_slug": "c",
    }


def test_api_exception_to_dict():
    e = APIException("test", 410, "my-slug", info={"stuff": "stuff"})
    assert e.to_dict() == {
        "error_message": "test",
        "error_info": {"stuff": "stuff"},
        "error_slug": "my-slug",
    }


def test_generic_api_exception():
    e = APIException("test")
    assert e.status_code == 400
    assert e.message == "test"
    assert e.info is None
    assert e.slug == "non-specific"


def test_custom_api_exception():
    e = APIException("test", 410, "my-slug", info={"stuff": "stuff"})
    assert e.status_code == 410
    assert e.message == "test"
    assert e.info == {"stuff": "stuff"}
    assert e.slug == "my-slug"
