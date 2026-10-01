import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="The Bitter Brew Radar ☕", layout="wide")

# ---------------------------------------------------------
# 1. Session State & Custom Styling
# ---------------------------------------------------------
if 'entered' not in st.session_state:
    st.session_state.entered = False

def enter_app():
    st.session_state.entered = True

st.markdown("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <style>
    [data-testid="stHeader"] *,
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarExpandButton"] * {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] div {
        color: #FAF4EE !important;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .welcome-card, .cafe-card {
        font-family: 'Georgia', serif !important;
    }

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
# 2. Welcome Screen
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
                Screen publicly traded companies for <b>overvaluation risks</b>, aggressive accruals, 
                and balance sheet distress using financial accounting metrics like the 
                <b>Altman Z-Score</b>, <b>SNOA Growth</b>, and <b>Cash Flow Gaps</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("☕ Enter the Café", on_click=enter_app, use_container_width=True)

# ---------------------------------------------------------
# 3. Main Dashboard View
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

    # Sidebar Controls
    st.sidebar.header("☕ Brew Control Panel")
    st.sidebar.write("Set global risk criteria for the screener.")
    max_z = st.sidebar.slider("Max Altman Z-Score (Distress < 1.81)", 1.0, 3.5, 1.81, 0.05)
    min_snoa = st.sidebar.slider("Min SNOA Growth % (Asset Bloat)", 0.0, 30.0, 15.0, 1.0)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("👈 Back to Welcome Screen"):
        st.session_state.entered = False
        st.rerun()

    # Title
    st.title("☕ The Bitter Brew Radar")

    # --- TAB NAVIGATION ---
    tab1, tab2 = st.tabs(["📊 Screener Radar", "🔍 Single Ticker Deep Dive"])

    # -----------------------------------------------------
    # TAB 1: SCREENER RADAR
    # -----------------------------------------------------
    with tab1:
        st.markdown("### High-Risk Candidates")
        st.write("Companies matching your brew threshold criteria in the control panel.")
        
        # Optional search filter within screener results
        search_term = st.text_input("Filter screener by Ticker or Name", "").strip().upper()
        
        # Filter Logic
        filtered_df = df[(df['Altman_Z'] <= max_z) & (df['SNOA_Growth_%'] >= min_snoa)]
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
                    <h3>🚨 {row['Ticker']} — {row['Company Name']}</h3>
                    <p><b>Altman Z-Score:</b> <span class="stat-badge">{row['Altman_Z']}</span> <i>(Distress Zone &lt; 1.81)</i></p>
                    <p><b>SNOA Growth:</b> <span class="stat-badge">{row['SNOA_Growth_%']}%</span> <i>(Bloated Operating Assets)</i></p>
                    <p><b>Cash Flow Gap:</b> <span class="stat-badge">${row['Cash_Earnings_Gap_$M']}M</span> <i>(Earnings exceed operating cash)</i></p>
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

        # Display Detailed Breakdown Card
        st.markdown(f"""
        <div class="cafe-card">
            <h2>☕ Diagnostic Report: {selected_company['Ticker']} ({selected_company['Company Name']})</h2>
            <hr style="border-top: 1px solid #E3D7CB;">
            <p style="font-size: 16px;"><b>Altman Z-Score:</b> <span class="stat-badge">{selected_company['Altman_Z']}</span></p>
            <p style="font-size: 16px;"><b>SNOA Growth Rate:</b> <span class="stat-badge">{selected_company['SNOA_Growth_%']}%</span></p>
            <p style="font-size: 16px;"><b>Cash vs. Earnings Gap:</b> <span class="stat-badge">${selected_company['Cash_Earnings_Gap_$M']}M</span></p>
            <div class="warning-note">
                <b>Detailed Breakdown:</b> This company shows significant reliance on operating accruals. When operating assets grow faster than revenues, future return on assets often experiences downward pressure.
            </div>
        </div>
        """, unsafe_allow_html=True)
