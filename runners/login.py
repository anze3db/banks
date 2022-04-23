from .bankinter.common import login as bankinter_login
from .business.export import login as business_login


def run(args):
    if args.bankinter:
        bankinter_login()
    if args.business:
        business_login()
    input("Logged in 🔓")
