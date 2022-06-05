from runners.common import ProcessHanlder

from .bankinter import login as bankinter_login
from .business import login as business_login
from .n26 import login as n26_login


def run(args):
    processes = ProcessHanlder()
    if args.bankinter:
        processes.run_job(bankinter_login)
    if args.business:
        processes.run_job(business_login)
    if args.n26:
        processes.run_job(n26_login)
    processes.join()
