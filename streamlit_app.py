import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="The Bitter Brew Radar ☕", layout="wide")

# Fixed CSS: Enforces readable dark mocha text across both Light and Dark modes
st.markdown("""
    <style>
    /* Force main app background */
    .stApp {
        background-color: #FAF6F0 !important;
    }
    
    /* Force main area text to be dark mocha */
    .stApp, .stApp p, .stApp span, .stApp label, h1, h2, h3, h4, h5, h6 {
        color: #3A2E2B !important;
        font-family: 'Georgia', serif;
    }

    /* Style the Sidebar */
    [data-testid="stSidebar"] {
        background-color: #2C221E !important;
    }
    [data-testid="stSidebar"] * {
        color: #F5EBE6 !important;
    }

    /* Custom Card Containers */
    .cafe-card {
        background-color: #FFFFFF !important;
        border: 2px solid #E8DFD8 !important;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.03);
    }
    
    /* Warning Box */
    .warning-note {
        background-color: #FFF3CD !important;
        border-left: 5px solid #FFC107 !important;
        padding: 12px 16px;
        border-radius: 8px;
        color: #664D03 !important;
        font-size: 14px;
        margin-top: 10px;
    }
    
    /* Code tag styling for numbers */
    .stat-badge {
        background-color: #EFE8E1 !important;
        color: #4A3B32 !important;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
        font-family: monospace;
    }
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
st.sidebar.title("☕ Brew Control Panel")
st.sidebar.write("Filter out overvalued / high-risk stocks.")

max_z = st.sidebar.slider("Max Altman Z-Score (Distress < 1.81)", 1.0, 3.5, 1.81, 0.05)
min_snoa = st.sidebar.slider("Min SNOA Growth % (Asset Bloat)", 0.0, 30.0, 15.0, 1.0)

# Filter Logic
filtered_df = df[(df['Altman_Z'] <= max_z) & (df['SNOA_Growth_%'] >= min_snoa)]

# Main Display Title
st.title("☕ The Bitter Brew Radar")
st.markdown("### *Overvalued & High-Risk Accounting Screener*")
st.write("Identifies red flags, aggressive accruals, and balance sheet distress.")
st.write("---")

# Display Filtered Companies inside custom Cards
if filtered_df.empty:
    st.info("No companies match your bitter brew criteria! Try adjusting the sidebar sliders.")
else:
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div class="cafe-card">
            <h3>🚨 {row['Ticker']} — {row['Company Name']}</h3>
            <p><b>Altman Z-Score:</b> <span class="stat-badge">{row['Altman_Z']}</span> <i>(Distress Zone &lt; 1.81)</i></p>
            <p><b>SNOA Growth:</b> <span class="stat-badge">{row['SNOA_Growth_%']}%</span> <i>(Bloated Operating Assets)</i></p>
            <p><b>Cash Flow Gap:</b> <span class="stat-badge">${row['Cash_Earnings_Gap_$M']}M</span> <i>(Earnings exceed operating cash)</i></p>
            <div class="warning-note">
                ☕ <b>Tasting Note:</b> High overvaluation risk! Reported earnings rely heavily on accounting accruals while actual cash flow lags behind.
            </div>
        </div>
        """, unsafe_allow_html=True)
