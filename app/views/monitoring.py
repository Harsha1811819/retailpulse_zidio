import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# LOAD DRIFT SUMMARY
# ============================================================

@st.cache_data
def load_drift():

    base_dir = Path(__file__).resolve().parents[2]
    data_path = base_dir / "Data" / "drift_summary.csv"

    if not data_path.exists():
        st.error(f"File not found:\n{data_path}")
        st.stop()

    df = pd.read_csv(data_path)

    return df


# ============================================================
# PAGE
# ============================================================

def render():

    st.title("🔬 Model Monitoring")
    st.caption("Feature Drift Monitoring")

    df = load_drift()

    # ========================================================
    # KPIs
    # ========================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Features Monitored",
        len(df)
    )

    drifted = int(df["DriftDetected"].sum())

    c2.metric(
        "Drifted Features",
        drifted
    )

    c3.metric(
        "Pipeline Status",
        "ALERT" if drifted > 0 else "Healthy"
    )

    st.divider()

    # ========================================================
    # BAR CHART
    # ========================================================

    st.subheader("📊 Drift Summary")

    chart_df = (
        df["DriftDetected"]
        .value_counts()
        .rename_axis("Drift")
        .reset_index(name="Count")
    )

    chart_df["Drift"] = chart_df["Drift"].map(
        {
            True: "Drift Detected",
            False: "Stable"
        }
    )

    fig = px.bar(
        chart_df,
        x="Drift",
        y="Count",
        color="Drift",
        text="Count",
        title="Feature Drift Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ========================================================
    # TABLE
    # ========================================================

    st.subheader("📋 Drift Details")

    display_df = df.copy()

    display_df["DriftDetected"] = display_df["DriftDetected"].map(
        {
            True: "Yes",
            False: "No"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    if drifted:

        st.warning(
            f"{drifted} feature(s) show data drift. Consider retraining the model."
        )

    else:

        st.success(
            "No feature drift detected."
        )