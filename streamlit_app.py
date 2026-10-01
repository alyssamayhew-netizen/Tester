import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="The Bitter Brew Radar ☕", layout="wide")

# Custom Café Styling
st.markdown("""
    <style>
    .stApp { background-color: #FAF6F0; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 2px solid #E8DFD8;
        padding: 16px;
        border-radius: 14px;
    }
    h1, h2, h3 { color: #4A3B32; font-family: 'Georgia', serif; }
    </style>
""", unsafe_allow_html=True)

# Sample Financial Data
data = {
    'Ticker': ['ROAST', 'BEANS', 'SIP', 'DRIP', 'MOCHA', 'LATTE'],
    'Company Name': ['Roast Corp', 'Beans Co', 'Sip Analytics', 'Drip Retail', 'Mocha Tech', 'Latte Goods'],
    'Altman_Z': [1.25, 1.65, 3.10, 1.40, 2.80, 1.10],
    'SNOA_Growth_%': [22.4, 18.1, 4.2, 19.5, 6.1, 28.0],
    'Cash_Earnings_Gap_$M': [14.2, 8.5, -2.1, 11.0, -1.0, 18.3]
}
df = pd.DataFrame(data)

# Sidebar Controls
st.sidebar.header("☕ Brew Control Panel")
max_z = st.sidebar.slider("Max Altman Z-Score (Distress < 1.81)", 1.0, 3.5, 1.81, 0.05)
min_snoa = st.sidebar.slider("Min SNOA Growth % (Asset Bloat)", 0.0, 30.0, 15.0, 1.0)

# Filter Logic
filtered_df = df[(df['Altman_Z'] <= max_z) & (df['SNOA_Growth_%'] >= min_snoa)]

# Main Display
st.title("☕ The Bitter Brew Radar: Overvalued Screening")
st.write("---")

for _, row in filtered_df.iterrows():
    with st.expander(f"🚨 {row['Ticker']} - {row['Company Name']} (Altman Z: {row['Altman_Z']})"):
        st.write(f"**Altman Z-Score:** `{row['Altman_Z']}` *(Distress Zone)*")
        st.write(f"**SNOA Growth:** `{row['SNOA_Growth_%']}%` *(Bloated Assets)*")
        st.warning("☕ **Tasting Note:** High overvaluation risk! Reported earnings rely heavily on accruals while cash generation lags behind.")
