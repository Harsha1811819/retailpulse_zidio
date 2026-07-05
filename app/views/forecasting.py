import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# LOAD REAL FORECAST DATA
# ============================================================

@st.cache_data
def load_forecast():

    base_dir = Path(__file__).resolve().parents[2]
    data_path = base_dir / "Data" / "hybrid_forecast.csv"

    if not data_path.exists():
        st.error(f"Forecast file not found:\n{data_path}")
        st.stop()

    df = pd.read_csv(data_path)

    df["ds"] = pd.to_datetime(df["ds"])

    return df


# ============================================================
# PAGE
# ============================================================

def render():

    st.title("📈 Demand Forecasting")
    st.caption("Hybrid Forecast using Prophet + LSTM")

    df = load_forecast()

    # ========================================================
    # KPI STRIP
    # ========================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Forecast",
        f"{df['HybridForecast'].mean():.2f}"
    )

    col2.metric(
        "Maximum Forecast",
        f"{df['HybridForecast'].max():.2f}"
    )

    prophet_vs_hybrid = (
        (abs(df["HybridForecast"] - df["yhat"])).mean()
    )

    col3.metric(
        "Avg Prophet ↔ Hybrid Difference",
        f"{prophet_vs_hybrid:.2f}"
    )

    st.divider()

    # ========================================================
    # MODEL SELECTION
    # ========================================================

    model_options = {
        "Prophet": "yhat",
        "LSTM": "LSTM",
        "Hybrid": "HybridForecast"
    }

    selected = st.multiselect(
        "Select Models",
        list(model_options.keys()),
        default=["Prophet", "LSTM", "Hybrid"]
    )

    if not selected:
        st.warning("Please select at least one model.")
        return

    plot_df = pd.DataFrame({
        "Date": df["ds"]
    })

    for model in selected:
        plot_df[model] = df[model_options[model]]

    melted = plot_df.melt(
        id_vars="Date",
        var_name="Model",
        value_name="Forecast"
    )

    fig = px.line(
        melted,
        x="Date",
        y="Forecast",
        color="Model",
        markers=True,
        title="Hybrid Demand Forecast"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ========================================================
    # DATA TABLE
    # ========================================================

    st.subheader("Forecast Data")

    st.dataframe(
        df[
            [
                "ds",
                "yhat",
                "LSTM",
                "HybridForecast"
            ]
        ].rename(
            columns={
                "ds": "Date",
                "yhat": "Prophet"
            }
        ),
        use_container_width=True
    )