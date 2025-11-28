"""
Medical Information Manager Page
License to Live: MIAS - Python/Streamlit Version
Comprehensive medical history management
"""

import streamlit as st
import sys
import os
from datetime import date

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from admin_auth import admin_login_page, show_logout_button

# Page configuration
st.set_page_config(
    page_title="Medical Info Manager - MIAS",
    page_icon="🏥",
    layout="wide"
)

# AUTHENTICATION CHECK - Must be logged in to access this page
if not admin_login_page():
    st.stop()

# Show logout button in sidebar
show_logout_button()

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
    
    /* Make sure all text elements are black */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #000000 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F0F2F6;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Forms and inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    .patient-card {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-left: 4px solid #2196F3;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-msg {
        background-color: #E8F5E9;
        padding: 1rem;
        border-left: 4px solid #4CAF50;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .error-msg {
        background-color: #FFEBEE;
        padding: 1rem;
        border-left: 4px solid #F44336;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏥 Medical Information Manager")
st.markdown("### Comprehensive Health Record Management")

# Initialize session state
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

# Patient Search Section
st.markdown("---")
st.markdown("### 🔍 Step 1: Search for Patient")

col1, col2 = st.columns([2, 1])

with col1:
    search_term = st.text_input(
        "Search by license number, first name, or last name:",
        placeholder="e.g., 10896644 or BRYAN or BARBER",
        help="Search is case-insensitive"
    )

with col2:
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")
    if st.button("🔍 Search", type="primary", use_container_width=True):
        st.rerun()

# Perform search
patients_df = db.search_patients(search_term)

if not patients_df.empty:
    st.success(f"✅ Found {len(patients_df)} patient(s)")
    
    # Display patients table
    st.dataframe(
        patients_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "patient_id": "ID",
            "license_number": "License #",
            "first_name": "First Name",
            "last_name": "Last Name",
            "date_of_birth": "DOB",
            "city": "City",
            "state": "State"
        }
    )
    
    # Patient selection
    if len(patients_df) > 0:
        selected_idx = st.selectbox(
            "Select a patient to manage:",
            options=range(len(patients_df)),
            format_func=lambda i: f"{patients_df.iloc[i]['first_name']} {patients_df.iloc[i]['last_name']} (License: {patients_df.iloc[i]['license_number']})"
        )
        
        if st.button("✅ Load Patient", type="primary"):
            st.session_state.selected_patient = patients_df.iloc[selected_idx]['patient_id']
            st.rerun()

else:
    if search_term:
        st.warning("⚠️ No patients found matching your search.")
    else:
        st.info("ℹ️ Enter a search term to find patients.")

# Display selected patient
if st.session_state.selected_patient:
    st.markdown("---")
    
    # Get patient details
    patient = db.get_patient_details(st.session_state.selected_patient)
    
    if patient:
        # Patient card
        st.markdown(f"""
        <div class="patient-card">
            <h3>👤 {patient['first_name']} {patient['last_name']}</h3>
            <p><strong>DOB:</strong> {patient['date_of_birth']} | <strong>License:</strong> {patient['license_number']} | <strong>Blood Type:</strong> {patient.get('blood_type', 'N/A')}</p>
            <p><strong>Address:</strong> {patient.get('address', 'N/A')}, {patient.get('city', 'N/A')}, {patient.get('state', 'N/A')} {patient.get('zip_code', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for medical information
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🩺 Medical Conditions",
            "⚠️ Allergies",
            "💊 Medications",
            "💉 Vaccinations",
            "🏥 Insurance",
            "📞 Emergency Contacts"
        ])
        
        # TAB 1: Medical Conditions
        with tab1:
            st.subheader("Medical Conditions")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Condition")
                with st.form("add_condition", clear_on_submit=True):
                    condition_name = st.text_input("Condition Name*:", placeholder="e.g., Hypertension")
                    diagnosis_date = st.date_input("Diagnosis Date:", value=date.today())
                    severity = st.selectbox("Severity:", ["", "Mild", "Moderate", "Severe", "Critical"])
                    notes = st.text_area("Notes:", placeholder="Additional details...")
                    
                    submitted = st.form_submit_button("➕ Add Condition", type="primary")
                    if submitted:
                        if condition_name:
                            success, msg = db.add_condition(
                                st.session_state.selected_patient,
                                condition_name,
                                str(diagnosis_date),
                                severity if severity else None,
                                notes if notes else None
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("❌ Condition name is required!")
            
            with col2:
                st.markdown("#### Existing Conditions")
                conditions_df = db.get_conditions(st.session_state.selected_patient)
                if not conditions_df.empty:
                    st.dataframe(conditions_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No conditions recorded yet.")
        
        # TAB 2: Allergies
        with tab2:
            st.subheader("Allergies")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Allergy")
                with st.form("add_allergy", clear_on_submit=True):
                    allergen = st.text_input("Allergen*:", placeholder="e.g., Penicillin")
                    allergy_type = st.selectbox("Type:", ["", "Medication", "Food", "Environmental", "Other"])
                    reaction = st.text_input("Reaction:", placeholder="e.g., Anaphylaxis")
                    severity = st.selectbox("Severity:", ["", "Mild", "Moderate", "Severe", "Life-threatening"])
                    
                    submitted = st.form_submit_button("➕ Add Allergy", type="primary")
                    if submitted:
                        if allergen:
                            success, msg = db.add_allergy(
                                st.session_state.selected_patient,
                                allergen,
                                allergy_type if allergy_type else None,
                                reaction if reaction else None,
                                severity if severity else None
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("❌ Allergen name is required!")
            
            with col2:
                st.markdown("#### Known Allergies")
                allergies_df = db.get_allergies(st.session_state.selected_patient)
                if not allergies_df.empty:
                    st.dataframe(allergies_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No allergies recorded yet.")
        
        # TAB 3: Medications
        with tab3:
            st.subheader("Medications")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Medication")
                with st.form("add_medication", clear_on_submit=True):
                    medication_name = st.text_input("Medication Name*:", placeholder="e.g., Lisinopril")
                    dosage = st.text_input("Dosage:", placeholder="e.g., 10mg")
                    frequency = st.text_input("Frequency:", placeholder="e.g., Once daily")
                    start_date = st.date_input("Start Date:", value=date.today())
                    end_date = st.date_input("End Date (leave blank if current):", value=None)
                    prescribing_doctor = st.text_input("Prescribing Doctor:", placeholder="e.g., Dr. Smith")
                    notes = st.text_area("Notes:")
                    
                    submitted = st.form_submit_button("➕ Add Medication", type="primary")
                    if submitted:
                        if medication_name:
                            success, msg = db.add_medication(
                                st.session_state.selected_patient,
                                medication_name,
                                dosage if dosage else None,
                                frequency if frequency else None,
                                str(start_date),
                                str(end_date) if end_date else None,
                                prescribing_doctor if prescribing_doctor else None,
                                notes if notes else None
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("❌ Medication name is required!")
            
            with col2:
                st.markdown("#### Current & Past Medications")
                medications_df = db.get_medications(st.session_state.selected_patient)
                if not medications_df.empty:
                    st.dataframe(medications_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No medications recorded yet.")
        
        # TAB 4: Vaccinations
        with tab4:
            st.subheader("Vaccinations")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Vaccination")
                with st.form("add_vaccination", clear_on_submit=True):
                    vaccine_name = st.text_input("Vaccine Name*:", placeholder="e.g., COVID-19 Booster")
                    administration_date = st.date_input("Administration Date:", value=date.today())
                    next_due_date = st.date_input("Next Due Date (if applicable):", value=None)
                    lot_number = st.text_input("Lot Number:", placeholder="e.g., LOT12345")
                    administered_by = st.text_input("Administered By:", placeholder="e.g., CVS Pharmacy")
                    
                    submitted = st.form_submit_button("➕ Add Vaccination", type="primary")
                    if submitted:
                        if vaccine_name:
                            success, msg = db.add_vaccination(
                                st.session_state.selected_patient,
                                vaccine_name,
                                str(administration_date),
                                str(next_due_date) if next_due_date else None,
                                lot_number if lot_number else None,
                                administered_by if administered_by else None
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("❌ Vaccine name is required!")
            
            with col2:
                st.markdown("#### Immunization History")
                vaccinations_df = db.get_vaccinations(st.session_state.selected_patient)
                if not vaccinations_df.empty:
                    st.dataframe(vaccinations_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No vaccinations recorded yet.")
        
        # TAB 5: Insurance
        with tab5:
            st.subheader("Insurance")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Insurance Policy")
                with st.form("add_insurance", clear_on_submit=True):
                    provider_name = st.text_input("Provider Name*:", placeholder="e.g., Blue Cross Blue Shield")
                    policy_number = st.text_input("Policy Number*:", placeholder="e.g., BCBS123456789")
                    group_number = st.text_input("Group Number:", placeholder="e.g., GRP987654")
                    effective_date = st.date_input("Effective Date:", value=None)
                    expiration_date = st.date_input("Expiration Date:", value=None)
                    is_active = st.checkbox("Currently Active", value=True)
                    
                    submitted = st.form_submit_button("➕ Add Insurance", type="primary")
                    if submitted:
                        if provider_name and policy_number:
                            success, msg = db.add_insurance(
                                st.session_state.selected_patient,
                                provider_name,
                                policy_number,
                                group_number if group_number else None,
                                str(effective_date) if effective_date else None,
                                str(expiration_date) if expiration_date else None,
                                is_active
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("❌ Provider name and policy number are required!")
            
            with col2:
                st.markdown("#### Insurance Policies")
                insurance_df = db.get_insurance(st.session_state.selected_patient)
                if not insurance_df.empty:
                    st.dataframe(insurance_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No insurance policies recorded yet.")
        
        # TAB 6: Emergency Contacts
        with tab6:
            st.subheader("Emergency Contacts")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Emergency Contact")
                with st.form("add_contact", clear_on_submit=True):
                    contact_name = st.text_input("Contact Name*:", placeholder="e.g., Jane Barber")
                    relationship = st.selectbox("Relationship:", ["", "Spouse", "Parent", "Sibling", "Child", "Friend", "Other"])
                    phone_primary = st.text_input("Primary Phone*:", placeholder="e.g., 214-555-0123")
                    phone_secondary = st.text_input("Secondary Phone:", placeholder="e.g., 214-555-0124")
                    email = st.text_input("Email:", placeholder="e.g., contact@email.com")
                    priority_order = st.number_input("Priority Order (1-10):", min_value=1, max_value=10, value=1)
                    
                    submitted = st.form_submit_button("➕ Add Contact", type="primary")
                    if submitted:
                        if contact_name and phone_primary:
                            success, msg = db.add_emergency_contact(
                                st.session_state.selected_patient,
                                contact_name,
                                relationship if relationship else None,
                                phone_primary,
                                phone_secondary if phone_secondary else None,
                                email if email else None,
                                priority_order
                            )
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("❌ Contact name and primary phone are required!")
            
            with col2:
                st.markdown("#### Emergency Contacts List")
                contacts_df = db.get_emergency_contacts(st.session_state.selected_patient)
                if not contacts_df.empty:
                    st.dataframe(contacts_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No emergency contacts recorded yet.")
    
    # Clear selection button
    st.markdown("---")
    if st.button("🔄 Clear Patient Selection"):
        st.session_state.selected_patient = None
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 Medical Info Manager")
    st.info("""
    Manage comprehensive health records for patients.
    
    **Features:**
    - Medical conditions tracking
    - Allergy management
    - Medication history
    - Vaccination records
    - Insurance policies
    - Emergency contacts
    """)
    
    if st.session_state.selected_patient:
        st.success(f"✅ Patient Selected: ID {st.session_state.selected_patient}")
    else:
        st.warning("⚠️ No patient selected")
