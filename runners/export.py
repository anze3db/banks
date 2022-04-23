from .bankinter import export as bankinter_export
from .business import export as business_export
from .n26 import export as n26_export


def run(args):
    if args.bankinter:
        bankinter_export()
    if args.business:
        business_export()
    if args.n26:
        n26_export()
