from .parsers import XLSParser, CSVParser, BankinterConfig, PersonalConfig, VisaConfig, BusinessConfig

bankinter_parser = XLSParser(BankinterConfig)
personal_parser = XLSParser(PersonalConfig)
visa_parser = XLSParser(VisaConfig)
business_parser = CSVParser(BusinessConfig)

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
    
    str_output = "Date,Amount,Currency,Description,Category\n"
    sum = 0

    for a in sorted(results):
        str_output += a.csv()
        sum += a.amount

    for category in (
        "Taxes",
        "Bank",
        "Groceries",
        "Restaurants",
        "Travel",
        "Home & Utilities",
        "SP Expenses",
        "Apartment",
        "Car",
        "Clothing & Footwear",
        "Health & Personal Care",
        "Surf",
        "Gifts",
        "Education",
        "Loans",
        "Charity",
        str(sum)
    ):
        str_output += ",,,," + category + "\n"

    print(str_output)
    
