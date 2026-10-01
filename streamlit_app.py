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
# 2. Complete Café Theme Styling (Bulletproof Sidebar Fix)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #FAF4EE !important;
    }
    
    /* Main Content Typography */
    .stApp p, .stApp span, .stApp label, h1, h2, h3, h4, h5, h6 {
        color: #3A2E2B !important;
        font-family: 'Georgia', serif;
    }

    /* -------------------------------------------------- */
    /* SIDEBAR DIRECT TARGETING                           */
    /* -------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #2C221E !important;
    }
    
    /* Force ALL text inside sidebar (headers, labels, markdown) to bright cream */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebarHeader"] {
        color: #FAF4EE !important;
    }

    /* SLIDER TRACK FIX: Light background bar across full width */
    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div {
        background-color: #5C4A42 !important;
        height: 6px !important;
        border-radius: 3px !important;
    }

    /* SLIDER FILLED TRACK: Caramel active bar */
    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div {
        background-color: #C49A6C !important;
        height: 6px !important;
    }

    /* SLIDER THUMB BUTTON: Round cream knob */
    [data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
        background-color: #FAF4EE !important;
        border: 2px solid #C49A6C !important;
        height: 18px !important;
        width: 18px !important;
    }

    /* SIDEBAR BUTTON: Warm caramel with dark mocha text */
    [data-testid="stSidebar"] button {
        background-color: #C49A6C !important;
        border: 2px solid #A87E52 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
    }

    [data-testid="stSidebar"] button p, 
    [data-testid="stSidebar"] button span {
        color: #2C221E !important;
        font-weight: bold !important;
    }

    /* -------------------------------------------------- */
    /* CARDS & BADGES                                     */
    /* -------------------------------------------------- */
    .cafe-card {
        background-color: #F3ECE4 !important;
        border: 2px solid #E3D7CB !important;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 18px;
        box-shadow: 0px 4px 12px rgba(58, 46, 43, 0.04);
    }

    .warning-note {
        background-color: #EBD8C1 !important;
        border-left: 5px solid #C49A6C !important;
        padding: 12px 16px;
        border-radius: 10px;
        color: #3A2E2B !important;
        font-size: 14px;
        margin-top: 12px;
    }
    
    .stat-badge {
        background-color: #E3D7CB !important;
        color: #2C221E !important;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
        font-family: monospace;
    }

    .welcome-card {
        background-color: #F3ECE4 !important;
        border: 2px solid #E3D7CB !important;
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        max-width: 700px;
        margin: 40px auto;
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
            <p style="font-size: 18px; color: #6E5A53 !important;">
                Welcome to the Financial Accounting Analysis Café!
            </p>
            <hr style="border: none; border-top: 1px solid #E3D7CB; margin: 20px 0;">
            <p style="font-size: 15px; color: #3A2E2B !important;">
                This application screens publicly traded companies for <b>overvaluation risks</b>, 
                aggressive accrual accounting, and balance sheet distress using formulas like 
                the <b>Altman Z-Score</b>, <b>SNOA Growth</b>, and <b>Cash Flow Gaps</b>.
            </p>
            <p style="font-size: 14px; color: #8C756B !important; margin-top: 15px;">
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

    # Sidebar Controls (Brew Panel)
    st.sidebar.title("☕ Brew Control Panel")
    st.sidebar.write("Set thresholds to screen for overvalued candidate stocks.")

    max_z = st.sidebar.slider("Max Altman Z-Score (Distress < 1.81)", 1.0, 3.5, 1.81, 0.05)
    min_snoa = st.sidebar.slider("Min SNOA Growth % (Asset Bloat)", 0.0, 30.0, 15.0, 1.0)

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
