import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logging.debug('App started')

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def capm(rf, rm, beta):
    return rf + beta * (rm - rf)

def wacc(equity_value, debt_value, re, rd, tax_rate):
    total_value = equity_value + debt_value
    return (equity_value / total_value) * re + (debt_value / total_value) * rd * (1 - tax_rate)

def future_value(pv, rate, years):
    return pv * (1 + rate) ** years

def npv(rate, cash_flows):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows, 1))

st.set_page_config(page_title="📊 Demo_Finance Models: CAPM, WACC, FV, NPV", layout="wide")

# Navigation sidebar
with st.container():
    st.sidebar.markdown("# Navigation")
    st.sidebar.markdown("[CAPM](#capm)")
    st.sidebar.markdown("[WACC](#wacc)")
    st.sidebar.markdown("[Future Value](#future-value)")
    st.sidebar.markdown("[NPV](#npv)")
    st.sidebar.markdown("[Download Report](#download-report)")

# Title
st.title("📊 Demo_Finance Models")

# Directly adding the "Developed by Semir Alemseged" text in a more professional and balanced size
st.markdown("""
    <p style="font-size:24px; text-align:center; color:#fff; font-weight:bold; background-color:#000; padding:15px; border-radius:10px; margin-top:30px;">
        Developed by Semir Alemseged
    </p>
""", unsafe_allow_html=True)

# Rest of the app layout and calculations
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton > button {
            background-color: #007BFF;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .nav-col {
            background-color: #2c2f38;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            position: fixed;
            top: 0;
            left: 0;
            width: 200px;
        }
        .nav-col a {
            color: white;
            font-size: 18px;
            margin: 15px 0;
            text-decoration: none;
            padding: 10px;
            border-radius: 5px;
        }
        .nav-col a:hover {
            background-color: #007BFF;
        }
        .content {
            margin-left: 220px;
        }
    </style>
    """, unsafe_allow_html=True)

# CAPM Calculation
st.header("CAPM Calculation", anchor="capm")
rf = st.number_input("Risk-Free Rate (%)", min_value=0.0, value=2.0, step=0.1) / 100
rm = st.number_input("Market Return (%)", min_value=0.0, value=8.0, step=0.1) / 100
beta = st.number_input("Beta", min_value=0.0, value=1.2, step=0.1)

if st.button("Calculate CAPM"):
    capm_result = capm(rf, rm, beta)
    st.success(f"Expected Return: {capm_result:.2%}")

    # CAPM Graph
    returns = [capm(rf, rm, b) for b in np.linspace(0, 2, 100)]
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, 2, 100), returns, color='cyan', linewidth=2)
    ax.set_title("CAPM: Expected Return vs Beta")
    ax.set_xlabel("Beta")
    ax.set_ylabel("Expected Return")
    ax.grid(True)
    st.pyplot(fig)

# WACC Calculation
st.header("WACC Calculation", anchor="wacc")
equity_value = st.number_input("Equity Value ($)", min_value=0.0, value=1_000_000.0)
debt_value = st.number_input("Debt Value ($)", min_value=0.0, value=500_000.0)
re = st.number_input("Cost of Equity (%)", min_value=0.0, value=10.0, step=0.1) / 100
rd = st.number_input("Cost of Debt (%)", min_value=0.0, value=5.0, step=0.1) / 100
tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, value=30.0, step=0.1) / 100

if st.button("Calculate WACC"):
    wacc_result = wacc(equity_value, debt_value, re, rd, tax_rate)
    st.success(f"Weighted Average Cost of Capital: {wacc_result:.2%}")
    
    # WACC Pie Chart
    labels = ['Equity', 'Debt']
    sizes = [equity_value, debt_value]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['blue', 'red'], startangle=90)
    ax.set_title("WACC Capital Structure")
    st.pyplot(fig)

# Future Value Calculation
st.header("Future Value Calculation", anchor="future-value")
pv = st.number_input("Present Value ($)", min_value=0.0, value=1000.0)
rate = st.number_input("Rate of Return (%)", min_value=0.0, value=5.0, step=0.1) / 100
years = st.number_input("Number of Years", min_value=1, value=10)

if st.button("Calculate Future Value"):
    fv_result = future_value(pv, rate, years)
    st.success(f"Future Value: ${fv_result:,.2f}")

# NPV Calculation
st.header("Net Present Value (NPV) Calculation", anchor="npv")
discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, value=5.0, step=0.1) / 100
cash_flows = st.text_area("Enter cash flows (comma separated)", "1000, 2000, 3000, 4000, 5000")
cash_flows = [float(x) for x in cash_flows.split(',') if x.strip()]

if st.button("Calculate NPV"):
    npv_result = npv(discount_rate, cash_flows)
    st.success(f"Net Present Value: ${npv_result:,.2f}")

# Download Results
st.header("Download Report", anchor="download-report")
if st.button("Download Report"):
    df = pd.DataFrame({
        'Metric': ['CAPM Expected Return', 'WACC', 'Future Value', 'NPV'],
        'Value': [capm(rf, rm, beta), wacc(equity_value, debt_value, re, rd, tax_rate), future_value(pv, rate, years), npv(discount_rate, cash_flows)]
    })
    df_csv = df.to_csv(index=False)
    st.download_button(label="Download as CSV", data=df_csv, file_name="financial_report.csv", mime="text/csv")
