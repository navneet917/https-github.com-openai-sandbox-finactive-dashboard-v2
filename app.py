# Finactive Empower-Style Dashboard MVP

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Finactive Dashboard")
st.image("https://via.placeholder.com/150x50?text=Finactive", width=150)
st.title("💼 Finactive – Personal Financial Wellness Dashboard")

# Dummy client dataset
clients = {
    "John Doe": {
        "income": 1200000,
        "expenses": 800000,
        "assets": {
            "Cash": 100000,
            "FDs": 300000,
            "Equity": 400000,
            "MFs": 300000,
            "Real Estate": 1200000,
            "EPF": 250000
        },
        "liabilities": {
            "Home Loan": 800000,
            "Car Loan": 200000
        },
        "portfolio": {
            "Equity": 400000,
            "MF": 300000
        },
        "emergency_fund": 100000
    },
    "Anita Sharma": {
        "income": 900000,
        "expenses": 500000,
        "assets": {
            "Cash": 50000,
            "FDs": 200000,
            "Equity": 250000,
            "MFs": 200000,
            "Real Estate": 900000,
            "EPF": 150000
        },
        "liabilities": {
            "Home Loan": 400000
        },
        "portfolio": {
            "Equity": 250000,
            "MF": 200000
        },
        "emergency_fund": 80000
    }
}

client_names = list(clients.keys())
selected_client = st.sidebar.selectbox("🔍 Select Client", client_names)
data = clients[selected_client]

# --- Calculations ---
net_worth = sum(data['assets'].values()) - sum(data['liabilities'].values())
savings_rate = 1 - data['expenses'] / data['income']
debt_ratio = sum(data['liabilities'].values()) / data['income']
emergency_months = data['emergency_fund'] / (data['expenses'] / 12)

scores = {
    "Investment Score": int(min(100, (sum(data['portfolio'].values()) / data['income']) * 100)),
    "Debt Score": int(max(0, 100 - (debt_ratio * 100))),
    "Budgeting Score": int(savings_rate * 100),
    "Emergency Fund Score": int(min(100, emergency_months / 6 * 100))
}

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Net Worth Overview")
    st.metric("Net Worth", f"Rs {net_worth:,}")
    st.write("### Asset Allocation")
    asset_df = pd.DataFrame.from_dict(data['assets'], orient='index', columns=['Value'])
    st.bar_chart(asset_df)

    st.write("### Liabilities")
    liability_df = pd.DataFrame.from_dict(data['liabilities'], orient='index', columns=['Outstanding'])
    st.bar_chart(liability_df)

with col2:
    st.subheader("💹 Portfolio Distribution")
    port_df = pd.Series(data['portfolio'])
    fig1, ax1 = plt.subplots()
    ax1.pie(port_df, labels=port_df.index, autopct='%1.1f%%')
    ax1.axis('equal')
    st.pyplot(fig1)

    st.subheader("📈 Financial Health Scores")
    for label, score in scores.items():
        st.metric(label, f"{score}/100")
        st.progress(score / 100)

# --- Recommendations ---
st.subheader("🧠 Recommendations")
if savings_rate < 0.2:
    st.warning("Increase your savings rate. Current rate is below 20%.")
if emergency_months < 6:
    st.info("Emergency fund should cover at least 6 months of expenses.")
if debt_ratio > 0.4:
    st.error("Debt ratio is high. Consider reducing liabilities.")
if scores['Investment Score'] < 60:
    st.info("Consider increasing your long-term investments to build wealth.")
