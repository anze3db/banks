import datetime as dt
import pathlib
import subprocess

from converters import run as run_convert

from .export import run as run_export


class ExportArgs:
    def __init__(self):
        self.bankinter = True
        self.business = True
        self.n26 = True


class ConvertArgs:
    def __init__(self, bankinter, business, n26):
        self.bankinter = [bankinter]
        self.personal = []
        self.n26 = [n26]
        self.visa = []
        self.business = [business]


def run(args):
    run_export(ExportArgs())
    todays_date = dt.datetime.utcnow().strftime("%Y-%m")
    banks_dir = pathlib.Path.home() / "Documents" / "banks"
    export_dir = banks_dir / ("export-" + todays_date)
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
