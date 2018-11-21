import argparse
from commands.transfer import run as run_transfer
from commands.export import run as run_export

parser = argparse.ArgumentParser(description='Access your bank in a jiffy. 🚀')
subparsers = parser.add_subparsers(help='Choose an action to perform.', title='Options')

transfer_parser = subparsers.add_parser('transfer', help='Create a new domestic transfer. 💸')
transfer_parser.add_argument('--bankinter', dest='bank', action='store_const', const='bankinter', default='bankinter')
transfer_parser.set_defaults(func=run_transfer)

export_parser = subparsers.add_parser('export', help='Export transactions. 📋')
export_parser.add_argument('--bankinter', dest='bank', action='store_const', const='bankinter', default='bankinter')
export_parser.set_defaults(func=run_export)

convert_parser = subparsers.add_parser('convert', help='Convert exported transactions. 🔁')
export_parser.set_defaults(func=run_export)

args = parser.parse_args()

try:
    args.func(args)
except:
    parser.print_help()
