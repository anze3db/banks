from datetime import datetime
import glob
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier


with open('/Users/anze/Documents/banks/learn/all.csv') as f:
    df = pd.read_csv(f, sep=";")

# def parse(cur):
#     date = datetime.strptime(cur, '%m/%d/%y')
#     return date.strftime('%Y-%m-%d')
#
# df['Date'] = df['Date'].apply(parse)
df['Amount'] = df['Amount'].apply(lambda x: "-" + x)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
pd.set_option("display.max_rows", None)
print(df.to_csv(sep=';', index=False))
# def run(args):
#     def parse_csvs():
#         csv_files = glob.glob(os.path.join(args.learn, "*.csv"))
#         return (pd.read_csv(f, sep=";") for f in sorted(csv_files))
#
#     def expan_df(df):
#         df[[f"descr_{i}" for i in range(11)]] = df["Description"].str.split(
#             r" |\-|\n|\.", expand=True, regex=True, n=10
#         )
#         df[[f"date_{i}" for i in range(3)]] = df["Date"].str.split("-", expand=True)
#         df.fillna("", inplace=True)
#         df.drop(columns=['Predictions', 'Confidence'], errors='ignore')
#         df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#         return df
#
#     my_csv = expan_df(pd.read_csv(args.file, sep=","))
#
#     df = expan_df(pd.concat(parse_csvs()))
#
#     enc = preprocessing.OrdinalEncoder()
#     enc.fit(pd.concat([df, my_csv]))
#     X = enc.transform(df)
#     print(my_csv)
#     myX = enc.transform(my_csv)
#     # print(np.raveldf[["Category"]].to_numpy())
#
#     le = preprocessing.LabelEncoder()
#     y = le.fit_transform(np.ravel(df[["Category"]]))
#     model = RandomForestClassifier(max_depth=50, n_estimators=100, max_features=1)
#     model.fit(X, y)
#
#     y_pred = model.predict(myX)
#     y_pred_stats = model.predict_proba(myX)
#     revers = le.inverse_transform(y_pred)
#     my_csv["Predictions"] = revers
#     confidence = [max(x) for x in y_pred_stats]
#     my_csv["Confidence"] = confidence
#     categories = [
#         "Apartment",
#         "Bank",
#         "Bike",
#         "Books",
#         "Car",
#         "Cash",
#         "CatX",
#         "Charity",
#         "Clothing",
#         "Dog",
#         "Education",
#         "Electronics",
#         "Expenses",
#         "Food & Drinks",
#         "Fun",
#         "Games",
#         "Gifts",
#         "Groceries",
#         "Health",
#         "Household",
#         "Investments",
#         "Leisure",
#         "Other",
#         "Placa",
#         "Restaurants",
#         "Shopping",
#         "SP"
#         "Sports",
#         "Surf",
#         "Taxes",
#         "Transport",
#         "Travel",
#         "Unknown",
#     ]
#     for cat in categories:
#         my_csv = my_csv.append(dict(Category=cat), ignore_index=True)
#     pd.set_option("display.max_rows", None)
#     print(
#         my_csv.to_csv(
#             columns=[
#                 "Date",
#                 "Amount",
#                 "Currency",
#                 "Description",
#                 "Source",
#                 "Category",
#                 "Predictions",
#                 "Confidence",
#             ]
#         )
#     )