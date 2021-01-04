import requests


def test_workers(app_fixture):
    requests.post(app_fixture.base_url+'/api/workers', json={
        'worker_id': 'TEST_ONE',
        'host': 'localhost',
        'port': 7600,
        'state': 1
    })
    requests.post(app_fixture.base_url + '/api/workers', json={
        'worker_id': 'TEST_TWO',
        'host': 'localhost',
        'port': 7601,
        'state': 1
    })
    response = requests.get(app_fixture.base_url + '/api/workers')
    assert response.ok
    body = response.json()
    assert len(body) == 2
    assert body[0]['worker_id'] == 'TEST_ONE'
    assert body[1]['worker_id'] == 'TEST_TWO'
