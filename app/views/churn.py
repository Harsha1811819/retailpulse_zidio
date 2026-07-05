import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import joblib
# from pathlib import Path

# ============================================================
# LOAD REAL CHURN PREDICTIONS
# ============================================================


@st.cache_data
def load_churn():

    base_dir = Path(__file__).resolve().parents[2]

    customer_path = base_dir / "Data" / "customers_unique_summary.csv"
    model_path = base_dir / "models" / "churn_xgboost.pkl"

    if not customer_path.exists():
        st.error(f"Missing file:\n{customer_path}")
        st.stop()

    if not model_path.exists():
        st.error(f"Missing file:\n{model_path}")
        st.stop()

    df = pd.read_csv(customer_path)

    model = joblib.load(model_path)

    X = df[
        [
            "Recency",
            "Frequency",
            "Monetary"
        ]
    ]

    df["Prediction"] = model.predict(X)

    df["Probability"] = model.predict_proba(X)[:, 1]

    return df


# ============================================================
# PAGE
# ============================================================

def render():

    st.title("⚠️ Churn Risk Dashboard")
    st.caption("XGBoost-based churn prediction")

    df = load_churn()

    # ========================================================
    # KPIs
    # ========================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Customers",
        len(df)
    )

    c2.metric(
        "Average Churn Probability",
        f"{df['Probability'].mean():.2%}"
    )

    c3.metric(
    "Model",
    "XGBoost"
    )

    st.divider()

    # ========================================================
    # TOP N
    # ========================================================

    top_n = st.slider(
        "Top At-Risk Customers",
        5,
        min(50, len(df)),
        10
    )

    risk_df = (
        df.sort_values(
            "Probability",
            ascending=False
        )
        .head(top_n)
    )

    # ========================================================
    # TABLE
    # ========================================================

    st.subheader("🚨 High-Risk Customers")

    st.dataframe(
        risk_df[
            [
                "CustomerID",
                "CustomerSegment",
                "Recency",
                "Frequency",
                "Monetary",
                "Probability"
            ]
        ],
        use_container_width=True
    )

    # ========================================================
    # BAR CHART
    # ========================================================

    st.subheader("📊 Churn Probability")

    fig = px.bar(
        risk_df,
        x="CustomerID",
        y="Probability",
        color="Probability",
        hover_data=[
            "CustomerSegment",
            "Recency",
            "Frequency",
            "Monetary"
        ],
        title="Top At-Risk Customers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    high_risk = len(
        df[df["Probability"] >= 0.50]
    )

    st.success(
        f"{high_risk} customers currently have a churn probability of 50% or higher."
    )