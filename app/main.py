import sys
import os
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RetailPulse Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛒 RetailPulse")

st.sidebar.caption(
    "AI-Powered Retail Analytics Platform"
)

st.sidebar.markdown("---")

# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "📈 Demand Forecasting",
        "👥 Customer Segments",
        "⚠️ Churn Risk",
        "📦 Inventory Optimizer",
        "🔬 Model Monitoring"
    ]
)

# ============================================================
# OVERVIEW PAGE
# ============================================================

if page.startswith("🏠"):

    st.title("🚀 RetailPulse Dashboard")

    st.subheader(
        "AI-Powered Retail Analytics Platform"
    )

    st.markdown("""
### Platform Features

- 📈 Hybrid Demand Forecasting
- 👥 Customer Segmentation
- ⚠️ Churn Prediction
- 📦 Inventory Optimization
- 🔬 Drift Monitoring
- 🤖 Automated Retraining
- ☁️ Cloud Deployment
""")

    st.divider()

    # ========================================================
    # LOAD PROJECT DATA
    # ========================================================

    base_dir = Path(__file__).resolve().parents[1]

    forecast = pd.read_csv(
        base_dir / "Data" / "hybrid_forecast.csv"
    )

    customers = pd.read_csv(
        base_dir / "Data" / "customers_unique_summary.csv"
    )

    inventory = pd.read_csv(
        base_dir / "Data" / "inventory_recommendation.csv"
    )

    drift = pd.read_csv(
        base_dir / "Data" / "drift_summary.csv"
    )

    # ========================================================
    # KPI STRIP
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Forecast Horizon",
        f"{len(forecast)} Days"
    )

    col2.metric(
        "Customers Analysed",
        f"{len(customers)}"
    )

    col3.metric(
        "Products Requiring Reorder",
        str(
            (
                inventory["Status"] == "Reorder Required"
            ).sum()
        )
    )

    col4.metric(
        "Drifted Features",
        str(
            drift["DriftDetected"].sum()
        )
    )

    st.divider()

    # ========================================================
    # PROJECT SUMMARY
    # ========================================================

    st.subheader("📊 System Overview")

    st.markdown(f"""
RetailPulse is an end-to-end AI-powered retail analytics platform for retail analytics using Machine Learning.

### Modules

- 📈 Demand Forecasting
- 👥 Customer Segmentation
- ⚠️ Churn Prediction
- 📦 Inventory Optimization
- 🔬 Model Monitoring
- 🤖 Automated ML Retraining

---

### Current Pipeline Summary

| Metric | Value |
|--------|------:|
| Forecast Records | **{len(forecast)}** |
| Customers Analysed | **{len(customers)}** |
| Inventory Items | **{len(inventory)}** |
| Products Requiring Reorder | **{(inventory["Status"]=="Reorder Required").sum()}** |
| Drifted Features | **{drift["DriftDetected"].sum()}** |

---

### Tech Stack

- Streamlit
- Prophet
- PyTorch Lightning
- XGBoost
- MLflow
- Evidently AI
- Docker
- Kubernetes
""")

# ============================================================
# FORECASTING PAGE
# ============================================================

elif page.startswith("📈"):

    from app.views import forecasting as p

    p.render()

# ============================================================
# CUSTOMER SEGMENTATION PAGE
# ============================================================

elif page.startswith("👥"):

    from app.views import segments as p

    p.render()

# ============================================================
# CHURN PAGE
# ============================================================

elif page.startswith("⚠️"):

    from app.views import churn as p

    p.render()

# ============================================================
# INVENTORY PAGE
# ============================================================

elif page.startswith("📦"):

    from app.views import inventory as p

    p.render()

# ============================================================
# MODEL MONITORING PAGE
# ============================================================

else:

    from app.views import monitoring as p

    p.render()