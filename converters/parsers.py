import datetime
from dataclasses import dataclass
from decimal import Decimal

import xlrd


@dataclass(order=True)
class Transaction:
    date: datetime.datetime
    description: str
    amount: Decimal
    currency: str
    src: str
    category: str = ""

    def csv(self):
        amount = "%.02f" % self.amount
        return f'{self.date},{amount},{self.currency},"{self.description}",{self.src},{self.category}\n'


class BusinessConfig:
    START_OFFSET = 3
    END_OFFSET = 0
    DESCRIPTION = [15, 16, 17, 9]
    AMOUNT = 1
    CURRENCY = 2
    DATE = 3
    DATE_FMT = "%Y-%m-%d"
    DELIMITER = ";"
    SRC_NAME = "UniCredit Business"
    CATEGORY = None
    DESCR_INDEX = 15
    DESCRIPTION_MAPPINGS = {
        "STROŠEK VODENJA": "Bank",
        "PROVIZIJA ELEKTR. STAND.": "Bank",
        "STR.EVID.PRILIVA-EKSTERNI": "Bank",
        "SI1922633588-45004": "Taxes",
        "SI1922633588-44008": "Taxes",
        "SI1922633588-43001": "Taxes",
        "SI1922633588-42005": "Taxes",
        "SI1922633588-62006": "Taxes",
        "SI1922633588-40002": "Taxes",
        "PROVIZIJA": "Bank",
        "GO TEL": "SP Expenses",
    }


class VisaConfig:
    START_OFFSET = 4
    END_OFFSET = 0
    DESCRIPTION = [2]
    AMOUNT = 5
    CURRENCY = 6
    DATE = 0
    DATE_FMT = "%d.%m.%Y"
    DELIMITER = ";"
    SRC_NAME = "UniCredit Visa"
    CATEGORY = None
    DESCR_INDEX = 2
    DESCRIPTION_MAPPINGS = {}


class PersonalConfig:
    START_OFFSET = 4
    END_OFFSET = 0
    DESCRIPTION = [12]
    AMOUNT = 1
    CURRENCY = 2
    DATE = 4
    DATE_FMT = "%d.%m.%Y"
    DELIMITER = ";"
    SRC_NAME = "UniCredit Personal"
    CATEGORY = None
    DESCR_INDEX = 12
    DESCRIPTION_MAPPINGS = {}


class BankinterConfig:
    START_OFFSET = 8
    END_OFFSET = 2
    DESCRIPTION = [2]
    AMOUNT = 4
    CURRENCY = 5
    DATE = 0
    DATE_FMT = "%d-%m-%Y"
    DELIMITER = ";"
    SRC_NAME = "Bankinter"
    CATEGORY = None
    DESCR_INDEX = 2
    DESCRIPTION_MAPPINGS = {
        "TRANSACCOES BXV": "Transport & Car",
        "EMPRESTIMO 90173353667-COB": "Apartment",
        "Comissao de Processamento Prestacao 038": "Bank",
        "Imposto do Selo sobre Com.Proc.Prest.038": "Bank",
        "IMPOSTO DO SELO SOBRE JUROS E COMISSOES": "Bank",
        "PAGAMENTO DE SEGUROS": "Apartment",
        "Cobranca DD-20000136755 FIDELIDADE COMP": "Health & Personal Care",
        "Cobranca DD-05511019025 NOS Comunicacoe": "Household & Utilities",
        "Cobranca DD-00159121887 AGUAS DE CASCAI": "Household & Utilities",
        "Cobranca DD-00000252231 GALP POWER": "Household & Utilities",
        "Cobranca DD-00000252231 PETROGAL": "Household & Utilities",
        "FARMACIA": "Health & Personal Care",
    }


class N26Config:
    START_OFFSET = 1
    END_OFFSET = 0
    DESCRIPTION = [1, 2, 3, 4]
    AMOUNT = 5
    CURRENCY = None
    DATE = 0
    DATE_FMT = '"%Y-%m-%d'
    DELIMITER = '","'
    SRC_NAME = "n26"
    CATEGORY = None
    DESCR_INDEX = 1
    DESCRIPTION_MAPPINGS = {
        "Charib": "Apartment",
        "LINODE": "SP Expenses",
        "MAILGUN TECHNOLOGIES,": "SP Expenses",
        "NETFLIX.COM": "Household & Utilities",
        "Charib": "Household & Utilities",
        "UBER   *EATS": "Bars & Restaurants",
        "APPLE.COM": "SP Expenses",
        "ARARATE": "Bars & Restaurants",
        "NAME-CHEAP.COM": "SP Expenses",
        "Booking.com": "Travel & Holidays",
        "RESTAURANT": "Bars & Restaurants",
        "PRACTICE PORTUGUESE": "Education",
        "LIDL": "Food & Groceries",
        "MOJ.A1.SI": "Household & Utilities",
        "PEIXARIA ESTORIL MAR": "Food & Groceries",
        "PINGO DOCE": "Food & Groceries",
        "GROUND BURGUER": "Bars & Restaurants",
        "OBRESTI": "Bank",
        "STR.EVID.PRILIVA": "Bank",
        "STROŠEK VODENJA": "Bank",
        "CONTINENTE": "Food & Groceries",
        "INTERMARCHE ERICEIRA": "Transport & Car",
        "CELEIRO DA ALDEIA": "Food & Groceries",
        "LUAR DA BARRA": "Bars & Restaurants",
        "POSTO ESTORIL V 3": "Transport & Car",
    }


class Parser:
    def __init__(self, config):
        self.config = config

    def open(self, filename: str):
        raise NotImplementedError()

    def get_value(self, sheet, row_idx, col_idx):
        raise NotImplementedError()

    def num_rows(self, sheet):
        raise NotImplementedError()

    def parse(self, filename):
        sheet = self.open(filename)
        res = []
        for row_idx in range(
            self.config.START_OFFSET, self.num_rows(sheet) - self.config.END_OFFSET
        ):
            res.append(self.parse_row(sheet, row_idx))
        return res

    def get_description(self, sheet, row_idx: int) -> str:
        return "\n".join(
            [
                self.get_value(sheet, row_idx, col_idx)
                for col_idx in self.config.DESCRIPTION
                if self.get_value(sheet, row_idx, col_idx).strip()
            ]
        )

    def get_category(self, sheet, row_idx: int) -> str:
        description = self.get_value(sheet, row_idx, self.config.DESCR_INDEX)
        for definition, category in self.config.DESCRIPTION_MAPPINGS.items():
            if definition in description:
                return category
        if self.config.CATEGORY:
            return self.get_value(sheet, row_idx, self.config.CATEGORY)
        return ""

    def parse_row(self, sheet, row_idx):
        amount = self.get_value(sheet, row_idx, self.config.AMOUNT)
        if isinstance(amount, float):
            amount = Decimal(amount)
        elif self.config.DELIMITER == '","':
            amount = Decimal(amount)
        else:
            amount = Decimal(amount.replace(".", "").replace(",", "."))

        return Transaction(
            datetime.datetime.strptime(
                self.get_value(sheet, row_idx, self.config.DATE), self.config.DATE_FMT
            ).strftime("%Y-%m-%d"),
            self.get_description(sheet, row_idx),
            amount,
            self.get_value(sheet, row_idx, self.config.CURRENCY)
            if self.config.CURRENCY
            else "EUR",
            self.config.SRC_NAME,
            self.get_category(sheet, row_idx),
        )


class XLSParser(Parser):
    def open(self, filename):
        workbook = xlrd.open_workbook(filename)
        return workbook.sheet_by_index(0)

    def num_rows(self, sheet):
        return sheet.nrows

    def get_value(self, sheet, row_idx, col_idx):
        return sheet.row_slice(rowx=row_idx)[col_idx].value


class CSVParser(Parser):
    def open(self, filename):
        with open(filename, encoding="windows-1250") as file:
            return file.readlines()

    def num_rows(self, sheet):
        return len(sheet)

    def get_value(self, sheet, row_idx, col_idx):
        return sheet[row_idx].split(self.config.DELIMITER)[col_idx]
