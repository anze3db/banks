import datetime as dt
import pathlib
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
        options = webdriver.ChromeOptions()
        # Get today's date as ISO string:
        todays_date = dt.datetime.utcnow().strftime("%Y-%m")
        dir_name = (
            pathlib.Path.home() / "Documents" / "banks" / ("export-" + todays_date)
        )
        pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
        options.add_experimental_option(
            "prefs",
            {"download.default_directory": str(dir_name)},
        )
        return webdriver.Chrome(options=options)
    except Exception as e:
        print("Possible issue with Chromedriver", e)
        raise
