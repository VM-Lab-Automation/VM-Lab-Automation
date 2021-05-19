import pytest
from mock import MagicMock
from logic.lab_service import LabsService
from models.lab import Lab
from models.lab_template import LabTemplate
from models.machine import Machine
from models.worker import Worker


class ServiceTestDependencies:
    def __init__(self):
        self.user_id = 1
        self.labs_repository = MagicMock()
        self.machines_repository = MagicMock()
        self.user_id = MagicMock()
        self.lab_templates_service = MagicMock()
        self.worker_selector = MagicMock()
        self.worker_client_factory = MagicMock()
        self.workers_service = MagicMock()
        self.worker1_client = MagicMock()
        self.worker2_client = MagicMock()
        self.worker3_client = MagicMock()
        self.labs = []
        self.workers = []


@pytest.fixture()
def tests_setup():
    result = ServiceTestDependencies()

    result.labs = [
        Lab("id1", "name", "worker1", 1, "ss", 2, "startDate", "date", 1, "description"),
        Lab("id2", "name", "worker2", 1, "ss", 1, "startDate", "date", 1, "description"),
        Lab("id3", "name", "worker2", 1, "ss", 2, "startDate", "date", 1, "description"),
        Lab("id4", "name", "worker3", 1, "ss", 1, "startDate", "date", 1, "description")
    ]
    workers = [
        Worker("worker1", "ok", "HOST1", "PORT1", "last"),
        Worker("worker2", "ok", "HOST2", "PORT2", "last"),
        Worker("worker3", "ok", "HOST3", "PORT3", "last")
    ]
    result.labs_repository.get_all_by_user.return_value = result.labs
    result.workers_service.get_workers.return_value = workers

    def workers_factory_side_effect(*args, **kwargs):
        if args[0] == workers[0]:
            return result.worker1_client
        elif args[0] == workers[1]:
            return result.worker2_client
        elif args[0] == workers[2]:
            return result.worker3_client

    result.worker_client_factory.for_worker.side_effect = workers_factory_side_effect

    result.worker1_client.get_labs_status.return_value = [{
        'lab_id': 'id1',
        'status': 'running'
    }]
    result.worker2_client.get_labs_status.return_value = [{
        'lab_id': 'id2',
        'status': 'running'
    }, {
        'lab_id': 'id3',
        'status': 'not_running'
    }]
    result.worker3_client.get_labs_status.return_value = [{
        'lab_id': 'id4',
        'status': 'not_running'
    }]

    result.lab_templates_service.get_all.return_value = [
        LabTemplate(1, "BASIC", "Basic"),
        LabTemplate(2, "KATHARA", "Kathara")
    ]

    result.workers = workers
    return result


def test_get_labs_should_return_labs(tests_setup):
    sut = LabsService(tests_setup.labs_repository, tests_setup.worker_selector, tests_setup.worker_client_factory,
                      tests_setup.workers_service, tests_setup.machines_repository, tests_setup.lab_templates_service)
    result = list(sut.get_labs_by_user(tests_setup.user_id))
    assert result[0] == {**tests_setup.labs[0].__dict__, 'lab_type': 'Kathara', 'status': 'running'}
    assert result[1] == {**tests_setup.labs[1].__dict__, 'lab_type': 'Basic', 'status': 'running'}
    assert result[2] == {**tests_setup.labs[2].__dict__, 'lab_type': 'Kathara', 'status': 'not_running'}
    assert result[3] == {**tests_setup.labs[3].__dict__, 'lab_type': 'Basic', 'status': 'not_running'}


def test_get_lab_details_should_return_lab_details(tests_setup):
    tests_setup.workers_service.get_worker.return_value = tests_setup.workers[1]
    tests_setup.worker2_client.get_vm_details.return_value = {
            "lab_id": "id2",
            "status": "running",
            "machines": [
                {
                    "name": "node-1",
                    "status": "running",
                    "rdp_port": "1111",
                    "ssh_port": "2222",
                    "login": "login",
                    "password": "password"
                }
            ]
        }

    tests_setup.machines_repository.get_by_lab_id.return_value = [
        Machine("machine_id", "id2", "node-1", "machine_name")
    ]

    tests_setup.labs_repository.get_by_id.return_value = tests_setup.labs[1]

    sut = LabsService(tests_setup.labs_repository, tests_setup.worker_selector, tests_setup.worker_client_factory,
                      tests_setup.workers_service, tests_setup.machines_repository, tests_setup.lab_templates_service)
    result = sut.get_lab_details("id2")

    assert result == {
        "lab_id": "id2",
        "status": "running",
        "lab_name": "name",
        "machines": [{
            "id": "node-1",
            "name": "machine_name",
            "status": "running",
            "rdp_address": "HOST2:1111",
            "ssh_address": "HOST2:2222",
            "login": "login",
            "password": "password"
        }]
    }
