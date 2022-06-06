from queue import Queue
from threading import Thread

from selenium import webdriver  # type: ignore

input_queue: Queue = Queue()
input_request_queue: Queue = Queue()


class ThreadHandler:
    def __init__(self):
        self.threads = []

    def run_job(self, job):
        job_process = Thread(target=job)
        job_process.start()
        self.threads.append(job_process)

    def join(self):
        for process in self.threads:
            process.join()


def get_chromedriver():
    try:
        return webdriver.Chrome("./chromedriver")
    except Exception as e:
        print("Possible issue with Chromedriver", e)
        raise
