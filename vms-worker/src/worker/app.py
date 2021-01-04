import os


from worker.api import register_endpoints
from flask import Flask
from flask_restplus import Api

from worker.labs.labs_repository import LabsRepository
from worker.lab_templates import LabTemplatesRepository
from worker.logger import get_logger
from worker.scheduler import setup_scheduler
from worker.worker import Worker


def create_app():
    log = get_logger(__name__)
    log.info('Setting up worker...')
    WORKER_ID = os.getenv('WORKER_ID')
    MAIN_SERVER_URL = os.getenv('MAIN_SERVER_URL')
    WORKER_HOST = os.getenv('WORKER_HOST')
    WORKER_PORT = os.getenv('WORKER_PORT')
    log.info("""
        Parameters:
            WORKER_ID: {}
            MAIN_SERVER_URL: {},
            WORKER_HOST: {},
            WORKER_PORT: {}
    """.format(WORKER_ID, MAIN_SERVER_URL, WORKER_HOST, WORKER_PORT))
    worker = Worker(WORKER_ID, WORKER_HOST, WORKER_PORT, LabsRepository(), LabTemplatesRepository())

    log.info("Setting up scheduled jobs")
    setup_scheduler(worker)

    log.info("Setting up api")
    app = Flask('VMs worker')
    api = Api(app)

    register_endpoints(api, worker)

    return app


app = create_app()
