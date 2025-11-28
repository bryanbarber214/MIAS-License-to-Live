"""
Patient Registration Page
License to Live: MIAS - Python/Streamlit Version
Barcode scanner integration with AAMVA parser
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aamva_parser import AAMVAParser
import database as db
from admin_auth import admin_login_page, show_logout_button

# Page configuration - FORCE LIGHT THEME
st.set_page_config(
    page_title="Patient Registration - MIAS",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AUTHENTICATION CHECK - Must be logged in to access this page
if not admin_login_page():
    st.stop()

# Show logout button in sidebar
show_logout_button()

# AGGRESSIVE CSS - Force white background and black text EVERYWHERE
st.markdown("""
<style>
    /* FORCE ENTIRE APP TO WHITE BACKGROUND */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* FORCE MAIN CONTENT AREA WHITE */
    .main .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* FORCE ALL TEXT TO BLACK */
    .stApp, .stApp * {
        color: #000000 !important;
    }
    
    /* FORCE MARKDOWN TEXT BLACK */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1, 
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, 
    .stMarkdown h5, .stMarkdown h6, .stMarkdown strong {
        color: #000000 !important;
    }
    
    /* FORCE EXPANDER TO WHITE BACKGROUND WITH BLACK TEXT */
    .streamlit-expanderHeader {
        background-color: #F8F9FA !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-top: none !important;
    }
    
    .streamlit-expanderContent p,
    .streamlit-expanderContent li,
    .streamlit-expanderContent strong,
    .streamlit-expanderContent ol,
    .streamlit-expanderContent ul,
    .streamlit-expanderContent span {
        color: #000000 !important;
        background-color: transparent !important;
    }
    
    /* FORCE TEXTAREA WHITE BACKGROUND WITH BLACK TEXT */
    textarea {
        color: #000000 !important;
        font-weight: 600 !important;
        background-color: #FFFFFF !important;
        border: 2px solid #1976D2 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        padding: 10px !important;
    }
    
    textarea::placeholder {
        color: #555555 !important;
        font-weight: 400 !important;
        font-size: 14px !important;
    }
    
    /* FORCE TEXT INPUT FIELDS WHITE */
    input[type="text"] {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
        padding: 8px !important;
    }
    
    /* FORCE LABELS BLACK */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* FORCE INFO BOXES READABLE */
    .stAlert {
        background-color: #E3F2FD !important;
        color: #000000 !important;
    }
    
    /* Custom styled boxes */
    .scan-box {
        border: 3px dashed #1976D2;
        padding: 1.5rem;
        background-color: #FFFFFF;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #000000;
    }
    
    .scan-box h4 {
        color: #1976D2 !important;
        margin: 0 !important;
    }
    
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-left: 4px solid #4CAF50;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000 !important;
    }
    
    .success-box strong {
        color: #2E7D32 !important;
    }
    
    .error-box {
        background-color: #FFEBEE;
        padding: 1rem;
        border-left: 4px solid #F44336;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000 !important;
    }
    
    .error-box strong {
        color: #C62828 !important;
    }
    
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-left: 4px solid #FF9800;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000 !important;
    }
    
    .warning-box strong {
        color: #E65100 !important;
    }
    
    .parsed-data {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-left: 4px solid #4CAF50;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        border-radius: 5px;
        color: #000000 !important;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* FORCE BUTTONS READABLE */
    .stButton button {
        color: #FFFFFF !important;
        background-color: #1976D2 !important;
        border: none !important;
    }
    
    .stButton button:hover {
        background-color: #1565C0 !important;
    }
    
    /* FORCE SELECTBOX READABLE */
    .stSelectbox select {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📋 Patient Registration")
st.markdown("### Barcode Scanner Integration")

# Initialize session state
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = None

# Instructions
with st.expander("📋 Instructions", expanded=True):
    st.markdown("""
    1. Click in the **Barcode Input** field below
    2. Scan the driver's license 2D barcode with your **Eyoyo scanner**
    3. Data will automatically populate (@ symbol and line breaks are normal)
    4. Click **Parse Barcode** to extract information
    5. Review the parsed information
    6. Add missing information (phone, email, blood type)
    7. **Create a 4-digit PIN** for patient portal access
    8. Click **Register Patient** to save to database
    
    **Note:** The Eyoyo scanner outputs @ symbol and line breaks - this is expected behavior!
    
    **Patient Portal:** After registration, patients can use their License # + PIN to access the Patient Portal and manage their medical information.
    """)

st.markdown("---")

# Main content layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="scan-box">
        <h4>🔍 Step 1: Scan Driver's License</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ The Eyoyo scanner outputs @ symbol and line breaks. This is normal - the parser will clean it automatically.")
    
    barcode_input = st.text_area(
        "Barcode Input:",
        value="",
        height=200,
        placeholder="Click here and scan driver's license...\n\nScanner will output:\n@\n[barcode data with line breaks]\n\nThis is normal!",
        help="Position cursor here and scan the 2D barcode on the back of the driver's license"
    )
    
    if st.button("🔍 Parse Barcode", type="primary", use_container_width=True):
        if not barcode_input or len(barcode_input.strip()) == 0:
            st.warning("⚠️ Please scan a barcode first!")
        else:
            # Parse the barcode
            parser = AAMVAParser()
            success, fields, error = parser.parse(barcode_input)
            
            if success:
                st.session_state.parsed_data = parser
                st.session_state.patient_data = parser.prepare_for_database()
                
                # Check for duplicates
                if db.license_exists(fields['license_number']):
                    st.markdown("""
                    <div class="warning-box">
                        <strong>⚠️ Warning:</strong> This license number already exists in the database!<br>
                        <strong>License Number:</strong> {}
                    </div>
                    """.format(fields['license_number']), unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="success-box">
                        ✅ Barcode parsed successfully!
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    ❌ Error parsing barcode: {}
                </div>
                """.format(error), unsafe_allow_html=True)
                st.session_state.parsed_data = None
                st.session_state.patient_data = None

with col2:
    st.markdown("### 📄 Step 2: Review Parsed Data")
    
    if st.session_state.parsed_data:
        # Display parsed data
        st.markdown("""
        <div class="parsed-data">
{}
        </div>
        """.format(st.session_state.parsed_data.format_display()), unsafe_allow_html=True)
        
        # Additional information form
        st.markdown("### Additional Information")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            phone = st.text_input(
                "Phone Number (Optional):",
                placeholder="e.g., 972-555-0100",
                help="Patient's phone number"
            )
            
            email = st.text_input(
                "Email Address (Optional):",
                placeholder="e.g., patient@email.com",
                help="Patient's email address"
            )
        
        with col_b:
            blood_type = st.selectbox(
                "Blood Type (Optional):",
                options=["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                help="Patient's blood type"
            )
            
            # PIN creation (REQUIRED)
            pin = st.text_input(
                "Create 4-Digit PIN (Required):",
                type="password",
                max_chars=4,
                placeholder="Enter 4 digits",
                help="Patient will use this PIN with their license number to access the Patient Portal"
            )
            
            pin_confirm = st.text_input(
                "Confirm PIN (Required):",
                type="password",
                max_chars=4,
                placeholder="Re-enter 4 digits",
                help="Confirm the PIN"
            )
        
        # Validate PIN
        pin_valid = False
        if pin and pin_confirm:
            if pin != pin_confirm:
                st.error("❌ PINs do not match!")
            elif not pin.isdigit() or len(pin) != 4:
                st.error("❌ PIN must be exactly 4 digits!")
            else:
                st.success("✅ PIN validated")
                pin_valid = True
        elif pin or pin_confirm:
            st.warning("⚠️ Please enter PIN in both fields")
        
        # Update patient data with optional fields
        if phone:
            st.session_state.patient_data['phone'] = phone
        if email:
            st.session_state.patient_data['email'] = email
        if blood_type:
            st.session_state.patient_data['blood_type'] = blood_type
        if pin_valid:
            st.session_state.patient_data['pin'] = pin
        
        # Show PIN requirement notice
        if not pin_valid:
            st.info("ℹ️ **Note:** A 4-digit PIN is required for patient portal access. The patient will use their License Number + PIN to log in and manage their medical information.")
        
    else:
        st.info("No data parsed yet. Scan a barcode to begin.")

st.markdown("---")

# Action buttons
st.markdown("### 📥 Step 3: Save to Database")

col1, col2 = st.columns(2)

with col1:
    # Check if PIN is set before enabling registration
    can_register = (st.session_state.patient_data is not None and 
                   st.session_state.patient_data.get('pin') is not None)
    
    if st.button("✅ Register Patient", type="primary", use_container_width=True, 
                disabled=not can_register):
        if st.session_state.patient_data:
            # Final validation
            if not st.session_state.patient_data.get('pin'):
                st.error("❌ Cannot register: 4-digit PIN is required!")
            # Check for duplicate
            elif db.license_exists(st.session_state.patient_data['license_number']):
                st.error("❌ Cannot register: License number already exists in database!")
            else:
                # Insert into database
                success, message = db.insert_patient(st.session_state.patient_data)
                
                if success:
                    st.success(f"""
                    ✅ {message}
                    
                    **Patient:** {st.session_state.patient_data['first_name']} {st.session_state.patient_data['last_name']}  
                    **License:** {st.session_state.patient_data['license_number']}
                    
                    **Patient Portal Access:**
                    - License #: {st.session_state.patient_data['license_number']}
                    - PIN: {st.session_state.patient_data['pin']}
                    
                    ⚠️ Please provide these credentials to the patient for portal access.
                    """)
                    
                    # Clear form after success
                    st.session_state.parsed_data = None
                    st.session_state.patient_data = None
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Registration failed: {message}")

with col2:
    if st.button("🔄 Clear Form", use_container_width=True):
        st.session_state.parsed_data = None
        st.session_state.patient_data = None
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Patient Registration")
    st.info("""
    This page allows you to register new patients by scanning their driver's license.
    
    **Requirements:**
    - Eyoyo EY-009P barcode scanner
    - Bluetooth connection to computer
    - Valid US driver's license (AAMVA format)
    """)
    
    st.markdown("### 🔍 Scanner Status")
    st.success("Ready for scan")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Ensure scanner is paired via Bluetooth
    - Click in the text area before scanning
    - The @ symbol and line breaks are normal
    - System detects duplicate license numbers
    """)
