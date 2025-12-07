"""
Patient QR Codes
License to Live: MIAS - Python/Streamlit Version
View and download patient emergency QR codes
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from admin_auth import admin_login_page, show_logout_button
import qr_generator

# Page configuration
st.set_page_config(
    page_title="Patient QR Codes - MIAS",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AUTHENTICATION CHECK
if not admin_login_page():
    st.stop()

# Show logout button
show_logout_button()

# Custom CSS
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .patient-card {
        background: white;
        border: 2px solid #e74c3c;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .qr-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="main-title">
    <h1>📱 Patient QR Codes</h1>
    <h3>View & Download Emergency Access QR Codes</h3>
</div>
""", unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <strong>ℹ️ About Emergency QR Codes:</strong><br>
    Each patient has a unique QR code that provides instant access to their critical medical information in emergencies.
    EMTs and medical professionals can scan the code to view allergies, medications, blood type, and emergency contacts.
</div>
""", unsafe_allow_html=True)

# Search section
st.markdown("### 🔍 Find Patient")

col1, col2 = st.columns([2, 1])

with col1:
    search_method = st.radio(
        "Search by:",
        ["Patient Name", "Patient ID", "License Number"],
        horizontal=True
    )

with col2:
    st.write("")  # Spacer

# Search input
if search_method == "Patient Name":
    search_query = st.text_input("Enter patient name (first or last):", placeholder="e.g., John Smith")
elif search_method == "Patient ID":
    search_query = st.text_input("Enter patient ID:", placeholder="e.g., 123")
else:  # License Number
    search_query = st.text_input("Enter license number:", placeholder="e.g., TX12345678")

search_button = st.button("🔍 Search", type="primary")

# Search and display results
if search_button and search_query:
    with st.spinner("Searching for patient..."):
        
        # Build query based on search method
        if search_method == "Patient Name":
            query = """
                SELECT patient_id, first_name, last_name, date_of_birth, blood_type, 
                       license_number, emergency_token
                FROM Patients 
                WHERE LOWER(first_name) LIKE LOWER(%s) 
                   OR LOWER(last_name) LIKE LOWER(%s)
                ORDER BY last_name, first_name
            """
            search_pattern = f"%{search_query}%"
            patients = db.execute_query(query, (search_pattern, search_pattern), fetch=True)
            
        elif search_method == "Patient ID":
            query = """
                SELECT patient_id, first_name, last_name, date_of_birth, blood_type, 
                       license_number, emergency_token
                FROM Patients 
                WHERE patient_id = %s
            """
            patients = db.execute_query(query, (search_query,), fetch=True)
            
        else:  # License Number
            query = """
                SELECT patient_id, first_name, last_name, date_of_birth, blood_type, 
                       license_number, emergency_token
                FROM Patients 
                WHERE license_number LIKE %s
            """
            search_pattern = f"%{search_query}%"
            patients = db.execute_query(query, (search_pattern,), fetch=True)
        
        if not patients:
            st.warning(f"❌ No patients found matching: {search_query}")
        else:
            st.success(f"✅ Found {len(patients)} patient(s)")
            
            # Display each patient with their QR code
            for patient in patients:
                st.markdown("---")
                
                # Patient info header
                col_a, col_b = st.columns([2, 1])
                
                with col_a:
                    st.markdown(f"""
                    ### {patient['first_name']} {patient['last_name']}
                    **Patient ID:** {patient['patient_id']}  
                    **DOB:** {patient['date_of_birth']}  
                    **Blood Type:** {patient['blood_type'] or 'Not specified'}  
                    **License:** {patient['license_number'][:8]}****
                    """)
                
                with col_b:
                    st.metric("🩸 Blood Type", patient['blood_type'] or 'Unknown')
                
                # Check if patient has emergency token
                if not patient['emergency_token']:
                    st.error("⚠️ This patient does not have an emergency QR code. Please register them again to generate one.")
                    continue
                
                # Generate QR code
                with st.expander("📱 View QR Code", expanded=True):
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("#### Emergency QR Code")
                        
                        # Generate QR code from emergency token
                        qr_image = qr_generator.create_emergency_qr_code(
                            patient_id=patient['patient_id'],
                            emergency_token=patient['emergency_token']
                        )
                        
                        # Convert to RGB mode for Streamlit (fix display issues)
                        if qr_image.mode != 'RGB':
                            qr_image = qr_image.convert('RGB')
                        
                        # Display QR code
                        st.image(qr_image, caption=f"Emergency QR Code for {patient['first_name']} {patient['last_name']}", use_container_width=False)
                        
                        # Download button for QR code
                        qr_bytes = qr_generator.image_to_bytes(qr_image)
                        st.download_button(
                            label="📥 Download QR Code",
                            data=qr_bytes,
                            file_name=f"emergency_qr_{patient['patient_id']}_{patient['last_name']}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.markdown("#### Printable Card")
                        
                        # Generate printable card with QR code
                        patient_data = {
                            'first_name': patient['first_name'],
                            'last_name': patient['last_name'],
                            'date_of_birth': str(patient['date_of_birth']),
                            'blood_type': patient['blood_type']
                        }
                        
                        card_image = qr_generator.create_printable_qr_card(
                            patient_data=patient_data,
                            qr_image=qr_image,
                            emergency_token=patient['emergency_token']
                        )
                        
                        # Convert to RGB mode for Streamlit
                        if card_image.mode != 'RGB':
                            card_image = card_image.convert('RGB')
                        
                        # Display card
                        st.image(card_image, caption="Wallet-sized Emergency Card", use_container_width=True)
                        
                        # Download button for card
                        card_bytes = qr_generator.image_to_bytes(card_image)
                        st.download_button(
                            label="📥 Download Printable Card",
                            data=card_bytes,
                            file_name=f"emergency_card_{patient['patient_id']}_{patient['last_name']}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Emergency URL
                    emergency_url = f"https://bryanbarber214.github.io/MIAS-License-to-Live/emergency_access.html?token={patient['emergency_token']}"
                    
                    st.markdown("---")
                    st.markdown("#### 🔗 Emergency Access URL")
                    st.code(emergency_url, language="text")
                    
                    st.info("""
                    **How to use:**
                    1. Print the card and give it to the patient
                    2. Patient should keep it in their wallet with their license
                    3. In an emergency, medical staff can scan the QR code
                    4. They will instantly see critical medical information
                    """)

# Sidebar instructions
with st.sidebar:
    st.markdown("### 📱 QR Code Viewer")
    
    st.info("""
    **How to use:**
    1. Search for a patient
    2. View their QR code
    3. Download QR code or printable card
    4. Give to patient for emergencies
    """)
    
    st.markdown("### 🎯 Use Cases")
    st.markdown("""
    - Reprint lost QR codes
    - Create replacement cards
    - Share with family members
    - Email QR code to patient
    - Print for medical records
    """)
    
    st.markdown("### 🔒 Security")
    st.success("""
    ✅ Each QR code is unique  
    ✅ Cannot be duplicated  
    ✅ Tied to patient record  
    ✅ Access is logged  
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Print on cardstock for durability
    - Laminate cards for longevity
    - Recommend patients take photo
    - Keep backup in phone wallet
    """)

# Show all patients option
st.markdown("---")
if st.button("📋 Show All Patients"):
    with st.spinner("Loading all patients..."):
        query = """
            SELECT patient_id, first_name, last_name, date_of_birth, blood_type, 
                   CASE WHEN emergency_token IS NOT NULL THEN '✅ Yes' ELSE '❌ No' END as has_qr
            FROM Patients 
            ORDER BY last_name, first_name
            LIMIT 50
        """
        all_patients = db.execute_query(query, fetch=True)
        
        if all_patients:
            import pandas as pd
            df = pd.DataFrame(all_patients)
            df.columns = ['ID', 'First Name', 'Last Name', 'Date of Birth', 'Blood Type', 'Has QR Code']
            
            st.dataframe(df, use_container_width=True, height=400)
            st.caption(f"Showing {len(all_patients)} patients. Use search above to find specific patient QR codes.")
        else:
            st.warning("No patients found in database.")
