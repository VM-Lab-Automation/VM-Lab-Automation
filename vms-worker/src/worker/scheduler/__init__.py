import threading
import time

import schedule

from worker.scheduler.start_labs import start_labs_job
from worker.scheduler.expire_labs import expire_labs_job
from worker.scheduler.keep_alive import keep_alive_job
from worker.utils.run_async import run_async


def __scheduler_thread():
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(10)


def setup_scheduler(worker):
    schedule.every(10).seconds.do(keep_alive_job, worker)
    schedule.every(1).minutes.do(run_async(start_labs_job), worker)
    schedule.every(5).minutes.do(run_async(expire_labs_job), worker)

    thread = threading.Thread(target=__scheduler_thread)
    thread.setDaemon(True)
    thread.start()
