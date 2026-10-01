import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="The Bitter Brew Radar ☕", layout="wide")

# ---------------------------------------------------------
# 1. Session State for Welcome Screen
# ---------------------------------------------------------
if 'entered' not in st.session_state:
    st.session_state.entered = False

def enter_app():
    st.session_state.entered = True

# ---------------------------------------------------------
# 2. Styling (Load Material Symbols & Fix Icons Safely)
# ---------------------------------------------------------
st.markdown("""
    <!-- Load Google Material Symbols Font so Streamlit icons render natively -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />

    <style>
    /* Force Streamlit Header & Sidebar icons to use standard icon fonts */
    [data-testid="stHeader"] *,
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarExpandButton"] *,
    [data-testid="stHeader"] span,
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Force all text inside the dark sidebar to bright cream */
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] div {
        color: #FAF4EE !important;
    }

    /* Keep Georgia strictly on main content, headers, and cards */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .welcome-card, .cafe-card {
        font-family: 'Georgia', serif !important;
    }

    /* Card Styling */
    .cafe-card {
        background-color: #F3ECE4;
        border: 2px solid #E3D7CB;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 18px;
        color: #3A2E2B;
    }
    .warning-note {
        background-color: #EBD8C1;
        border-left: 5px solid #C49A6C;
        padding: 12px 16px;
        border-radius: 10px;
        color: #3A2E2B;
        font-size: 14px;
        margin-top: 12px;
    }
    .stat-badge {
        background-color: #E3D7CB;
        color: #2C221E !important;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
        font-family: monospace !important;
    }
    .welcome-card {
        background-color: #F3ECE4;
        border: 2px solid #E3D7CB;
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        max-width: 700px;
        margin: 40px auto;
        color: #3A2E2B;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Welcome / Landing Page View
# ---------------------------------------------------------
if not st.session_state.entered:
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="welcome-card">
            <h1>☕ The Bitter Brew Radar</h1>
            <p style="font-size: 18px; color: #6E5A53;">
                Welcome to the Financial Accounting Analysis Café!
            </p>
            <hr style="border: none; border-top: 1px solid #E3D7CB; margin: 20px 0;">
            <p style="font-size: 15px;">
                This application screens publicly traded companies for <b>overvaluation risks</b>, 
                aggressive accrual accounting, and balance sheet distress using formulas like 
                the <b>Altman Z-Score</b>, <b>SNOA Growth</b>, and <b>Cash Flow Gaps</b>.
            </p>
            <p style="font-size: 14px; color: #8C756B; margin-top: 15px;">
                <i>Adjust your screening criteria in the brew panel to spot high-risk candidates.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("☕ Enter the Café", on_click=enter_app, use_container_width=True)

# ---------------------------------------------------------
# 4. Main Screener Dashboard View
# ---------------------------------------------------------
else:
    # Sample Data
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
    st.sidebar.write("Set thresholds to screen for overvalued candidate stocks.")

    max_z = st.sidebar.slider("Max Altman Z-Score (Distress < 1.81)", 1.0, 3.5, 1.81, 0.05)
    min_snoa = st.sidebar.slider("Min SNOA Growth % (Asset Bloat)", 0.0, 30.0, 15.0, 1.0)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("👈 Back to Welcome Screen"):
        st.session_state.entered = False
        st.rerun()

    # Filter Logic
    filtered_df = df[(df['Altman_Z'] <= max_z) & (df['SNOA_Growth_%'] >= min_snoa)]

    # Main Dashboard Header
    st.title("☕ The Bitter Brew Radar")
    st.markdown("### *Overvalued & High-Risk Accounting Screener*")
    st.write("Identifies red flags, aggressive accruals, and balance sheet distress.")
    st.write("---")

    # Display Cards
    if filtered_df.empty:
        st.info("No companies match your bitter brew criteria! Try adjusting the sliders in the sidebar.")
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
