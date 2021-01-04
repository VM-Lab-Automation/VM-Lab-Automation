from worker.labs.lab_status import LabStatus
from worker.logger import get_logger
from worker.utils.date_helper import parse_date
from worker.worker import Worker
import datetime


def expire_labs_job(worker: Worker):
    log = get_logger(__name__)
    log.info('Starting expire labs job')
    for lab in worker.labs():
        lab_status = lab.status(include_machines=False)
        expiration_date_str = lab_status.get('expiration_date')
        status = LabStatus[lab_status.get('status')]
        if status == LabStatus.EXPIRED:
            continue

        expiration_date = None
        try:
            expiration_date = parse_date(expiration_date_str)
        except:
            log.warning('Lab with id {} has invalid expiration date'.format(lab.id))
            continue

        if expiration_date is not None:
            if datetime.datetime.now() > expiration_date:
                log.info('Expiring lab with id {} since it\'s after expiration time'.format(lab.id))
                lab.expire()

    log.info('Expire labs job ended')