import glob
import os

# import numpy as np
# import pandas as pd
# from sklearn import preprocessing
# from sklearn.ensemble import RandomForestClassifier


def run(args):
    def parse_csvs():
        csv_files = glob.glob(os.path.join(args.learn, "*.csv"))
        return (pd.read_csv(f, sep=";") for f in sorted(csv_files))

    def expan_df(df):
        # df[[f"descr_{i}" for i in range(11)]] = df["Description"].str.split(
        #     r" |\-|\n|\.", expand=True, regex=True, n=10
        # )
        # df[[f"date_{i}" for i in range(3)]] = df["Date"].str.split("-", expand=True)
        df["Amount"] = df["Amount"].apply(lambda x: float(str(x).replace(",", "")))
        df["Description"] = df["Description"].apply(lambda x: str(x) if x else None)
        df["Source"] = df["Source"].apply(lambda x: str(x))
        df["Category"] = df["Category"].apply(lambda x: str(x) if x else None)
        df.drop(columns=["Predictions", "Confidence"], errors="ignore")
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        # df.fillna("", inplace=True)
        return df

    # pd.set_option("display.max_rows", None)
    # pd.set_option("display.max_columns", None)
    my_csv = expan_df(pd.read_csv(args.file, sep=","))

    df = expan_df(pd.concat(parse_csvs()))
    # print(df)`
    # print(my_csv)`
    enc = preprocessing.OrdinalEncoder()
    enc.fit(pd.concat([df, my_csv]))
    X = enc.transform(df)
    # print(df)
    # print(my_csv)

    myX = enc.transform(my_csv)
    # print(np.raveldf[["Category"]].to_numpy())

    le = preprocessing.LabelEncoder()
    y = le.fit_transform(np.ravel(df[["Category"]]))
    model = RandomForestClassifier(max_depth=50, n_estimators=100, max_features=1)
    model.fit(X, y)

    y_pred = model.predict(myX)
    y_pred_stats = model.predict_proba(myX)
    revers = le.inverse_transform(y_pred)
    my_csv["Predictions"] = revers
    confidence = [max(x) for x in y_pred_stats]
    my_csv["Confidence"] = confidence
    categories = [
        "Apartment",
        "Bank",
        "Bike",
        "Books",
        "Car",
        "Cash",
        "CatX",
        "Charity",
        "Clothing",
        "Dog",
        "Education",
        "Electronics",
        "Expenses",
        "Food & Drinks",
        "Fun",
        "Games",
        "Gifts",
        "Groceries",
        "Health",
        "Household",
        "Investments",
        "Leisure",
        "Other",
        "Placa",
        "Restaurants",
        "Shopping",
        "SP Expenses",
        "Sports",
        "Surf",
        "Taxes",
        "Transport",
        "Travel",
        "Unknown",
    ]
    df_categories = pd.DataFrame.from_records([{"Category": cat for cat in categories}])
    my_csv = pd.concat([my_csv, df_categories], ignore_index=True)
    print(
        my_csv.to_csv(
            columns=[
                "Date",
                "Amount",
                "Currency",
                "Description",
                "Source",
                "Category",
                "Predictions",
                "Confidence",
            ],
            sep=";",
            index=False,
        )
    )
