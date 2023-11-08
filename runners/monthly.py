import datetime as dt
import pathlib
import subprocess

from converters import run as run_convert

from .export import run as run_export


class ExportArgs:
    def __init__(self, bankinter=False, business=False, n26=False):
        self.bankinter = bankinter
        self.business = business
        self.n26 = n26


class ConvertArgs:
    def __init__(self, bankinter, business, n26):
        self.bankinter = [bankinter]
        self.personal = []
        self.n26 = [n26]
        self.visa = []
        self.business = [business]


def run(args):
    todays_date = dt.datetime.utcnow().strftime("%Y-%m")
    banks_dir = pathlib.Path.home() / "Documents" / "banks"
    export_dir = banks_dir / ("export-" + todays_date)
    if n26_exists := (export_dir / "n26-csv-transactions.csv").exists():
        print("N26: Already exported")
    if bankinter_exists := (export_dir / "ConsultaMovimentos.xls").exists():
        print("Bankinter: Already exported")
    if business_exists := (export_dir / "export.csv").exists():
        print("Business: Already exported")
    export_args = ExportArgs(
        bankinter=not bankinter_exists,
        business=not business_exists,
        n26=not n26_exists,
    )
    run_export(export_args)
    output = run_convert(
        ConvertArgs(
            bankinter=export_dir / "ConsultaMovimentos.xls",
            business=export_dir / "export.csv",
            n26=export_dir / "n26-csv-transactions.csv",
        )
    )
    output_file = banks_dir / (dt.datetime.utcnow().strftime("%Y-%m") + ".csv")
    pathlib.Path(output_file).write_text(output)
    print(f"Done! 🎉 {output_file}")
    subprocess.run(["open", str(output_file)])
