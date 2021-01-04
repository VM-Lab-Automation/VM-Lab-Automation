import json

import requests
from wiremock.constants import Config
from wiremock.resources.mappings import Mapping, MappingRequest, HttpMethods, MappingResponse
from wiremock.resources.mappings.resource import Mappings


def test_labs(app_fixture):
    login_response = requests.post(app_fixture.base_url + '/api/auth/login', json={
        'username': 'user1',
        'password': 'pass',
    })
    assert login_response.ok

    requests.post(app_fixture.base_url+'/api/workers', json={
        'worker_id': 'TEST_ONE',
        'host': 'localhost',
        'port': app_fixture.wiremock_server.port,
        'state': 1
    })
    requests.post(app_fixture.base_url + '/api/workers', json={
        'worker_id': 'TEST_TWO',
        'host': 'localhost',
        'port': 7601,
        'state': 2
    })
    post_response = requests.post(app_fixture.base_url + '/api/labs', json={
        'lab_name': 'First lab',
        'lab_type': 'Kathara',
        'start_date': '2020-04-06T14:00:00.000Z',
        'expiration_date': '2020-04-08T14:00:00.000Z',
        'description': 'description',
        'machines': [
            'm1', 'm2'
        ]
    }, headers={
        'Authorization': 'Bearer {}'.format(login_response.json()['token'])
    })

    assert post_response.ok
    lab_id = post_response.json()
    Config.base_url = 'http://localhost:{}/__admin'.format(app_fixture.wiremock_server.port)

    mapping = Mapping(
        priority=100,
        request=MappingRequest(
            method=HttpMethods.GET,
            url_path='/labs/status',
            query_parameters={
                'lab_ids': {
                    'matches': '.*'
                }
            }
        ),
        response=MappingResponse(
            status=200,
            body = json.dumps([{
                'lab_id': lab_id,
                'status': 'running'
            }])
        ),
        persistent=True,
    )
    Mappings.create_mapping(mapping=mapping)

    response = requests.get(app_fixture.base_url + '/api/labs', headers={
        'Authorization': 'Bearer {}'.format(login_response.json()['token'])
    })
    assert response.ok
    body = response.json()
    assert len(body) == 1
    assert body[0]['id'] == lab_id
    assert body[0]['status'] == 'running'
