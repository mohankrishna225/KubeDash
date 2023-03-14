import pytest, logging
from flask.testing import FlaskClient
from kubedash import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app("testing")
    yield app

@pytest.fixture(scope='module')
def client(app):
    ctx = app.test_request_context()
    # file deepcode ignore DisablesCSRFProtection/test: <please specify a reason of ignoring this>
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()
    
