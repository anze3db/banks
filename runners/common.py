from selenium import webdriver  # type: ignore


class ProcessHanlder:
    def __init__(self):
        self.processes = []

    def run_job(self, job):
        job_process = Process(target=job)
        job_process.start()
        self.processes.append(job_process)

    def join(self):
        for process in self.processes:
            process.join()


def get_chromedriver():
    try:
        return webdriver.Chrome("./chromedriver")
    except Exception as e:
        print("Possible issue with Chromedriver", e)
        raise
