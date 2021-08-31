from .parsers import (
    XLSParser,
    CSVParser,
    BankinterConfig,
    PersonalConfig,
    VisaConfig,
    BusinessConfig,
    N26Config,
)

bankinter_parser = XLSParser(BankinterConfig)
personal_parser = XLSParser(PersonalConfig)
visa_parser = XLSParser(VisaConfig)
business_parser = CSVParser(BusinessConfig)
n26_parser = CSVParser(N26Config)


def run(args):
    results = []
    for file in args.bankinter:
        results += bankinter_parser.parse(file)
    for file in args.personal:
        results += personal_parser.parse(file)
    for file in args.visa:
        results += visa_parser.parse(file)
    for file in args.business:
        results += business_parser.parse(file)
    for file in args.n26:
        results += n26_parser.parse(file)

    str_output = "Date,Amount,Currency,Description,Source,Category\n"

    for a in sorted(results):
        str_output += a.csv()

    for category in (
        "Apartment",
        "Bank",
        "Bike",
        "Transport & Car",
        "Charity",
        "Clothing & Footwear",
        "Dog",
        "Education",
        "Gadgets",
        "Games",
        "Gifts",
        "Food & Groceries",
        "Health & Personal Care",
        "Household & Utilities",
        "Investments",
        "Loans",
        "Bars & Restaurants",
        "SP Expenses",
        "Surf",
        "Taxes",
        "Travel & Holidays",
    ):
        str_output += ",,,,," + category + "\n"

    print(str_output)
