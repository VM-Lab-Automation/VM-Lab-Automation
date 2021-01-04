from worker.clients import MainServerClient


def keep_alive_job(worker):
    client = MainServerClient()
    client.update_worker_state(worker.id, worker.host, worker.port, 1)
