from mock import MagicMock
from logic.lab_service import LabsService
from models.lab import Lab
from models.lab_template import LabTemplate
from models.worker import Worker

def test_get_labs_should_return_labs():
    user_id = 1
    labs_repository = MagicMock()
    machines_repository = MagicMock()
    lab_templates_service = MagicMock()
    worker_selector = MagicMock()
    worker_client_factory = MagicMock()
    workers_service = MagicMock()
    worker1_client = MagicMock()
    worker2_client = MagicMock()
    worker3_client = MagicMock()
    labs = [
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
    labs_repository.get_all_by_user.return_value = labs
    workers_service.get_workers.return_value = workers

    def workers_factory_side_effect(*args, **kwargs):
        if args[0] == workers[0]:
            return worker1_client
        elif args[0] == workers[1]:
            return worker2_client
        elif args[0] == workers[2]:
            return worker3_client
    worker_client_factory.for_worker.side_effect = workers_factory_side_effect

    worker1_client.get_labs_status.return_value = [{
        'lab_id': 'id1',
        'status': 'running'
    }]
    worker2_client.get_labs_status.return_value = [{
        'lab_id': 'id2',
        'status': 'running'
    }, {
        'lab_id': 'id3',
        'status': 'not_running'
    }]
    worker3_client.get_labs_status.return_value = [{
        'lab_id': 'id4',
        'status': 'not_running'
    }]

    lab_templates_service.get_all.return_value = [
        LabTemplate(1, "BASIC", "Basic"),
        LabTemplate(2, "KATHARA", "Kathara")
    ]

    sut = LabsService(labs_repository, worker_selector, worker_client_factory, workers_service, machines_repository, lab_templates_service)
    result = list(sut.get_labs_by_user(user_id))
    assert result[0] == {**labs[0].__dict__, 'lab_type': 'Kathara', 'status': 'running'}
    assert result[1] == {**labs[1].__dict__, 'lab_type': 'Basic', 'status': 'running'}
    assert result[2] == {**labs[2].__dict__, 'lab_type': 'Kathara', 'status': 'not_running'}
    assert result[3] == {**labs[3].__dict__, 'lab_type': 'Basic', 'status': 'not_running'}
