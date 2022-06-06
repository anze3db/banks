from .bankinter import export as bankinter_export
from .business import export as business_export
from .common import ThreadHandler
from .n26 import export as n26_export


def run(args):
    threads = ThreadHandler()
    if args.bankinter:
        threads.run_job(bankinter_export)
    if args.business:
        threads.run_job(business_export)
    if args.n26:
        threads.run_job(n26_export)
