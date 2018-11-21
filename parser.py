from banks.parsers import personal_parser, visa_parser, bankinter_parser, business_parser

all_results = personal_parser.parse('export_19_11_2018 (1).xls') + \
              visa_parser.parse('export_19_11_2018.xls') + \
              bankinter_parser.parse('ConsultaMovimentos (4).xls') + \
              business_parser.parse('export (1).csv')

summ = 0
str_output = ("Date,Amount,Currency,Description,Category\n")
for a in sorted(all_results):
    str_output += a.csv()
    summ += a.amount
for category in (
    "Taxes",
    "Bank",
    "Food & Drinks",
    "Travel",
    "Home & Utilities",
    "SP Expenses",
    "Apartment",
    "Car",
    "Clothing & Footwear",
    "Health & Personal Care",
    "Surf",
    "Gifts",
    "Leisure",
    "Education",
    "Clothing",
    "Loans",
    "Other",
    "Charity",
    "Sports",
    "Transport"
):
    str_output += ",,,," + category + "\n"
print("Total this month: %.02f" % summ)
with open('out.csv', 'w') as f:
    f.write(str_output)
