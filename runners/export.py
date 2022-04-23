from .bankinter.export import run as bankinter_run
from .business import run as business_run
from .n26 import export as n26_export


def run(args):
    if args.bankinter:
        bankinter_run(args)
    if args.business:
        business_run(args)
    if args.n26:
        n26_export()
