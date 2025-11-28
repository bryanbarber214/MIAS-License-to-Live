"""
Database Management Page
License to Live: MIAS - Python/Streamlit Version
View, edit, and delete patient records
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from admin_auth import admin_login_page, show_logout_button

# Page configuration
st.set_page_config(
    page_title="Database Management - MIAS",
    page_icon="🗄️",
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
    
    /* Data table styling */
    .dataframe {
        font-size: 14px !important;
    }
    
    .dataframe th {
        background-color: #1976D2 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        padding: 10px !important;
    }
    
    .dataframe td {
        padding: 8px !important;
        border-bottom: 1px solid #E0E0E0 !important;
    }
    
    /* Action buttons */
    .action-button {
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🗄️ Database Management")
st.markdown("### View, Search, and Manage Patient Records")

# Initialize session state
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None
if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = False
if 'patient_to_delete' not in st.session_state:
    st.session_state.patient_to_delete = None

st.markdown("---")

# Search and Filter Section
st.markdown("### 🔍 Search Patients")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    search_term = st.text_input(
        "Search by Name or License Number:",
        placeholder="Enter name or license number...",
        help="Search for patients by first name, last name, or license number"
    )

with col2:
    search_type = st.selectbox(
        "Search Field:",
        options=["All Fields", "First Name", "Last Name", "License Number"],
        help="Choose which field to search"
    )

with col3:
    st.markdown("&nbsp;")  # Spacing
    st.markdown("&nbsp;")  # Spacing
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

st.markdown("---")

# Get all patients or search results
if search_button and search_term:
    # Search functionality
    if search_type == "License Number":
        patients = db.search_patients_by_license(search_term)
    elif search_type == "First Name":
        patients = db.search_patients_by_name(search_term, 'first')
    elif search_type == "Last Name":
        patients = db.search_patients_by_name(search_term, 'last')
    else:  # All Fields
        patients = db.search_patients_all_fields(search_term)
    
    if patients:
        st.success(f"✅ Found {len(patients)} patient(s)")
    else:
        st.warning("⚠️ No patients found matching your search")
else:
    # Show all patients
    patients = db.get_all_patients()
    st.info(f"📊 Showing all {len(patients)} patients in database")

# Display patients table
if patients:
    st.markdown("### 📋 Patient Records")
    
    # Convert to display format
    import pandas as pd
    
    display_data = []
    for patient in patients:
        display_data.append({
            'ID': patient.get('patient_id', 'N/A'),
            'License #': patient.get('license_number', 'N/A'),
            'First Name': patient.get('first_name', 'N/A'),
            'Last Name': patient.get('last_name', 'N/A'),
            'Date of Birth': patient.get('date_of_birth', 'N/A'),
            'City': patient.get('city', 'N/A'),
            'State': patient.get('state', 'N/A'),
            'Phone': patient.get('phone', 'N/A') if patient.get('phone') else 'Not provided',
            'Email': patient.get('email', 'N/A') if patient.get('email') else 'Not provided'
        })
    
    df = pd.DataFrame(display_data)
    
    # Display dataframe
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Patient Selection for Actions
    st.markdown("### ⚙️ Manage Patient Record")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create selection options
        patient_options = [f"{p.get('patient_id')} - {p.get('first_name')} {p.get('last_name')} (License: {p.get('license_number')})" 
                          for p in patients]
        
        selected_patient_str = st.selectbox(
            "Select a patient to manage:",
            options=patient_options,
            help="Choose a patient to view details or delete"
        )
        
        # Extract patient_id from selection
        if selected_patient_str:
            selected_id = int(selected_patient_str.split(' - ')[0])
            st.session_state.selected_patient = next((p for p in patients if p.get('patient_id') == selected_id), None)
    
    # Show selected patient details
    if st.session_state.selected_patient:
        patient = st.session_state.selected_patient
        
        st.markdown("---")
        st.markdown("### 👤 Patient Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Personal Information:**")
            st.markdown(f"**ID:** {patient.get('patient_id')}")
            st.markdown(f"**Name:** {patient.get('first_name')} {patient.get('last_name')}")
            st.markdown(f"**DOB:** {patient.get('date_of_birth')}")
            st.markdown(f"**Blood Type:** {patient.get('blood_type', 'Not provided')}")
        
        with col2:
            st.markdown("**Contact Information:**")
            st.markdown(f"**Phone:** {patient.get('phone', 'Not provided')}")
            st.markdown(f"**Email:** {patient.get('email', 'Not provided')}")
            st.markdown(f"**Address:** {patient.get('address', 'N/A')}")
            st.markdown(f"**City, State ZIP:** {patient.get('city', '')}, {patient.get('state', '')} {patient.get('zip_code', '')}")
        
        with col3:
            st.markdown("**License Information:**")
            st.markdown(f"**License #:** {patient.get('license_number')}")
            st.markdown(f"**State:** {patient.get('state')}")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🗑️ Delete Patient", type="primary", use_container_width=True):
                st.session_state.show_delete_confirm = True
                st.session_state.patient_to_delete = patient
        
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
        
        # Delete confirmation
        if st.session_state.show_delete_confirm and st.session_state.patient_to_delete:
            st.markdown("---")
            st.warning(f"""
            ⚠️ **CONFIRM DELETION**
            
            Are you sure you want to delete this patient record?
            
            **Patient:** {st.session_state.patient_to_delete.get('first_name')} {st.session_state.patient_to_delete.get('last_name')}  
            **License:** {st.session_state.patient_to_delete.get('license_number')}  
            **Patient ID:** {st.session_state.patient_to_delete.get('patient_id')}
            
            **This action cannot be undone!**
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Yes, Delete Patient", type="primary", use_container_width=True):
                    # Perform deletion
                    success, message = db.delete_patient(st.session_state.patient_to_delete.get('patient_id'))
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state.show_delete_confirm = False
                        st.session_state.patient_to_delete = None
                        st.session_state.selected_patient = None
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Deletion failed: {message}")
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_delete_confirm = False
                    st.session_state.patient_to_delete = None
                    st.rerun()

else:
    st.info("No patients in database. Use Patient Registration to add patients.")

# Sidebar
with st.sidebar:
    st.markdown("### 🗄️ Database Management")
    st.info("""
    This page allows you to manage patient records in the database.
    
    **Features:**
    - View all patients
    - Search by name or license
    - View patient details
    - Delete patient records
    """)
    
    st.markdown("### ⚠️ Important")
    st.warning("""
    **Deleting a patient will:**
    - Remove all patient data
    - Cannot be undone
    - Require confirmation
    """)
    
    st.markdown("### 📊 Database Stats")
    total_patients = len(patients) if patients else 0
    st.metric("Total Patients", total_patients)
