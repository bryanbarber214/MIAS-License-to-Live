"""
Emergency Access API
Simple API endpoint for HTML emergency page
Returns patient data as JSON
"""

import streamlit as st
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db

# Set page config
st.set_page_config(
    page_title="MIAS Emergency API",
    page_icon="🚨",
)

# Get token from query parameters
query_params = st.query_params
token = query_params.get("token", None)

if not token:
    # Return error JSON
    response = {
        "error": "No emergency access token provided",
        "success": False
    }
else:
    try:
        # Fetch patient data
        patient_data = db.get_patient_by_emergency_token(token)
        
        if not patient_data:
            response = {
                "error": "Invalid or expired emergency access token",
                "success": False
            }
        else:
            # Log the access
            db.log_emergency_access(patient_data['patient_id'], token)
            
            # Get additional data
            allergies = db.get_allergies(patient_data['patient_id'])
            medications = db.get_medications(patient_data['patient_id'])
            conditions = db.get_conditions(patient_data['patient_id'])
            contacts = db.get_emergency_contacts(patient_data['patient_id'])
            
            # Convert DataFrames to list of dicts
            allergies_list = allergies.to_dict('records') if not allergies.empty else []
            medications_list = medications.to_dict('records') if not medications.empty else []
            conditions_list = conditions.to_dict('records') if not conditions.empty else []
            contacts_list = contacts.to_dict('records') if not contacts.empty else []
            
            # Build response
            response = {
                "success": True,
                "patient": {
                    "patient_id": patient_data['patient_id'],
                    "first_name": patient_data['first_name'],
                    "last_name": patient_data['last_name'],
                    "date_of_birth": str(patient_data['date_of_birth']),
                    "license_number": patient_data['license_number'],
                    "blood_type": patient_data.get('blood_type', 'Unknown'),
                    "updated_at": str(patient_data.get('updated_at', ''))
                },
                "allergies": allergies_list,
                "medications": medications_list,
                "conditions": conditions_list,
                "contacts": contacts_list
            }
    except Exception as e:
        response = {
            "error": f"Server error: {str(e)}",
            "success": False
        }

# Return JSON response
st.write(json.dumps(response, indent=2, default=str))

# Hide Streamlit UI elements
st.markdown("""
<style>
    header {visibility: hidden;}
    .stApp {background-color: #1e1e1e;}
    .stMarkdown {color: #00ff00; font-family: monospace;}
</style>
""", unsafe_allow_html=True)
