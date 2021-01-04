import os
import requests
import logging


class MainServerClient:

    def __init__(self):
        self.address = os.getenv('MAIN_SERVER_URL')

    def __get_path(self, suffix):
        return '{}{}'.format(self.address, suffix)

    def update_worker_state(self, worker_id, host, port, state):
        try:
            requests.post(self.__get_path('/workers'), json={
                'worker_id': worker_id,
                'host': host,
                'port': port,
                'state': state
            })
        except BaseException as e:
            logging.warning('Cannot update worker state. Backend seems to be unavailable. %s' % e)
