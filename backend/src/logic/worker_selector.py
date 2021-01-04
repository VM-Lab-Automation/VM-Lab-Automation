from logic.worker_service import WorkerService
import random

from models.worker import Worker


class WorkerSelector:
    def __init__(self, worker_service: WorkerService):
        self.worker_service = worker_service
        self.prev_worker = 0

    def next(self) -> Worker:
        all_workers = self.worker_service.get_workers()
        running_workers = [w for w in all_workers if w.state == 1]
        return random.choice(running_workers)
