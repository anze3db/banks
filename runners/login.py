import time

from .bankinter import login as bankinter_login
from .business import login as business_login
from .common import ThreadHandler, input_queue, input_request_queue
from .n26 import login as n26_login


def keep_running(fun):
    _ = fun()
    time.sleep(100000)


def run(args):
    processes = ThreadHandler()
    if args.bankinter:
        processes.run_job(keep_running(bankinter_login))
    if args.business:
        processes.run_job(keep_running(business_login))
    if args.n26:
        processes.run_job(keep_running(n26_login))
    while True:
        message = input_request_queue.get()
        print(message)
        response = input()
        input_queue.put(response)

    processes.join()
