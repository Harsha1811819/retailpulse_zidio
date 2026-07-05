import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# LOAD INVENTORY RECOMMENDATIONS
# ============================================================

@st.cache_data
def load_inventory():

    base_dir = Path(__file__).resolve().parents[2]
    data_path = base_dir / "Data" / "inventory_recommendation.csv"

    if not data_path.exists():
        st.error(f"File not found:\n{data_path}")
        st.stop()

    df = pd.read_csv(data_path)

    return df


# ============================================================
# PAGE
# ============================================================

def render():

    st.title("📦 Inventory Optimizer")
    st.caption("AI-driven reorder recommendations")

    df = load_inventory()

    # ========================================================
    # KPIs
    # ========================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Products Monitored",
        len(df)
    )

    c2.metric(
        "Products Requiring Reorder",
        (df["Status"] == "Reorder Required").sum()
    )

    c3.metric(
        "Total Recommended Order",
        f"{df['RecommendedOrder'].sum()} Units"
    )

    st.divider()

    # ========================================================
    # STOCK COMPARISON
    # ========================================================

    st.subheader("📊 Stock Levels")

    plot_df = df.melt(
        id_vars="StockCode",
        value_vars=[
            "CurrentStock",
            "PredictedDemand",
            "SafetyStock"
        ],
        var_name="Metric",
        value_name="Units"
    )

    fig = px.bar(
        plot_df,
        x="StockCode",
        y="Units",
        color="Metric",
        barmode="group",
        title="Current Stock vs Predicted Demand vs Safety Stock"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ========================================================
    # RECOMMENDATION TABLE
    # ========================================================

    st.subheader("📋 Inventory Recommendations")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # REORDER CHART
    # ========================================================

    reorder_df = df[df["RecommendedOrder"] > 0]

    if not reorder_df.empty:

        st.subheader("📦 Recommended Order Quantity")

        fig = px.bar(
            reorder_df,
            x="StockCode",
            y="RecommendedOrder",
            color="Status",
            text="RecommendedOrder",
            title="Products Requiring Reorder"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    total = df["RecommendedOrder"].sum()

    st.success(
        f"Total recommended replenishment across all monitored products: {total} units."
    )