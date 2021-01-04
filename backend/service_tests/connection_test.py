import requests


def test_is_connection(app_fixture):
    response = requests.get(app_fixture.base_url+'/api')
    assert response.ok
