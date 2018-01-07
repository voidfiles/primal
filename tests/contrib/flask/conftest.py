from flask import Flask

import pytest


@pytest.fixture
def app():
    from primal.contrib.flask.api import metadata_api
    app = Flask(__name__)
    app.register_blueprint(metadata_api, url_prefix='')

    return app
