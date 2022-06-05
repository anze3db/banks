from .bankinter import export as bankinter_export
from .business import export as business_export
from .common import ProcessHanlder
from .n26 import export as n26_export


def run(args):
    processes = ProcessHanlder()
    if args.bankinter:
        processes.run_job(bankinter_export)
    if args.business:
        processes.run_job(business_export)
    if args.n26:
        processes.run_job(n26_export)

    print("started processes")
    processes.join()
    print("done")
