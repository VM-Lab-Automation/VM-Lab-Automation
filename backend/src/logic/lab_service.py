from logic.db.labs_repository import LabsRepository
from logic.db.machines_repository import MachinesRepository
from logic.lab_templates_service import LabTemplatesService
from logic.worker_selector import WorkerSelector
from logic.workers.worker_client import WorkerClientFactory
from logic.worker_service import WorkerService
from models.lab import Lab
from models.lab_create_request import LabCreateRequest
import datetime
import uuid

from models.machine import Machine

MAX_VM_COUNT = 3


class LabsService:
    def __init__(self,
                 labs_repository: LabsRepository,
                 worker_selector: WorkerSelector,
                 worker_client_factory: WorkerClientFactory,
                 worker_service: WorkerService,
                 machines_repository: MachinesRepository,
                 lab_templates_service: LabTemplatesService):
        self.worker_client_factory = worker_client_factory
        self.labs_repository = labs_repository
        self.workers_selector = worker_selector
        self.worker_service = worker_service
        self.machines_repository = machines_repository
        self.lab_templates_service = lab_templates_service

    def __get_worker_client(self, worker):
        return self.worker_client_factory.for_worker(worker)

    def __send_to_worker(self, worker, lab_id, lab_template, vm_count, start_date, expiration_date):
        client = self.__get_worker_client(worker)
        client.send_job(lab_id, lab_template, vm_count, start_date, expiration_date)

    def __get_worker_client_by_lab_id(self, lab_id):
        lab = self.labs_repository.get_by_id(lab_id)
        worker = self.worker_service.get_worker(lab.worker_id)
        return self.__get_worker_client(worker)

    def create_lab(self, lab_request: LabCreateRequest):
        id = str(uuid.uuid4())
        worker = self.workers_selector.next()
        template = self.lab_templates_service.get_template_by_lab_name(lab_request.lab_template_name)
        lab = Lab(
            id,
            lab_request.lab_name,
            worker.worker_id,
            lab_request.user_id,
            datetime.datetime.now(),
            template.id,
            lab_request.start_date,
            lab_request.expiration_date,
            lab_request.description,
            len(lab_request.machines)
        )
        self.labs_repository.insert(lab)
        for i, machine in enumerate(lab_request.machines[:MAX_VM_COUNT]):
            machine_id = uuid.uuid4()
            self.machines_repository.insert(Machine(
                machine_id,
                id,
                'node-{}'.format(i+1),
                machine
            ))
        self.__send_to_worker(worker, id, template.code_name, min(len(lab_request.machines), MAX_VM_COUNT), lab_request.start_date, lab_request.expiration_date)
        return id

    def __split_labs_by_workers(self, labs: [Lab]):
        workers = self.worker_service.get_workers()
        result = {worker.worker_id: [] for worker in workers}
        for lab in labs:
            result[lab.worker_id].append(lab.id)
        return result, workers

    def get_labs_by_user(self, user_id):
        labs = self.labs_repository.get_all_by_user(user_id)
        lab_dict = {lab.id: lab for lab in labs}
        labs_by_workers, workers = self.__split_labs_by_workers(labs)
        for worker in workers:
            labs_id = labs_by_workers[worker.worker_id]
            if len(labs_id) > 0:
                client = self.__get_worker_client(worker)
                bulk_response = client.get_labs_status(labs_id)
                for response in bulk_response:
                    lab_dict[response['lab_id']].status = response['status']

        templates = {template.id: template.lab_name for template in self.lab_templates_service.get_all()}
        labs = list(lab_dict.values())
        return [{**lab.__dict__, "lab_type": templates[lab.lab_template_id]} for lab in labs]

    def get_lab_details(self, lab_id):
        lab = self.labs_repository.get_by_id(lab_id)
        worker = self.worker_service.get_worker(lab.worker_id)
        client = self.__get_worker_client(worker)

        machines = self.machines_repository.get_by_lab_id(lab_id)
        machines_names = dict(map(lambda machine: (machine.default_name, machine.display_name), machines))

        details = client.get_vm_details(lab_id)
        for machine in details.get('machines'):
            machine['id'] = machine['name']
            machine['name'] = machines_names.get(machine['name'])

            rdp_port = machine.pop('rdp_port') if 'rdp_port' in machine else 0
            ssh_port = machine.pop('ssh_port') if 'ssh_port' in machine else 0
            machine['rdp_address'] = "{}:{}".format(worker.host, rdp_port)
            machine['ssh_address'] = "{}:{}".format(worker.host, ssh_port)
        details['lab_name'] = lab.name
        return details

    def restart_lab_machine(self, lab_id, vm_id):
        client = self.__get_worker_client_by_lab_id(lab_id)
        client.restart_machine(lab_id, vm_id)

    def get_lab_files(self, lab_id):
        client = self.__get_worker_client_by_lab_id(lab_id)
        return client.get_machine_files(lab_id)
