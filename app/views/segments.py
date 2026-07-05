import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# LOAD CUSTOMER SUMMARY
# ============================================================

@st.cache_data
def load_segments():

    base_dir = Path(__file__).resolve().parents[2]
    data_path = base_dir / "Data" / "customers_unique_summary.csv"

    if not data_path.exists():
        st.error(f"File not found:\n{data_path}")
        st.stop()

    df = pd.read_csv(data_path, low_memory=False)

    return df


# ============================================================
# PAGE
# ============================================================

def render():

    st.title("👥 Customer Segmentation")
    st.caption("RFM Based Customer Segmentation")

    df = load_segments()

    # --------------------------------------------------------
    # Keep only required columns
    # --------------------------------------------------------

    customer_df = df[
        [
            "CustomerID",
            "CustomerSegment",
            "Recency",
            "Frequency",
            "Monetary",
        ]
    ].copy()

    # --------------------------------------------------------
    # Filter
    # --------------------------------------------------------

    segments = sorted(customer_df["CustomerSegment"].unique())

    selected = st.multiselect(
        "Select Customer Segments",
        segments,
        default=segments,
    )

    customer_df = customer_df[
        customer_df["CustomerSegment"].isin(selected)
    ]

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Customers",
        len(customer_df)
    )

    c2.metric(
        "Customer Segments",
        customer_df["CustomerSegment"].nunique()
    )

    c3.metric(
        "Average Monetary Value",
        f"${customer_df['Monetary'].mean():,.2f}"
    )

    st.divider()

    # --------------------------------------------------------
    # Segment Distribution
    # --------------------------------------------------------

    st.subheader("📊 Customer Distribution")

    segment_counts = (
        customer_df["CustomerSegment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Customer Segment",
        "Customers"
    ]

    fig = px.bar(
        segment_counts,
        x="Customer Segment",
        y="Customers",
        color="Customer Segment",
        text="Customers",
        title="Customers per Segment"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # Average Monetary
    # --------------------------------------------------------

    st.subheader("💰 Average Monetary Value")

    monetary = (
        customer_df.groupby("CustomerSegment")["Monetary"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        monetary,
        x="CustomerSegment",
        y="Monetary",
        color="CustomerSegment",
        text_auto=".2f",
        title="Average Spend by Segment"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # Average Recency
    # --------------------------------------------------------

    st.subheader("📅 Average Recency")

    recency = (
        customer_df.groupby("CustomerSegment")["Recency"]
        .mean()
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        recency,
        x="CustomerSegment",
        y="Recency",
        color="CustomerSegment",
        text_auto=".2f",
        title="Average Days Since Last Purchase"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # Summary Table
    # --------------------------------------------------------

    st.subheader("📋 Segment Summary")

    summary = (
        customer_df.groupby("CustomerSegment")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean"),
        )
        .round(2)
        .reset_index()
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # Customer Details
    # --------------------------------------------------------

    st.subheader("👤 Customer Details")

    st.dataframe(
        customer_df,
        use_container_width=True,
        hide_index=True,
    )