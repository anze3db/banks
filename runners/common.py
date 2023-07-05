from threading import Thread

from selenium import webdriver  # type: ignore


class ThreadHandler:
    def __init__(self):
        self.threads = []

    def run_job(self, job):
        job_thread = Thread(target=job)
        job_thread.start()
        self.threads.append(job_thread)

    def join(self):
        for thread in self.threads:
            thread.join()


def get_chromedriver():
    try:
        return webdriver.Chrome()
    except Exception as e:
        print("Possible issue with Chromedriver", e)
        raise
