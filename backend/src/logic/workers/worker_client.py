from io import BytesIO

import requests

from logic.helpers.date_helper import DateHelper
from models.worker import Worker


class WorkerClientFactory:
    def for_worker(self, worker: Worker):
        return WorkerClient('http://{}:{}'.format(worker.host, worker.api_port))


class WorkerClient:
    def __init__(self, worker_address):
        self.worker_address = worker_address

    def send_job(self, lab_id, lab_template, vm_count, start_date, expiration_date):
        requests.post(self.worker_address + '/lab', json={
            'lab_id': str(lab_id),
            'lab_template': lab_template,
            'vm_count': vm_count,
            'start_date': DateHelper.date_to_ISO_string(start_date),
            'expiration_date': DateHelper.date_to_ISO_string(expiration_date)
        })

    def get_labs_status(self, lab_ids: [str]):
        url = "{}/labs/status".format(self.worker_address)
        response = requests.get(url, params={
            'lab_ids': lab_ids
        })
        return response.json()

    def get_vm_details(self, lab_id):
        url = "{}/labs/{}/status".format(self.worker_address, lab_id)
        response = requests.get(url)
        return response.json()

    def restart_machine(self, lab_id, vm_id):
        url = "{}/labs/{}/machine/{}/start".format(self.worker_address, lab_id, vm_id)
        requests.put(url)

    def get_machine_files(self, lab_id) -> BytesIO:
        url = "{}/labs/{}/machine_files".format(self.worker_address, lab_id)
        response = requests.get(url)
        return BytesIO(response.content)
