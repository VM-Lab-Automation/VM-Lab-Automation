from worker.labs.lab_status import LabStatus
from worker.logger import get_logger
from worker.utils.date_helper import parse_date
from worker.worker import Worker
import datetime


def start_labs_job(worker: Worker):
    log = get_logger(__name__)
    log.info('Starting start labs job')
    for lab in worker.labs():
        lab_status = lab.status(include_machines=False)
        status = LabStatus[lab_status.get('status')]
        if status != LabStatus.PREPARING:
            continue
        start_date_str = lab_status['start_date']
        start_date = None
        try:
            start_date = parse_date(start_date_str)
        except:
            log.warning('Lab with id {} has invalid start date'.format(lab.id))
            continue
        if start_date is not None:
            if datetime.datetime.now() > start_date:
                log.info('Starting lab {}'.format(lab.id))
                lab.start()

    log.info('Start labs job ended')