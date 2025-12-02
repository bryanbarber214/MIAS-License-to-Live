"""
Emergency Access Page
License to Live: MIAS - Python/Streamlit Version
Displays patient emergency information when QR code is scanned
"""

import streamlit as st
from global_styles import apply_global_styles
import database as db

# Page configuration
st.set_page_config(
    page_title="Emergency Access - MIAS",
    page_icon="🚨",
    layout="wide"
)

# Apply global styles
apply_global_styles()

# Custom CSS for emergency page
st.markdown("""
<style>
    .emergency-header {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .critical-info-box {
        background-color: #ffebee;
        border-left: 4px solid #e74c3c;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Get token from URL parameters
query_params = st.query_params
emergency_token = query_params.get('token', None)

# Emergency header
st.markdown("""
<div class="emergency-header">
    <h1>🚨 EMERGENCY MEDICAL ACCESS</h1>
    <h3>License to Live: MIAS</h3>
</div>
""", unsafe_allow_html=True)

if not emergency_token:
    st.error("❌ No emergency token provided")
    st.info("""
    This page is accessed by scanning a patient's emergency QR code.
    
    If you are medical personnel and need to access a patient's emergency information:
    1. Scan the QR code on the patient's medical card or driver's license
    2. You will be automatically directed to their emergency medical information
    """)
    st.stop()

# Look up patient by emergency token
patient = db.get_patient_by_emergency_token(emergency_token)

if not patient:
    st.error("❌ Invalid or expired emergency access token")
    st.warning("""
    This emergency access link may be:
    - Invalid
    - Expired
    - Never activated
    
    Please contact the patient's emergency contact or hospital administration.
    """)
    st.stop()

# Log emergency access
db.log_emergency_access(patient['patient_id'], emergency_token)

# Display patient information
st.success("✅ Emergency access granted - Information displayed below")

# CRITICAL INFORMATION (Top Priority)
st.markdown("## 🚨 CRITICAL INFORMATION")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="critical-info-box">
        <h3>👤 Patient Identity</h3>
        <p><strong>Name:</strong> {patient['first_name']} {patient['last_name']}</p>
        <p><strong>DOB:</strong> {patient['date_of_birth']}</p>
        <p><strong>Age:</strong> {db.calculate_age(patient['date_of_birth'])} years</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    blood_type = patient.get('blood_type', 'Unknown')
    st.markdown(f"""
    <div class="critical-info-box">
        <h3>🩸 Blood Type</h3>
        <h1 style="color: #e74c3c; text-align: center; margin: 1rem 0;">{blood_type}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="critical-info-box">
        <h3>📞 Contact Info</h3>
        <p><strong>Phone:</strong> {patient.get('phone', 'Not available')}</p>
        <p><strong>Email:</strong> {patient.get('email', 'Not available')}</p>
    </div>
    """, unsafe_allow_html=True)

# ALLERGIES (Critical for treatment)
st.markdown("---")
st.markdown("## ⚠️ ALLERGIES & ADVERSE REACTIONS")

allergies_df = db.get_allergies(patient['patient_id'])

if not allergies_df.empty:
    for _, allergy in allergies_df.iterrows():
        severity_color = {
            'Life-threatening': '#c0392b',
            'Severe': '#e67e22',
            'Moderate': '#f39c12',
            'Mild': '#27ae60'
        }.get(allergy.get('severity', 'Unknown'), '#95a5a6')
        
        st.markdown(f"""
        <div class="warning-box" style="border-left-color: {severity_color};">
            <h4 style="color: {severity_color}; margin: 0;">⚠️ {allergy['allergen']}</h4>
            <p><strong>Type:</strong> {allergy.get('allergy_type', 'Unknown')}</p>
            <p><strong>Severity:</strong> {allergy.get('severity', 'Unknown')}</p>
            <p><strong>Reaction:</strong> {allergy.get('reaction', 'Unknown')}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("✅ No known allergies on record")

# CURRENT MEDICATIONS
st.markdown("---")
st.markdown("## 💊 CURRENT MEDICATIONS")

medications_df = db.get_medications(patient['patient_id'])

if not medications_df.empty:
    for _, med in medications_df.iterrows():
        with st.expander(f"💊 {med['medication_name']} - {med.get('dosage', 'Dose not specified')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Frequency:** {med.get('frequency', 'Not specified')}")
                st.write(f"**Prescribing Doctor:** {med.get('prescribing_doctor', 'Unknown')}")
            with col2:
                st.write(f"**Start Date:** {med.get('start_date', 'Unknown')}")
                if med.get('notes'):
                    st.write(f"**Notes:** {med['notes']}")
else:
    st.info("No current medications on record")

# MEDICAL CONDITIONS
st.markdown("---")
st.markdown("## 🏥 MEDICAL CONDITIONS")

conditions_df = db.get_conditions(patient['patient_id'])

if not conditions_df.empty:
    for _, condition in conditions_df.iterrows():
        severity_emoji = {
            'Severe': '🔴',
            'Moderate': '🟡',
            'Mild': '🟢'
        }.get(condition.get('severity', 'Unknown'), '⚪')
        
        with st.expander(f"{severity_emoji} {condition['condition_name']} ({condition.get('severity', 'Unknown')})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Diagnosis Date:** {condition.get('diagnosis_date', 'Unknown')}")
            with col2:
                if condition.get('notes'):
                    st.write(f"**Notes:** {condition['notes']}")
else:
    st.info("No chronic medical conditions on record")

# EMERGENCY CONTACTS
st.markdown("---")
st.markdown("## 📞 EMERGENCY CONTACTS")

contacts_df = db.get_emergency_contacts(patient['patient_id'])

if not contacts_df.empty:
    for _, contact in contacts_df.iterrows():
        primary_badge = "🔴 PRIMARY" if contact.get('is_primary') else ""
        with st.expander(f"👤 {contact['contact_name']} - {contact['relationship']} {primary_badge}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Phone:** {contact['phone_number']}")
            with col2:
                st.write(f"**Email:** {contact.get('email', 'Not provided')}")
else:
    st.warning("⚠️ No emergency contacts on record")

# INSURANCE INFORMATION
st.markdown("---")
st.markdown("## 🏥 INSURANCE INFORMATION")

insurance_df = db.get_insurance(patient['patient_id'])

if not insurance_df.empty:
    for _, ins in insurance_df.iterrows():
        with st.expander(f"🏥 {ins['insurance_provider']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Policy Number:** {ins.get('policy_number', 'Not available')}")
                st.write(f"**Group Number:** {ins.get('group_number', 'Not available')}")
            with col2:
                st.write(f"**Subscriber:** {ins.get('subscriber_name', 'Unknown')}")
                st.write(f"**Phone:** {ins.get('phone_number', 'Not available')}")
else:
    st.warning("⚠️ No insurance information on record")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>🚨 Emergency Access Log</strong></p>
    <p>This emergency access has been logged and timestamped.</p>
    <p>License to Live: Medical Information Access System (MIAS)</p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.markdown("### 🚨 Emergency Access")
    st.error("**Emergency Mode Active**")
    
    st.markdown("### ℹ️ Information")
    st.info("""
    This page displays critical medical information for emergency situations.
    
    All access is logged and timestamped for security and auditing purposes.
    """)
    
    st.markdown("### ⚠️ Important")
    st.warning("""
    **For Medical Personnel Only**
    
    This information is confidential and protected under HIPAA regulations.
    """)
