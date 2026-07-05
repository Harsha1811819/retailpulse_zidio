
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "online_retail_feature_engineered.csv"

MODEL_DIR = BASE_DIR / "airflow" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "churn_xgboost.pkl"

print("="*60)
print("Loading Dataset")
print("="*60)

df = pd.read_csv(DATA_PATH)

print("Dataset Shape :", df.shape)

df["Churn"] = (df["Recency"] > 90).astype(int)

features = [
    "Recency",
    "Frequency",
    "Monetary"
]

X = df[features]
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = XGBClassifier(
    random_state=42,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print(f"Accuracy : {acc:.4f}")

joblib.dump(model, MODEL_PATH)

print("\nModel Saved Successfully")
print(MODEL_PATH)
