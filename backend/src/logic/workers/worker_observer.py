import threading
import time
from datetime import datetime
from logger import get_logger
from logic.helpers.date_helper import DateHelper


def __workers_observer_thread(worker_repository):
    log = get_logger(__name__)
    while True:
        workers = worker_repository.get_all_running()
        now = datetime.now()
        for w in workers:
            wlu = DateHelper.datetime_from_ISO_string(w.last_update)
            if (now - wlu).total_seconds() >= 15:
                log.warning("Worker with id {} seems to be unavailable. Changing state to not running.".format(w.worker_id))
                w.state = 2
                worker_repository.insert_or_update(w)
        time.sleep(5)


def start_workers_observer_thread(worker_repository):
    thread = threading.Thread(target=__workers_observer_thread, args=[worker_repository])
    thread.setDaemon(True)
    thread.start()
    return thread
