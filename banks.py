import argparse

from converters import run as run_convert
from runners.export import run as run_export
from runners.login import run as run_login
from runners.transfer import run as run_transfer

parser = argparse.ArgumentParser(
    prog="banks", description="Access your bank in a jiffy. 🚀"
)
subparsers = parser.add_subparsers(help="Choose an action to perform.", title="Options")


export_parser = subparsers.add_parser("login", help="Login to online banking. 🔒")
export_parser.add_argument(
    "--bankinter",
    action="store_true",
)
export_parser.add_argument(
    "--business",
    action="store_true",
)
export_parser.add_argument(
    "--n26",
    action="store_true",
)
export_parser.set_defaults(func=run_login)

transfer_parser = subparsers.add_parser(
    "transfer", help="Create a new domestic transfer. 💸"
)
transfer_parser.add_argument(
    "--bankinter",
    dest="bank",
    action="store_const",
    const="bankinter",
    default="bankinter",
)
transfer_parser.set_defaults(func=run_transfer)

export_parser = subparsers.add_parser("export", help="Export transactions. 📋")
export_parser.add_argument(
    "--bankinter",
    action="store_true",
)
export_parser.add_argument(
    "--business",
    action="store_true",
)
export_parser.add_argument(
    "--n26",
    action="store_true",
)
export_parser.set_defaults(func=run_export)

convert_parser = subparsers.add_parser(
    "convert", help="Convert exported transactions. 🔁"
)
convert_parser.add_argument("--bankinter", dest="bankinter", nargs="+", default=[])
convert_parser.add_argument("--personal", dest="personal", nargs="+", default=[])
convert_parser.add_argument("--visa", dest="visa", nargs="+", default=[])
convert_parser.add_argument("--business", dest="business", nargs="+", default=[])
convert_parser.add_argument("--n26", dest="n26", nargs="+", default=[])
convert_parser.set_defaults(func=run_convert)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
