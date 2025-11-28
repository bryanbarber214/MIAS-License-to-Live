"""
Patient Portal - Login Page
License to Live: MIAS - Python/Streamlit Version
Patients log in with License # + PIN to access their medical information
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db

# Page configuration
st.set_page_config(
    page_title="Patient Portal - MIAS",
    page_icon="🔐",
    layout="wide"
)

# AGGRESSIVE CSS - Force white background and black text
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    .main .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .stApp, .stApp * {
        color: #000000 !important;
    }
    
    .login-box {
        background-color: #F8F9FA;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #1976D2;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .welcome-header {
        text-align: center;
        color: #1976D2;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1976D2;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = None
if 'patient_name' not in st.session_state:
    st.session_state.patient_name = None

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.patient_id = None
    st.session_state.patient_name = None
    st.rerun()

# If already authenticated, redirect to dashboard
if st.session_state.authenticated:
    st.switch_page("pages/6_Patient_Dashboard.py")

# Login Page
st.markdown("""
<div class="welcome-header">
    <h1>🔐 Patient Portal</h1>
    <h3>Secure Access to Your Medical Information</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Login form
st.markdown("""
<div class="login-box">
    <h3 style="text-align: center; color: #1976D2;">Sign In</h3>
    <p style="text-align: center; color: #666;">Enter your credentials to access your medical information</p>
</div>
""", unsafe_allow_html=True)

# Center the login form
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("login_form"):
        st.markdown("### 🆔 Login Credentials")
        
        license_number = st.text_input(
            "Driver's License Number:",
            placeholder="Enter your license number",
            max_chars=20,
            help="The license number from your driver's license"
        )
        
        pin = st.text_input(
            "4-Digit PIN:",
            type="password",
            max_chars=4,
            placeholder="Enter your PIN",
            help="The PIN you created during registration"
        )
        
        st.markdown("&nbsp;")  # Spacing
        
        submitted = st.form_submit_button("🔓 Sign In", use_container_width=True, type="primary")
        
        if submitted:
            if not license_number or not pin:
                st.error("❌ Please enter both License Number and PIN")
            elif not pin.isdigit() or len(pin) != 4:
                st.error("❌ PIN must be exactly 4 digits")
            else:
                # Authenticate
                success, patient_id, message = db.authenticate_patient(license_number, pin)
                
                if success:
                    # Get patient name
                    patient_data = db.get_patient_by_id(patient_id)
                    
                    if patient_data:
                        st.session_state.authenticated = True
                        st.session_state.patient_id = patient_id
                        st.session_state.patient_name = f"{patient_data['first_name']} {patient_data['last_name']}"
                        
                        st.success(f"✅ {message}")
                        st.balloons()
                        
                        # Redirect to dashboard
                        st.switch_page("pages/6_Patient_Dashboard.py")
                    else:
                        st.error("❌ Error loading patient data")
                else:
                    st.error(f"❌ {message}")

st.markdown("---")

# Information section
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4>ℹ️ First Time Here?</h4>
        <p>If you recently registered as a patient, you should have received:</p>
        <ul>
            <li>Your Driver's License Number</li>
            <li>A 4-digit PIN</li>
        </ul>
        <p>Use these credentials to log in.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4>🔒 Security Notice</h4>
        <p>Your medical information is protected. Never share your PIN with anyone.</p>
        <p><strong>Forgot your PIN?</strong><br>
        Contact your healthcare provider or visit the registration desk for a PIN reset.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Features section
st.markdown("### 📋 What You Can Do in the Patient Portal")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📊 View Your Information**
    - Personal details
    - Medical history
    - Contact information
    """)

with col2:
    st.markdown("""
    **🏥 Manage Medical Data**
    - Medical conditions
    - Allergies
    - Medications
    - Emergency contacts
    """)

with col3:
    st.markdown("""
    **🔐 Secure Access**
    - Your data is encrypted
    - HIPAA compliant
    - Only you can access
    """)

# Sidebar
with st.sidebar:
    st.markdown("### 🔐 Patient Portal")
    st.info("""
    **Welcome to the Patient Portal**
    
    Log in with your:
    - Driver's License Number
    - 4-Digit PIN
    
    **Need Help?**
    Contact your healthcare provider for assistance.
    """)
    
    st.markdown("### 📞 Support")
    st.markdown("""
    **Registration Desk**
    Available during business hours
    
    **For Technical Support:**
    Contact your healthcare facility
    """)
