"""
Patient Dashboard
License to Live: MIAS - Python/Streamlit Version
After login, patients can view and update their medical information
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Patient Dashboard - MIAS",
    page_icon="👤",
    layout="wide"
)

# AGGRESSIVE CSS
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
    
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white !important;
        margin-bottom: 2rem;
    }
    
    .dashboard-header h1, .dashboard-header p {
        color: white !important;
    }
    
    .info-card {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1976D2;
        margin: 1rem 0;
    }
    
    .medical-card {
        background-color: #FFF9C4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FBC02D;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Please log in to access the Patient Portal")
    if st.button("Go to Login Page"):
        st.switch_page("pages/5_Patient_Portal.py")
    st.stop()

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.patient_id = None
    st.session_state.patient_name = None
    st.switch_page("pages/5_Patient_Portal.py")

# Get patient data
patient_id = st.session_state.patient_id
patient_data = db.get_patient_by_id(patient_id)

if not patient_data:
    st.error("❌ Error loading patient data")
    st.stop()

# Dashboard Header
st.markdown(f"""
<div class="dashboard-header">
    <h1>👤 Welcome, {patient_data['first_name']}!</h1>
    <p>Manage your medical information securely</p>
</div>
""", unsafe_allow_html=True)

# Logout button in top right
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col4:
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.markdown("---")

# Navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview",
    "🏥 Medical Conditions", 
    "⚠️ Allergies",
    "💊 Medications",
    "📞 Emergency Contacts",
    "⚙️ Settings"
])

# TAB 1: Overview
with tab1:
    st.markdown("### 📊 Your Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Personal Information")
        st.markdown(f"**Name:** {patient_data['first_name']} {patient_data['last_name']}")
        st.markdown(f"**Date of Birth:** {patient_data['date_of_birth']}")
        st.markdown(f"**License Number:** {patient_data['license_number']}")
        st.markdown(f"**Blood Type:** {patient_data['blood_type'] if patient_data['blood_type'] else 'Not provided'}")
        
    with col2:
        st.markdown("#### Contact Information")
        st.markdown(f"**Phone:** {patient_data['phone'] if patient_data['phone'] else 'Not provided'}")
        st.markdown(f"**Email:** {patient_data['email'] if patient_data['email'] else 'Not provided'}")
        st.markdown(f"**Address:** {patient_data['address'] if patient_data['address'] else 'Not provided'}")
        st.markdown(f"**City:** {patient_data['city']}, {patient_data['state']} {patient_data['zip_code']}")
    
    st.info("ℹ️ **Note:** You can only update medical information. To update personal information (name, address), please contact the registration desk.")

# TAB 2: Medical Conditions
with tab2:
    st.markdown("### 🏥 Medical Conditions")
    
    # Get existing conditions
    conditions = db.get_conditions(patient_id)
    
    if not conditions.empty:
        st.dataframe(conditions, use_container_width=True, hide_index=True)
    else:
        st.info("No medical conditions recorded")
    
    st.markdown("---")
    st.markdown("#### ➕ Add New Condition")
    
    with st.form("add_condition"):
        condition_name = st.text_input("Condition Name:", placeholder="e.g., Hypertension, Diabetes")
        diagnosis_date = st.date_input("Diagnosis Date (Optional):")
        severity = st.selectbox("Severity:", ["", "Mild", "Moderate", "Severe", "Critical"])
        notes = st.text_area("Notes (Optional):", placeholder="Additional information about this condition")
        
        if st.form_submit_button("Add Condition", type="primary"):
            if not condition_name:
                st.error("❌ Condition name is required")
            else:
                success, message = db.add_condition(
                    patient_id, 
                    condition_name, 
                    str(diagnosis_date) if diagnosis_date else None,
                    severity if severity else None,
                    notes if notes else None
                )
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# TAB 3: Allergies
with tab3:
    st.markdown("### ⚠️ Allergies")
    
    # Get existing allergies
    allergies = db.get_allergies(patient_id)
    
    if not allergies.empty:
        st.dataframe(allergies, use_container_width=True, hide_index=True)
    else:
        st.info("No allergies recorded")
    
    st.markdown("---")
    st.markdown("#### ➕ Add New Allergy")
    
    with st.form("add_allergy"):
        allergen = st.text_input("Allergen:", placeholder="e.g., Penicillin, Peanuts, Latex")
        allergy_type = st.selectbox("Type:", ["", "Medication", "Food", "Environmental", "Other"])
        severity = st.selectbox("Severity:", ["", "Mild", "Moderate", "Severe", "Life-threatening"])
        reaction = st.text_input("Reaction (Optional):", placeholder="e.g., Rash, Anaphylaxis")
        
        if st.form_submit_button("Add Allergy", type="primary"):
            if not allergen:
                st.error("❌ Allergen name is required")
            else:
                success, message = db.add_allergy(
                    patient_id,
                    allergen,
                    allergy_type if allergy_type else None,
                    severity if severity else None,
                    reaction if reaction else None
                )
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# TAB 4: Medications
with tab4:
    st.markdown("### 💊 Current Medications")
    
    # Get existing medications
    medications = db.get_medications(patient_id)
    
    if not medications.empty:
        st.dataframe(medications, use_container_width=True, hide_index=True)
    else:
        st.info("No medications recorded")
    
    st.markdown("---")
    st.markdown("#### ➕ Add New Medication")
    
    with st.form("add_medication"):
        med_name = st.text_input("Medication Name:", placeholder="e.g., Lisinopril")
        dosage = st.text_input("Dosage (Optional):", placeholder="e.g., 10mg")
        frequency = st.text_input("Frequency (Optional):", placeholder="e.g., Once daily")
        prescriber = st.text_input("Prescriber (Optional):", placeholder="e.g., Dr. Smith")
        
        if st.form_submit_button("Add Medication", type="primary"):
            if not med_name:
                st.error("❌ Medication name is required")
            else:
                success, message = db.add_medication(
                    patient_id,
                    med_name,
                    dosage if dosage else None,
                    frequency if frequency else None,
                    prescriber if prescriber else None
                )
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# TAB 5: Emergency Contacts
with tab5:
    st.markdown("### 📞 Emergency Contacts")
    
    # Get existing contacts
    contacts = db.get_emergency_contacts(patient_id)
    
    if not contacts.empty:
        st.dataframe(contacts, use_container_width=True, hide_index=True)
    else:
        st.info("No emergency contacts recorded")
    
    st.markdown("---")
    st.markdown("#### ➕ Add Emergency Contact")
    
    with st.form("add_contact"):
        contact_name = st.text_input("Contact Name:", placeholder="e.g., John Doe")
        relationship = st.text_input("Relationship:", placeholder="e.g., Spouse, Parent, Sibling")
        phone = st.text_input("Phone Number:", placeholder="e.g., 972-555-0100")
        is_primary = st.checkbox("Primary Contact")
        
        if st.form_submit_button("Add Contact", type="primary"):
            if not contact_name or not phone:
                st.error("❌ Name and phone number are required")
            else:
                success, message = db.add_emergency_contact(
                    patient_id,
                    contact_name,
                    relationship if relationship else None,
                    phone,
                    is_primary
                )
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# TAB 6: Settings
with tab6:
    st.markdown("### ⚙️ Account Settings")
    
    st.markdown("#### 📱 Update Contact Information")
    
    with st.form("update_contact"):
        new_phone = st.text_input("Phone Number:", value=patient_data['phone'] if patient_data['phone'] else "", placeholder="972-555-0100")
        new_email = st.text_input("Email Address:", value=patient_data['email'] if patient_data['email'] else "", placeholder="patient@email.com")
        
        if st.form_submit_button("Update Contact Info"):
            updated = False
            if new_phone and new_phone != patient_data.get('phone'):
                success, message = db.update_patient_medical_info(patient_id, 'phone', new_phone)
                if success:
                    st.success(f"✅ Phone updated")
                    updated = True
                else:
                    st.error(f"❌ {message}")
                    
            if new_email and new_email != patient_data.get('email'):
                success, message = db.update_patient_medical_info(patient_id, 'email', new_email)
                if success:
                    st.success(f"✅ Email updated")
                    updated = True
                else:
                    st.error(f"❌ {message}")
            
            if updated:
                st.rerun()
            elif not new_phone and not new_email:
                st.warning("⚠️ Please enter phone or email to update")
    
    st.markdown("---")
    st.markdown("#### 🩸 Update Blood Type")
    
    with st.form("update_blood_type"):
        new_blood_type = st.selectbox(
            "Blood Type:", 
            options=["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            index=["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(patient_data['blood_type']) if patient_data['blood_type'] in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] else 0
        )
        
        if st.form_submit_button("Update Blood Type"):
            if new_blood_type:
                success, message = db.update_patient_medical_info(patient_id, 'blood_type', new_blood_type)
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Please select a blood type")

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {patient_data['first_name']} {patient_data['last_name']}")
    st.markdown(f"**License:** {patient_data['license_number']}")
    st.markdown(f"**Last Login:** {patient_data['last_login'] if patient_data['last_login'] else 'First time'}")
    
    st.markdown("---")
    
    st.markdown("### 📋 Quick Stats")
    conditions_count = len(db.get_conditions(patient_id))
    allergies_count = len(db.get_allergies(patient_id))
    medications_count = len(db.get_medications(patient_id))
    contacts_count = len(db.get_emergency_contacts(patient_id))
    
    st.metric("Medical Conditions", conditions_count)
    st.metric("Allergies", allergies_count)
    st.metric("Medications", medications_count)
    st.metric("Emergency Contacts", contacts_count)
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
        logout()
