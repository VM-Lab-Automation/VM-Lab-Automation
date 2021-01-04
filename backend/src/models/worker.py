class Worker:

    def __init__(self, worker_id, state, host, api_port, last_update):
        self.last_update = last_update
        self.host = host
        self.api_port = api_port
        self.state = state
        self.worker_id = worker_id
