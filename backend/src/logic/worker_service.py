from logic.helpers.date_helper import DateHelper
from logic.db.workers_repository import WorkersRepository
from models.worker import Worker
from datetime import datetime


class WorkerService:

    def __init__(self, worker_repository: WorkersRepository):
        self.worker_repository = worker_repository

    def update_state(self, worker_id, state, host, port):
        self.worker_repository.insert_or_update(Worker(worker_id, state, host, port, DateHelper.date_to_ISO_string(datetime.now())))

    def get_workers(self):
        return self.worker_repository.get_all()

    def get_worker(self, worker_id) -> Worker:
        return self.worker_repository.get_by_id(worker_id)
