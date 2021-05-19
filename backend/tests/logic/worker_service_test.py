from mock import MagicMock

from logic.worker_service import WorkerService
from models.worker import Worker


def test_insert_or_update_should_be_called():
    workers_repository = MagicMock()

    workers = [
        Worker("worker1", "ok", "HOST1", "PORT1", "last"),
        Worker("worker2", "ok", "HOST2", "PORT2", "last")
    ]
    worker_to_add = Worker("worker3", "ok", "HOST3", "PORT3", "last")
    workers_repository.return_value = workers

    worker_service = WorkerService(workers_repository)

    worker_service.update_state(
        worker_to_add.worker_id,
        worker_to_add.state,
        worker_to_add.host,
        worker_to_add.api_port
    )

    workers_repository.insert_or_update.assert_called()
