import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="The Bitter Brew Radar ☕", layout="wide")

# ---------------------------------------------------------
# 1. Session State Initialization
# ---------------------------------------------------------
if 'entered' not in st.session_state:
    st.session_state.entered = False

if 'max_z' not in st.session_state:
    st.session_state.max_z = 1.81

if 'min_snoa' not in st.session_state:
    st.session_state.min_snoa = 15.0

def enter_app():
    st.session_state.entered = True

# Sync Callbacks for Altman Z
def sync_z_from_slider():
    st.session_state.max_z = st.session_state.max_z_slider

def sync_z_from_input():
    st.session_state.max_z = st.session_state.max_z_input

# Sync Callbacks for SNOA
def sync_snoa_from_slider():
    st.session_state.min_snoa = st.session_state.min_snoa_slider

def sync_snoa_from_input():
    st.session_state.min_snoa = st.session_state.min_snoa_input

# ---------------------------------------------------------
# 2. Custom CSS (Styles & Sidebar Tweaks)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Typography */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .welcome-card, .cafe-card {
        font-family: 'Georgia', serif !important;
    }

    /* Polished Cafe Card Container */
    .cafe-card {
        background: linear-gradient(135deg, #F5EEE6 0%, #EFE5DA 100%);
        border: 1px solid #D8C7B8;
        box-shadow: 0 4px 12px rgba(58, 46, 43, 0.05);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        color: #3A2E2B;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .cafe-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(58, 46, 43, 0.09);
    }

    /* Accent Tasting Note Callout Box */
    .warning-note {
        background-color: #E6D2BC;
        border-left: 4px solid #A87B51;
        padding: 12px 16px;
        border-radius: 8px;
        color: #2C221E;
        font-size: 14px;
        margin-top: 14px;
        line-height: 1.5;
    }

    /* Stat Badges */
    .stat-badge {
        background-color: #D8C7B8;
        color: #2C221E !important;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-family: 'Courier New', monospace !important;
        font-size: 14px;
    }

    /* Welcome / Landing Screen Card */
    .welcome-card {
        background: linear-gradient(135deg, #F5EEE6 0%, #EFE5DA 100%);
        border: 2px solid #D8C7B8;
        box-shadow: 0 8px 24px rgba(58, 46, 43, 0.08);
        padding: 44px;
        border-radius: 24px;
        text-align: center;
        max-width: 720px;
        margin: 40px auto;
        color: #3A2E2B;
    }

    /* --- SIDEBAR CUSTOMIZATION --- */
    
    /* Reduce top padding of the sidebar so title sits higher */
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-top: 1.2rem !important;
    }

    /* Sidebar text colors */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FAF4EE !important;
    }

    /* Make hover tooltip (?) icons bright and clearly visible */
    [data-testid="stSidebar"] [data-testid="stTooltipIcon"] svg {
        fill: #FAF4EE !important;
        color: #FAF4EE !important;
        opacity: 0.95 !important;
    }

    /* Number Input Container Box Sizing */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        height: 32px !important;
        min-height: 32px !important;
        border-radius: 6px !important;
        background-color: #FAF4EE !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="input"] input {
        color: #2C221E !important;
        background-color: transparent !important;
        height: 32px !important;
        padding: 0px 8px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* Hide step arrows on number inputs for a cleaner compact look */
    [data-testid="stSidebar"] button[title="Increase"], 
    [data-testid="stSidebar"] button[title="Decrease"] {
        display: none !important;
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
            <h1 style="margin-bottom: 8px;">☕ The Bitter Brew Radar</h1>
            <p style="font-size: 18px; color: #6E5A53; margin-top: 0;">
                Financial Accounting Analysis Café
            </p>
            <hr style="border: none; border-top: 1px solid #D8C7B8; margin: 24px 0;">
            <p style="font-size: 15px; line-height: 1.6;">
                Screen publicly traded companies for <b>overvaluation risks</b>, aggressive accruals, 
                and balance sheet distress using financial accounting metrics like the 
                <b>Altman Z-Score</b>, <b>SNOA Growth</b>, and <b>Cash Flow Gaps</b>.
            </p>
            <p style="font-size: 14px; color: #7D6B63; margin-top: 18px;">
                <i>Adjust your screening criteria in the brew panel to spot high-risk candidates.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("☕ Enter the Café", on_click=enter_app, use_container_width=True)

# ---------------------------------------------------------
# 4. Main Dashboard View
# ---------------------------------------------------------
else:
    # Sample Dataset
    data = {
        'Ticker': ['ROAST', 'BEANS', 'SIP', 'DRIP', 'MOCHA', 'LATTE'],
        'Company Name': ['Roast Corp', 'Beans Co', 'Sip Analytics', 'Drip Retail', 'Mocha Tech', 'Latte Goods'],
        'Altman_Z': [1.25, 1.65, 3.10, 1.40, 2.80, 1.10],
        'SNOA_Growth_%': [22.4, 18.1, 4.2, 19.5, 6.1, 28.0],
        'Cash_Earnings_Gap_$M': [14.2, 8.5, -2.1, 11.0, -1.0, 18.3]
    }
    df = pd.DataFrame(data)

    # --- SIDEBAR CONTROL PANEL ---
    st.sidebar.markdown(
        "<h2 style='text-align: center; margin-top: 0px; margin-bottom: 8px; font-size: 22px;'>☕ Brew Controls</h2>", 
        unsafe_allow_html=True
    )
    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid #5A4742; margin-top: 0px; margin-bottom: 24px;'>", unsafe_allow_html=True)
    
    # 1. Altman Z-Score Control Row
    z_col1, z_col2 = st.sidebar.columns([0.68, 0.32])
    with z_col1:
        st.slider(
            "Max Altman Z-Score",
            min_value=1.00,
            max_value=3.50,
            value=st.session_state.max_z,
            step=0.05,
            key="max_z_slider",
            on_change=sync_z_from_slider,
            help="Altman Z-Score measures financial distress risk:\n\n• Safe Zone: > 2.99\n• Grey Zone: 1.81 – 2.99\n• Distress Zone: < 1.81 (High Risk)"
        )
    with z_col2:
        st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) # Height spacer
        st.number_input(
            "Max Z Input",
            min_value=1.00,
            max_value=3.50,
            value=st.session_state.max_z,
            step=0.05,
            key="max_z_input",
            on_change=sync_z_from_input,
            label_visibility="collapsed"
        )

    st.sidebar.markdown("<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True)

    # 2. SNOA Growth Control Row
    snoa_col1, snoa_col2 = st.sidebar.columns([0.68, 0.32])
    with snoa_col1:
        st.slider(
            "Min SNOA Growth %",
            min_value=0.0,
            max_value=30.0,
            value=st.session_state.min_snoa,
            step=0.5,
            key="min_snoa_slider",
            on_change=sync_snoa_from_slider,
            help="Scaled Net Operating Assets (SNOA) growth measures asset accumulation relative to revenue:\n\n• Healthy Range: < 10%\n• Caution Zone: 10% – 15%\n• Asset Bloat Zone: > 15% (High Risk)"
        )
    with snoa_col2:
        st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) # Height spacer
        st.number_input(
            "Min SNOA Input",
            min_value=0.0,
            max_value=30.0,
            value=st.session_state.min_snoa,
            step=0.5,
            key="min_snoa_input",
            on_change=sync_snoa_from_input,
            label_visibility="collapsed"
        )

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("👈 Welcome Screen", use_container_width=True):
        st.session_state.entered = False
        st.rerun()

    # Title Header
    st.title("☕ The Bitter Brew Radar")

    # --- TAB NAVIGATION ---
    tab1, tab2 = st.tabs(["📊 Screener Radar", "🔍 Single Ticker Deep Dive"])

    # -----------------------------------------------------
    # TAB 1: SCREENER RADAR
    # -----------------------------------------------------
    with tab1:
        st.markdown("### High-Risk Candidates")
        st.write("Companies matching your brew threshold criteria.")
        
        search_term = st.text_input("Filter screener by Ticker or Name:", "").strip().upper()
        
        filtered_df = df[(df['Altman_Z'] <= st.session_state.max_z) & (df['SNOA_Growth_%'] >= st.session_state.min_snoa)]
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Ticker'].str.contains(search_term) | 
                filtered_df['Company Name'].str.upper().str.contains(search_term)
            ]

        if filtered_df.empty:
            st.info("No companies match the criteria!")
        else:
            for _, row in filtered_df.iterrows():
                st.markdown(f"""
                <div class="cafe-card">
                    <h3 style="margin-top:0;">🚨 {row['Ticker']} — {row['Company Name']}</h3>
                    <p style="margin-bottom: 6px;"><b>Altman Z-Score:</b> <span class="stat-badge">{row['Altman_Z']}</span></p>
                    <p style="margin-bottom: 6px;"><b>SNOA Growth:</b> <span class="stat-badge">{row['SNOA_Growth_%']}%</span></p>
                    <p style="margin-bottom: 6px;"><b>Cash Flow Gap:</b> <span class="stat-badge">${row['Cash_Earnings_Gap_$M']}M</span></p>
                    <div class="warning-note">
                        ☕ <b>Tasting Note:</b> High overvaluation risk! Reported earnings rely heavily on accounting accruals while actual cash flow lags behind.
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # TAB 2: SINGLE TICKER DEEP DIVE
    # -----------------------------------------------------
    with tab2:
        st.markdown("### Individual Accounting Health Check")
        st.write("Lookup any specific company stock symbol to run a direct diagnosis.")

        ticker_query = st.selectbox("Select a Ticker to analyze:", df['Ticker'].unique())
        selected_company = df[df['Ticker'] == ticker_query].iloc[0]

        st.markdown(f"""
        <div class="cafe-card">
            <h2 style="margin-top:0;">☕ Diagnostic Report: {selected_company['Ticker']} ({selected_company['Company Name']})</h2>
            <hr style="border-top: 1px solid #D8C7B8;">
            <p style="font-size: 16px;"><b>Altman Z-Score:</b> <span class="stat-badge">{selected_company['Altman_Z']}</span></p>
            <p style="font-size: 16px;"><b>SNOA Growth Rate:</b> <span class="stat-badge">{selected_company['SNOA_Growth_%']}%</span></p>
            <p style="font-size: 16px;"><b>Cash vs. Earnings Gap:</b> <span class="stat-badge">${selected_company['Cash_Earnings_Gap_$M']}M</span></p>
            <div class="warning-note">
                <b>Detailed Breakdown:</b> This company shows significant reliance on operating accruals. When operating assets grow faster than revenues, future return on assets often experiences downward pressure.
            </div>
        </div>
        """, unsafe_allow_html=True)
