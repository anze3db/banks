import xlrd
import datetime

from dataclasses import dataclass
from decimal import Decimal


@dataclass(order=True)
class Transaction:
    date: datetime.datetime
    description: str
    amount: Decimal
    currency: str

    def csv(self):
        amount = "%.02f" % self.amount
        return f"{self.date},{amount},{self.currency},\"{self.description}\",\n"


class BusinessConfig:
    START_OFFSET = 3
    END_OFFSET = 0
    DESCRIPTION = 15
    AMOUNT = 1
    CURRENCY = 2
    DATE = 3
    DATE_FMT = '%Y-%m-%d'


class VisaConfig:
    START_OFFSET = 4
    END_OFFSET = 0
    DESCRIPTION = 2
    AMOUNT = 5
    CURRENCY = 6
    DATE = 0
    DATE_FMT = '%d.%m.%Y'


class PersonalConfig:
    START_OFFSET = 4
    END_OFFSET = 0
    DESCRIPTION = 12
    AMOUNT = 1
    CURRENCY = 2
    DATE = 4
    DATE_FMT = '%d.%m.%Y'


class BankinterConfig:
    START_OFFSET = 8
    END_OFFSET = 2
    DESCRIPTION = 2
    AMOUNT = 4
    CURRENCY = 5
    DATE = 0
    DATE_FMT = '%d-%m-%Y'


class Parser:
    def __init__(self, config):
        self.config = config

    def parse(self, filename):
        sheet = self.open(filename)
        res = []
        for row_idx in range(self.config.START_OFFSET, self.num_rows(sheet) - self.config.END_OFFSET):
            res.append(self.parse_row(sheet, row_idx))
        return res

    def parse_row(self, sheet, row_idx):
        amount = self.get_value(sheet, row_idx, self.config.AMOUNT)

        if isinstance(amount, float):
            amount = Decimal(amount)
        else:
            amount = Decimal(amount.replace('.', '').replace(',', '.'))

        return Transaction(
            datetime.datetime.strptime(self.get_value(sheet, row_idx, self.config.DATE), self.config.DATE_FMT),
            self.get_value(sheet, row_idx, self.config.DESCRIPTION),
            amount, 
            self.get_value(sheet, row_idx, self.config.CURRENCY)
        )


class XLSParser(Parser):
    def open(self, filename):
        workbook = xlrd.open_workbook(filename)
        return workbook.sheet_by_index(0)

    def num_rows(self, worksheet):
        return worksheet.nrows

    def get_value(self, worksheet, row_idx, col_idx):
        return worksheet.row_slice(rowx=row_idx)[col_idx].value


class CSVParser(Parser):
    def open(self, filename):
        with open(filename, encoding="windows-1250") as file:
            return file.readlines()

    def num_rows(self, sheet):
        return len(sheet)

    def get_value(self, sheet, row_idx, col_idx):
        return sheet[row_idx].split(';')[col_idx]
