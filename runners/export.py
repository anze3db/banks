from .bankinter.export import run as bankinter_run
from .business.export import run as business_run


def run(args):
    if args.bankinter:
        bankinter_run(args)
    if args.business:
        business_run(args)
