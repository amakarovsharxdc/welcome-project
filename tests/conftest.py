from fastapi.testclient import TestClient
import pytest

from service.app import app


@pytest.fixture(scope='function', name='api')
def fixture_api():
    yield app.api


@pytest.fixture(scope='function', name='storage')
def fixture_storage(api):
    api.storage.tree.clear()
    yield api.storage


@pytest.fixture(scope='session', name='client')
def fixture_client():
    with TestClient(app) as client:
        yield client
