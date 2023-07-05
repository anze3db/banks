import glob
import os

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

path = os.getcwd()


def parse_csvs():
    csv_files = glob.glob(os.path.join("/Users/anze/Documents/banks/learn", "*.csv"))
    return (pd.read_csv(f, sep=";") for f in sorted(csv_files))


def expan_df(df):
    df[[f"descr_{i}" for i in range(11)]] = df["Description"].str.split(
        r" |\-|\n|\.", expand=True, regex=True, n=10
    )
    df[[f"date_{i}" for i in range(3)]] = df["Date"].str.split("-", expand=True)
    return df


my_csv = expan_df(pd.read_csv("./2022-05.csv", sep=","))
my_cats = my_csv.pop("Category")
df = expan_df(pd.concat(parse_csvs()))
df_categories = df.pop("Category")
# print(df)

enc = preprocessing.OrdinalEncoder()
enc.fit(pd.concat([df, my_csv]))
# print(enc.categories_)
X = enc.transform(df)
myX = enc.transform(my_csv)
np.set_printoptions(threshold=np.inf)
# print(np.raveldf[["Category"]].to_numpy())

le = preprocessing.LabelEncoder()
y = le.fit_transform(np.ravel(df_categories))
from sklearn.datasets import make_circles, make_classification, make_moons
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

model = RandomForestClassifier(max_depth=500, n_estimators=1000, max_features=1)
model.fit(X, y)
y_pred = model.predict(myX)
y_pred_stats = model.predict_proba(myX)
revers = le.inverse_transform(y_pred)
my_csv["Predictions"] = revers
confidence = [max(x) for x in y_pred_stats]
my_csv["Confidence"] = confidence
pd.set_option("display.max_rows", None)
my_csv["Category"] = my_cats

with open("2022-05-cov.csv", "w") as f:
    my_csv[
        [
            "Date",
            "Currency",
            "Description",
            "Source",
            "Category",
            "Predictions",
            "Confidence",
        ]
    ].to_csv(f, sep=";")
# for prd in r?ee:
#     print(prd, )


# Splitting train : test to 80 : 20 ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    # GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=50),
    RandomForestClassifier(max_depth=50, n_estimators=100, max_features=1),
    MLPClassifier(alpha=1, max_iter=10000),
    AdaBoostClassifier(),
    GaussianNB(),
    # QuadraticDiscriminantAnalysis(),
]

for classifier in classifiers:
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    # print(
    #     [
    #         (a, b)
    #         for a, b in zip(le.inverse_transform(y_pred), le.inverse_transform(y_test))
    #         if a != b
    #     ],
    # )
    accuracy = accuracy_score(y_test, y_pred)
    print(classifier, "Accuracy", accuracy)
    classifier.predict(myX)
