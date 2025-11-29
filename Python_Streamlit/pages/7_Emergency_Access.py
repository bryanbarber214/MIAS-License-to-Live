"""
Emergency Access Page
License to Live: MIAS - Python/Streamlit Version
Public emergency medical information access via QR code
NO LOGIN REQUIRED - For emergency use only
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from global_styles import apply_global_styles

# Page configuration
st.set_page_config(
    page_title="Emergency Medical Access - MIAS",
    page_icon="🚨",
    layout="wide"
)

# Apply global styles
apply_global_styles()

# Additional CSS for emergency page
st.markdown("""
<style>
    .emergency-header {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .emergency-header h1, .emergency-header p {
        color: white !important;
    }
    
    .critical-alert {
        background-color: #ffebee;
        border-left: 5px solid #e74c3c;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    
    .info-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }
    
    .emergency-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Get emergency token from URL parameters
query_params = st.query_params
emergency_token = query_params.get("token", None)

# Emergency header
st.markdown("""
<div class="emergency-header">
    <h1>🚨 EMERGENCY MEDICAL ACCESS</h1>
    <p>Critical Patient Information - Emergency Use Only</p>
</div>
""", unsafe_allow_html=True)

# If no token provided
if not emergency_token:
    st.error("❌ No emergency access token provided")
    st.info("""
    **This page requires a valid emergency access QR code.**
    
    If you are a patient:
    - Your QR code was provided during registration
    - Keep it in your wallet or on your phone
    - Show it to medical professionals in emergencies
    
    If you are a medical professional:
    - Ask the patient for their emergency QR code
    - Scan the QR code with your phone camera
    - You will be directed to their emergency medical information
    """)
    st.stop()

# Fetch patient data using emergency token
patient_data = db.get_patient_by_emergency_token(emergency_token)

if not patient_data:
    st.error("❌ Invalid or expired emergency access token")
    st.warning("This QR code may be invalid or the patient record may have been removed.")
    st.stop()

# Log the emergency access
db.log_emergency_access(patient_data['patient_id'], emergency_token)

# Display patient information
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 👤 Patient Identification")
    st.markdown(f"""
    **Name:** {patient_data['first_name']} {patient_data['last_name']}  
    **Date of Birth:** {patient_data['date_of_birth']} (Age: {db.calculate_age(patient_data['date_of_birth'])} years)  
    **License Number:** {patient_data['license_number']}
    """)

with col2:
    # Blood type in large text
    blood_type = patient_data.get('blood_type', 'Unknown')
    st.markdown(f"""
    <div style="background-color: #e74c3c; color: white; padding: 1.5rem; 
                border-radius: 10px; text-align: center;">
        <h2 style="color: white; margin: 0;">🩸 Blood Type</h2>
        <h1 style="color: white; margin: 0.5rem 0; font-size: 3rem;">{blood_type}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# CRITICAL ALLERGIES
st.markdown("### ⚠️ CRITICAL ALLERGIES")
allergies = db.get_allergies(patient_data['patient_id'])

if not allergies.empty:
    # Separate life-threatening allergies
    life_threatening = allergies[allergies['severity'] == 'Life-threatening']
    other_allergies = allergies[allergies['severity'] != 'Life-threatening']
    
    if not life_threatening.empty:
        st.markdown('<div class="critical-alert">', unsafe_allow_html=True)
        st.error("🚨 **LIFE-THREATENING ALLERGIES:**")
        for _, allergy in life_threatening.iterrows():
            st.markdown(f"""
            - **{allergy['allergen']}** ({allergy.get('allergy_type', 'Unknown type')})
              - Reaction: {allergy.get('reaction', 'Not specified')}
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if not other_allergies.empty:
        st.warning("**Other Allergies:**")
        for _, allergy in other_allergies.iterrows():
            severity = allergy.get('severity', 'Unknown')
            st.markdown(f"- **{allergy['allergen']}** - {severity} ({allergy.get('allergy_type', '')})")
else:
    st.success("✅ No known allergies recorded")

st.markdown("---")

# CURRENT MEDICATIONS
st.markdown("### 💊 Current Medications")
medications = db.get_medications(patient_data['patient_id'])

if not medications.empty:
    for _, med in medications.iterrows():
        dosage = med.get('dosage', '')
        frequency = med.get('frequency', '')
        st.markdown(f"- **{med['medication_name']}** - {dosage} {frequency}")
else:
    st.info("No current medications recorded")

st.markdown("---")

# MEDICAL CONDITIONS
st.markdown("### 🏥 Medical Conditions")
conditions = db.get_conditions(patient_data['patient_id'])

if not conditions.empty:
    for _, condition in conditions.iterrows():
        severity = condition.get('severity', '')
        severity_badge = f" ({severity})" if severity else ""
        st.markdown(f"- **{condition['condition_name']}**{severity_badge}")
        if condition.get('notes'):
            st.caption(f"  ↳ {condition['notes']}")
else:
    st.info("No medical conditions recorded")

st.markdown("---")

# EMERGENCY CONTACTS
st.markdown("### 📞 Emergency Contacts")
emergency_contacts = db.get_emergency_contacts(patient_data['patient_id'])

if not emergency_contacts.empty:
    for _, contact in emergency_contacts.iterrows():
        is_primary = "⭐ PRIMARY" if contact.get('is_primary') else ""
        relationship = contact.get('relationship', 'Contact')
        st.markdown(f"""
        **{contact['contact_name']}** ({relationship}) {is_primary}  
        📱 {contact['phone_number']}
        """)
else:
    st.warning("No emergency contacts on file")

st.markdown("---")

# FOOTER INFO
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    **Last Updated:**  
    {patient_data.get('updated_at', 'Unknown')}
    """)

with col2:
    st.markdown(f"""
    **Access Code:**  
    EM-{patient_data['patient_id']}-{emergency_token[:8]}
    """)

with col3:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    **Accessed:**  
    {current_time}
    """)

st.markdown("---")

# Disclaimer
st.warning("""
⚠️ **EMERGENCY USE ONLY**

This information is provided for emergency medical treatment only. 
All access to this page is logged for security and HIPAA compliance.

For non-emergency access to patient records, please use the appropriate 
staff or provider portal with proper authentication.
""")

# Print button
if st.button("🖨️ Print This Page", use_container_width=True):
    st.info("Use your browser's print function (Ctrl+P or Cmd+P) to print this emergency summary.")

# Sidebar
with st.sidebar:
    st.markdown("### 🚨 Emergency Access")
    st.error("""
    **Active Emergency Session**
    
    This is a public emergency access page.
    No login required.
    """)
    
    st.markdown("### 📋 Information Displayed")
    st.info("""
    - Patient Identification
    - Blood Type
    - Critical Allergies
    - Current Medications
    - Medical Conditions
    - Emergency Contacts
    """)
    
    st.markdown("### 🔒 Privacy Notice")
    st.warning("""
    All access is logged and monitored.
    
    This page is for emergency medical use only.
    
    Unauthorized access may result in legal action.
    """)
    
    st.markdown("### 📞 Support")
    st.markdown("""
    **For technical issues:**
    Contact system administrator
    
    **For medical emergencies:**
    Call 911
    """)
