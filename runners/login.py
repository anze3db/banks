from .bankinter.common import login as bankinter_login
from .business import login as business_login
from .n26 import login as n26_login


def run(args):
    if args.bankinter:
        bankinter_login()
        input("Logged in 🔓")
    if args.business:
        business_login()
        input("Logged in 🔓")
    if args.n26:
        n26_login()
        input("Logged in 🔓")
