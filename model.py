import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load


df = pd.read_csv("/Users/kothakotakarthikreddy/Downloads/ivinfusion_dataset_2000.csv")


if "condition_encoded" not in df.columns:
    le = LabelEncoder()
    df["condition_encoded"] = le.fit_transform(df["condition"])
    dump(le, "condition_encoder.pkl")
else:
    le = LabelEncoder()
    le.fit(df["condition"])


X = df[["age", "weight", "condition_encoded", "iv_volume", "drip_rate"]]
y_reg = df["infusion_time"]
y_clf = df["risk_level"]


reg_model = LinearRegression()
reg_model.fit(X, y_reg)

clf_model = RandomForestClassifier()
clf_model.fit(X, y_clf)

dump(reg_model, "infusion_time_model.pkl")
dump(clf_model, "risk_level_model.pkl")
dump(le, "condition_encoder.pkl")

print("✅ Models trained and saved successfully.")


def predict_infusion_time(age, weight, condition, volume, drip_rate):
    condition_encoded = le.transform([condition])[0]
    X_new = [[age, weight, condition_encoded, volume, drip_rate]]
    return reg_model.predict(X_new)[0]

def classify_flow_rate(age, weight, condition, volume, drip_rate):
    condition_encoded = le.transform([condition])[0]
    X_new = [[age, weight, condition_encoded, volume, drip_rate]]
    return clf_model.predict(X_new)[0]
