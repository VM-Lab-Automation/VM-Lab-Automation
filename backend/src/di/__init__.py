from flask import Config

from logic.auth_service import AuthService
from logic.db.lab_templates_repository import LabTemplatesRepository
from logic.db.labs_repository import LabsRepository
from logic.db.machines_repository import MachinesRepository
from logic.db.users_repository import UsersRepository
from logic.db.workers_repository import WorkersRepository
from logic.helpers.tokens_helper import TokensHelper
from logic.lab_service import LabsService
from logic.lab_templates_service import LabTemplatesService
from logic.worker_selector import WorkerSelector
from logic.worker_service import WorkerService
from logic.workers.worker_client import WorkerClientFactory


class DIContainer:
    def __init__(self, app_config: Config):

        self.workers_channel_client = WorkerClientFactory()

        self.labs_repository = LabsRepository(app_config)
        self.worker_repository = WorkersRepository(app_config)
        self.users_repository = UsersRepository(app_config)
        self.machines_repository = MachinesRepository(app_config)
        self.lab_templates_repository = LabTemplatesRepository(app_config)

        self.tokens_helper = TokensHelper(app_config)

        self.worker_service = WorkerService(self.worker_repository)
        self.worker_selector = WorkerSelector(self.worker_service)
        self.lab_templates_service = LabTemplatesService(self.lab_templates_repository)
        self.labs_service = LabsService(self.labs_repository,
                                        self.worker_selector,
                                        self.workers_channel_client,
                                        self.worker_service,
                                        self.machines_repository,
                                        self.lab_templates_service)
        self.auth_service = AuthService(self.users_repository, self.tokens_helper)

