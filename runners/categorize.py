import glob
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier


def run(args):
    def parse_csvs():
        csv_files = glob.glob(os.path.join(args.learn, "*.csv"))
        return (pd.read_csv(f, sep=";") for f in sorted(csv_files))

    def expan_df(df):
        df[[f"descr_{i}" for i in range(11)]] = df["Description"].str.split(
            r" |\-|\n|\.", expand=True, regex=True, n=10
        )
        df[[f"date_{i}" for i in range(3)]] = df["Date"].str.split("-", expand=True)
        df.fillna("", inplace=True)
        return df

    my_csv = expan_df(pd.read_csv(args.file, sep=","))

    df = expan_df(pd.concat(parse_csvs()))

    enc = preprocessing.OrdinalEncoder()
    enc.fit(pd.concat([df, my_csv]))
    X = enc.transform(df)
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
    pd.set_option("display.max_rows", None)
    print(
        my_csv.to_csv(
            columns=[
                "Date",
                "Amount",
                "Description",
                "Source",
                "Category",
                "Predictions",
                "Confidence",
            ]
        )
    )
