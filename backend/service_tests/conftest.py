import inspect
import os
import sqlite3
import sys
import threading
import pytest
from wiremock.server import WireMockServer

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


class TestsFixture:

    def __init__(self, base_url, wiremock_server):
        self.base_url = base_url
        self.wiremock_server = wiremock_server


@pytest.fixture(scope="session", autouse=True)
def app_fixture():
    """DOCS"""
    if os.path.exists('test_db.db'):
        os.remove('test_db.db')
    from setup_db import init_db
    init_db('test_db.db')
    with WireMockServer(port=7600) as wiremock_server:
        os.environ['FLASK_ENV'] = 'Testing'

        from service_interface import app

        assert app is not None
        app_thread = threading.Thread(target=app.run, kwargs={'port': 5008})
        app_thread.setDaemon(True)
        app_thread.start()
        yield TestsFixture('http://localhost:5008', wiremock_server)
