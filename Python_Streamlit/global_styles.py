"""
Global Styling Module
License to Live: MIAS - Python/Streamlit Version
Import this at the top of every page to ensure consistent light theme
"""

import streamlit as st

def apply_global_styles():
    """Apply global CSS styling to force light theme on all pages"""
    st.markdown("""
    <style>
        /* ===== GLOBAL APP STYLING ===== */
        
        /* Force white background everywhere */
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        .main .block-container {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        /* Force all text to be black */
        .stApp, .stApp *, 
        h1, h2, h3, h4, h5, h6, 
        p, span, div, label, li, a {
            color: #000000 !important;
        }
        
        /* ===== SIDEBAR STYLING ===== */
        
        /* Lighten the sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #F8F9FA !important;
        }
        
        section[data-testid="stSidebar"] * {
            color: #000000 !important;
        }
        
        /* Sidebar navigation items */
        section[data-testid="stSidebar"] .css-1d391kg,
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"],
        section[data-testid="stSidebar"] .st-emotion-cache-1gwvy71 {
            background-color: #F8F9FA !important;
        }
        
        /* Sidebar links */
        section[data-testid="stSidebar"] a {
            color: #1976D2 !important;
        }
        
        section[data-testid="stSidebar"] a:hover {
            color: #1565C0 !important;
            background-color: #E3F2FD !important;
        }
        
        /* ===== NAVIGATION STYLING ===== */
        
        /* Top navigation bar */
        header[data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }
        
        /* Navigation menu items */
        [data-testid="stSidebarNav"] {
            background-color: #F8F9FA !important;
        }
        
        [data-testid="stSidebarNav"] li {
            background-color: transparent !important;
        }
        
        [data-testid="stSidebarNav"] li:hover {
            background-color: #E3F2FD !important;
        }
        
        /* Selected navigation item */
        [data-testid="stSidebarNav"] li[data-selected="true"] {
            background-color: #BBDEFB !important;
        }
        
        /* ===== TABS STYLING ===== */
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: #F0F2F6 !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #000000 !important;
            background-color: #F0F2F6 !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #E3F2FD !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #1976D2 !important;
            border-bottom: 2px solid #1976D2 !important;
        }
        
        /* ===== FORMS & INPUTS ===== */
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input,
        .stNumberInput > div > div > input,
        textarea {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #CCCCCC !important;
        }
        
        /* Input labels */
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label {
            color: #000000 !important;
        }
        
        /* ===== DATAFRAMES ===== */
        
        .stDataFrame {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        .stDataFrame table {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        .stDataFrame th {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
        }
        
        .stDataFrame td {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        /* ===== METRICS ===== */
        
        [data-testid="stMetricValue"] {
            color: #000000 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #000000 !important;
        }
        
        [data-testid="stMetricDelta"] {
            color: #000000 !important;
        }
        
        /* ===== BUTTONS ===== */
        
        .stButton > button {
            color: #FFFFFF !important;
            background-color: #1976D2 !important;
            border: none !important;
        }
        
        .stButton > button:hover {
            background-color: #1565C0 !important;
        }
        
        .stButton > button[kind="secondary"] {
            color: #000000 !important;
            background-color: #F0F2F6 !important;
        }
        
        /* ===== INFO/WARNING/ERROR BOXES ===== */
        
        .stAlert {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        .stSuccess {
            background-color: #E8F5E9 !important;
            color: #1B5E20 !important;
        }
        
        .stInfo {
            background-color: #E3F2FD !important;
            color: #0D47A1 !important;
        }
        
        .stWarning {
            background-color: #FFF3E0 !important;
            color: #E65100 !important;
        }
        
        .stError {
            background-color: #FFEBEE !important;
            color: #B71C1C !important;
        }
        
        /* ===== EXPANDERS ===== */
        
        .streamlit-expanderHeader {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
        }
        
        .streamlit-expanderContent {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        /* ===== CHARTS (PLOTLY) ===== */
        
        .js-plotly-plot {
            background-color: #FFFFFF !important;
        }
        
        /* ===== CODE BLOCKS ===== */
        
        .stCodeBlock {
            background-color: #F5F5F5 !important;
        }
        
        code {
            color: #D32F2F !important;
            background-color: #F5F5F5 !important;
        }
        
        /* ===== MARKDOWN ===== */
        
        .stMarkdown {
            color: #000000 !important;
        }
        
        /* ===== SCROLLBARS ===== */
        
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #F0F2F6;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #CCCCCC;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #999999;
        }
    </style>
    """, unsafe_allow_html=True)

