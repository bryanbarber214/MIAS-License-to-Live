"""
Admin Authentication Module
License to Live: MIAS - Python/Streamlit Version
Protects staff/admin pages with password authentication
"""

import streamlit as st
from typing import Tuple

def check_admin_authentication() -> bool:
    """
    Check if admin user is authenticated
    Returns True if authenticated, False otherwise
    """
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    return st.session_state.admin_authenticated


def admin_login_page():
    """
    Display admin login page
    Call this at the top of any protected page
    Returns True if authenticated, False if login screen should be shown
    """
    # Check if already authenticated
    if check_admin_authentication():
        return True
    
    # Show login screen
    st.markdown("""
    <div style="max-width: 500px; margin: 2rem auto; padding: 2rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; text-align: center; color: white;">
        <h1>🔐 Staff Access Required</h1>
        <p>This page requires staff authentication</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔑 Staff Login")
        
        with st.form("admin_login_form"):
            username = st.text_input(
                "Username:",
                placeholder="Enter staff username",
                help="Contact admin if you don't have credentials"
            )
            
            password = st.text_input(
                "Password:",
                type="password",
                placeholder="Enter password",
                help="Use the staff password provided by your administrator"
            )
            
            submitted = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
            
            if submitted:
                if authenticate_admin(username, password):
                    st.session_state.admin_authenticated = True
                    st.success("✅ Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
                    st.warning("⚠️ Please contact your administrator if you've forgotten your credentials")
        
        st.markdown("---")
        
        st.info("""
        **🏥 Staff Access Only**
        
        This page is for authorized medical staff only. If you are a patient, 
        please use the **Patient Portal** to access your information.
        
        📞 Need help? Contact your system administrator.
        """)
    
    return False


def authenticate_admin(username: str, password: str) -> bool:
    """
    Authenticate admin user against stored credentials
    Credentials are stored in Streamlit secrets
    """
    try:
        # Get credentials from Streamlit secrets
        correct_username = st.secrets["admin"]["username"]
        correct_password = st.secrets["admin"]["password"]
        
        # Check credentials
        if username == correct_username and password == correct_password:
            return True
        else:
            return False
            
    except Exception as e:
        # If secrets not configured, use default (FOR DEVELOPMENT ONLY)
        st.warning("""
        ⚠️ **Admin credentials not configured in Streamlit secrets!**
        
        Using default credentials: `admin` / `password123`
        
        **IMPORTANT:** Configure proper credentials in Streamlit Cloud settings!
        """)
        
        # Default credentials (INSECURE - only for development)
        return username == "admin" and password == "password123"


def admin_logout():
    """Logout admin user"""
    st.session_state.admin_authenticated = False
    st.rerun()


def show_logout_button():
    """Display logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Staff Session")
        st.success("✅ Authenticated")
        
        if st.button("🚪 Logout", use_container_width=True):
            admin_logout()
