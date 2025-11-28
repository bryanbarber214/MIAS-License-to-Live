"""
License to Live: MIAS - Main Application
Python/Streamlit Version
Medical Information Access System
"""

import streamlit as st
from global_styles import apply_global_styles

# Page configuration
st.set_page_config(
    page_title="License to Live: MIAS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styles
apply_global_styles()

# Custom CSS
st.markdown("""
<style>
    .main-title {
        color: #1565C0;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("""
<div class="main-title">
    <h1>🏥 License to Live: MIAS</h1>
    <h3>Medical Information Access System</h3>
    <p>Python/Streamlit Version</p>
</div>
""", unsafe_allow_html=True)

# Welcome message
st.markdown("""
### Welcome to the Medical Information Access System!

License to Live: MIAS enables emergency medical access by linking driver's licenses 
to critical health information. This Python/Streamlit version provides the same 
functionality as the R Shiny version, with enhanced deployment options.
""")

# Feature boxes with improved visibility
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔍 Patient Registration")
    st.markdown("""
    Scan driver's licenses with 2D barcode scanner
    
    **Features:**
    - ✅ AAMVA standard parser
    - ✅ Automatic data extraction
    - ✅ Duplicate detection
    - ✅ Real-time validation
    """)

with col2:
    st.markdown("### 🏥 Medical Information")
    st.markdown("""
    Comprehensive health record management
    
    **Includes:**
    - ✅ Medical conditions
    - ✅ Allergies & medications
    - ✅ Vaccinations & insurance
    - ✅ Emergency contacts
    """)

with col3:
    st.markdown("### 📊 Analytics Dashboard")
    st.markdown("""
    Real-time data visualization
    
    **Analytics:**
    - ✅ 8 summary metrics
    - ✅ Interactive plotly charts
    - ✅ Population insights
    - ✅ Export capabilities
    """)

st.markdown("---")

# Instructions
st.markdown("""
### 🚀 Getting Started

**Use the sidebar on the left** to navigate between the three main applications:

1. **📋 Patient Registration** - Register new patients using barcode scanner
2. **🏥 Medical Info Manager** - Add and view complete medical histories  
3. **📊 Analytics Dashboard** - View real-time statistics and visualizations

### 💡 Quick Tips

- **For Demos:** Start with the Analytics Dashboard to see the system in action
- **Scanner Required:** Patient Registration requires an Eyoyo EY-009P barcode scanner
- **Database:** All apps connect to the same AWS RDS MySQL database
- **Real-time:** Changes made in one app are immediately visible in others

### 🗄️ Database Connection

Connected to: **AWS RDS MySQL**  
Database: `mias_db`  
Status: 🟢 Active
""")

st.markdown("---")

# Team information
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👥 Team
    - Ryan King
    - Raphe Burstein  
    - Bryan Barber
    """)

with col2:
    st.markdown("""
    ### 📚 Course Info
    **SMU ITOM 6265**  
    Database Management  
    Fall 2025
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>License to Live: MIAS</strong></p>
    <p>Python/Streamlit Version | Healthcare Information Systems</p>
    <p>Built with ❤️ by Team Barber-King-Burstein</p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.markdown("### 📱 Navigation")
    st.info("""
    Select a page from above to begin:
    
    - **Patient Registration** 
    - **Medical Info Manager**
    - **Analytics Dashboard**
    """)
    
    st.markdown("### 🔐 Database")
    st.success("✅ Connected to AWS RDS")
    
    st.markdown("### 📊 System Stats")
    # Could add quick stats here if desired
    st.metric("Platform", "Streamlit")
    st.metric("Database", "MySQL 8.0")
    st.metric("Version", "Python 1.0")
