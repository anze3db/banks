import time

from .bankinter import login as bankinter_login
from .business import login as business_login
from .common import ThreadHandler
from .n26 import login as n26_login


def keep_running(fun):
    _ = fun()
    time.sleep(100000)


def run(args):
    threads = ThreadHandler()
    if args.bankinter:
        threads.run_job(keep_running(bankinter_login))
    if args.business:
        threads.run_job(keep_running(business_login))
    if args.n26:
        threads.run_job(keep_running(n26_login))

    threads.join()
