"""
Database Connection Helper
License to Live: MIAS - Python/Streamlit Version
Handles all database operations for the MIAS system
"""

import pymysql
import pandas as pd
from typing import Dict, List, Optional, Tuple
import streamlit as st

# Database configuration
DB_CONFIG = {
    'host': 'mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'License2Live',
    'database': 'mias_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


@st.cache_resource
def get_connection():
    """Get database connection (cached by Streamlit)"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None


def execute_query(query: str, params: Optional[Tuple] = None, fetch: bool = True):
    """
    Execute a SQL query with automatic reconnection
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (True for SELECT, False for INSERT/UPDATE/DELETE)
        
    Returns:
        Query results (if fetch=True) or number of affected rows
    """
    connection = get_connection()
    if not connection:
        return None
    
    try:
        # Test if connection is alive
        connection.ping(reconnect=True)
        
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
                
    except pymysql.Error as e:
        # Clear cache and try to reconnect once
        st.cache_resource.clear()
        try:
            connection = pymysql.connect(**DB_CONFIG)
            with connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                else:
                    connection.commit()
                    return cursor.rowcount
        except Exception as retry_error:
            st.error(f"Query error: {str(retry_error)}")
            return None
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return None


def query_to_dataframe(query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
    """Execute query and return results as DataFrame"""
    results = execute_query(query, params, fetch=True)
    if results:
        return pd.DataFrame(results)
    return pd.DataFrame()


# ==================== PATIENT OPERATIONS ====================

def search_patients(search_term: str = "") -> pd.DataFrame:
    """Search for patients"""
    if not search_term:
        query = """
            SELECT patient_id, license_number, first_name, last_name, 
                   date_of_birth, city, state 
            FROM Patients 
            ORDER BY last_name, first_name 
            LIMIT 50
        """
        return query_to_dataframe(query)
    else:
        query = """
            SELECT patient_id, license_number, first_name, last_name, 
                   date_of_birth, city, state 
            FROM Patients 
            WHERE license_number LIKE %s 
               OR first_name LIKE %s 
               OR last_name LIKE %s
            ORDER BY last_name, first_name
        """
        search_pattern = f"%{search_term}%"
        return query_to_dataframe(query, (search_pattern, search_pattern, search_pattern))


def get_patient_details(patient_id: int) -> Optional[Dict]:
    """Get detailed patient information"""
    query = "SELECT * FROM Patients WHERE patient_id = %s"
    results = execute_query(query, (patient_id,))
    return results[0] if results else None


def license_exists(license_number: str) -> bool:
    """Check if license number already exists"""
    query = "SELECT COUNT(*) as count FROM Patients WHERE license_number = %s"
    result = execute_query(query, (license_number,))
    return result[0]['count'] > 0 if result else False


def insert_patient(patient_data: Dict) -> Tuple[bool, str]:
    """Insert new patient into database"""
    query = """
        INSERT INTO Patients 
        (license_number, first_name, last_name, date_of_birth, address, 
         city, state, zip_code, phone, email, blood_type, pin)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    params = (
        patient_data.get('license_number'),
        patient_data.get('first_name'),
        patient_data.get('last_name'),
        patient_data.get('date_of_birth'),
        patient_data.get('address'),
        patient_data.get('city'),
        patient_data.get('state'),
        patient_data.get('zip_code'),
        patient_data.get('phone'),
        patient_data.get('email'),
        patient_data.get('blood_type'),
        patient_data.get('pin')  # Added PIN
    )
    
    try:
        result = execute_query(query, params, fetch=False)
        if result and result > 0:
            return True, "Patient registered successfully!"
        return False, "Failed to register patient"
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== MEDICAL CONDITIONS ====================

def get_conditions(patient_id: int) -> pd.DataFrame:
    """Get medical conditions for a patient"""
    query = """
        SELECT * FROM Medical_Conditions 
        WHERE patient_id = %s 
        ORDER BY diagnosis_date DESC
    """
    return query_to_dataframe(query, (patient_id,))


def add_condition(patient_id: int, condition_name: str, diagnosis_date: Optional[str], 
                 severity: Optional[str], notes: Optional[str]) -> Tuple[bool, str]:
    """Add medical condition"""
    query = """
        INSERT INTO Medical_Conditions 
        (patient_id, condition_name, diagnosis_date, severity, notes)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        result = execute_query(query, (patient_id, condition_name, diagnosis_date, 
                                      severity, notes), fetch=False)
        return (True, "Condition added successfully") if result else (False, "Failed to add condition")
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== ALLERGIES ====================

def get_allergies(patient_id: int) -> pd.DataFrame:
    """Get allergies for a patient"""
    query = "SELECT * FROM Allergies WHERE patient_id = %s"
    return query_to_dataframe(query, (patient_id,))


def add_allergy(patient_id: int, allergen: str, allergy_type: Optional[str] = None,
               severity: Optional[str] = None, reaction: Optional[str] = None) -> Tuple[bool, str]:
    """Add allergy"""
    query = """
        INSERT INTO Allergies 
        (patient_id, allergen, allergy_type, reaction, severity)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        result = execute_query(query, (patient_id, allergen, allergy_type, 
                                      reaction, severity), fetch=False)
        return (True, "Allergy added successfully") if result else (False, "Failed to add allergy")
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== MEDICATIONS ====================

def get_medications(patient_id: int) -> pd.DataFrame:
    """Get medications for a patient"""
    query = """
        SELECT * FROM Medications 
        WHERE patient_id = %s 
        ORDER BY start_date DESC
    """
    return query_to_dataframe(query, (patient_id,))


def add_medication(patient_id: int, medication_name: str, dosage: Optional[str] = None,
                  frequency: Optional[str] = None, prescribing_doctor: Optional[str] = None,
                  start_date: Optional[str] = None, end_date: Optional[str] = None,
                  notes: Optional[str] = None) -> Tuple[bool, str]:
    """Add medication - simplified version for patient portal"""
    from datetime import datetime
    
    # If no start_date provided, use today
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    query = """
        INSERT INTO Medications 
        (patient_id, medication_name, dosage, frequency, start_date, 
         end_date, prescribing_doctor, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        result = execute_query(query, (patient_id, medication_name, dosage, frequency,
                                      start_date, end_date, prescribing_doctor, notes), 
                              fetch=False)
        return (True, "Medication added successfully") if result else (False, "Failed to add medication")
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== VACCINATIONS ====================

def get_vaccinations(patient_id: int) -> pd.DataFrame:
    """Get vaccinations for a patient"""
    query = """
        SELECT * FROM Vaccinations 
        WHERE patient_id = %s 
        ORDER BY administration_date DESC
    """
    return query_to_dataframe(query, (patient_id,))


def add_vaccination(patient_id: int, vaccine_name: str, administration_date: str,
                   next_due_date: Optional[str], lot_number: Optional[str],
                   administered_by: Optional[str]) -> Tuple[bool, str]:
    """Add vaccination"""
    query = """
        INSERT INTO Vaccinations 
        (patient_id, vaccine_name, administration_date, next_due_date, 
         lot_number, administered_by)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        result = execute_query(query, (patient_id, vaccine_name, administration_date,
                                      next_due_date, lot_number, administered_by), 
                              fetch=False)
        return (True, "Vaccination added successfully") if result else (False, "Failed to add vaccination")
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== INSURANCE ====================

def get_insurance(patient_id: int) -> pd.DataFrame:
    """Get insurance policies for a patient"""
    query = """
        SELECT * FROM Insurance 
        WHERE patient_id = %s 
        ORDER BY is_active DESC, effective_date DESC
    """
    return query_to_dataframe(query, (patient_id,))


def add_insurance(patient_id: int, provider_name: str, policy_number: str,
                 group_number: Optional[str], effective_date: Optional[str],
                 expiration_date: Optional[str], is_active: bool) -> Tuple[bool, str]:
    """Add insurance policy"""
    query = """
        INSERT INTO Insurance 
        (patient_id, provider_name, policy_number, group_number, 
         effective_date, expiration_date, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        result = execute_query(query, (patient_id, provider_name, policy_number,
                                      group_number, effective_date, expiration_date,
                                      1 if is_active else 0), fetch=False)
        return (True, "Insurance added successfully") if result else (False, "Failed to add insurance")
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== EMERGENCY CONTACTS ====================

def get_emergency_contacts(patient_id: int) -> pd.DataFrame:
    """Get emergency contacts for a patient"""
    query = """
        SELECT * FROM Emergency_Contacts 
        WHERE patient_id = %s 
        ORDER BY priority_order
    """
    return query_to_dataframe(query, (patient_id,))


def add_emergency_contact(patient_id: int, contact_name: str, relationship: Optional[str],
                         phone_primary: str, phone_secondary: Optional[str],
                         email: Optional[str], priority_order: Optional[int]) -> Tuple[bool, str]:
    """Add emergency contact"""
    query = """
        INSERT INTO Emergency_Contacts 
        (patient_id, contact_name, relationship, phone_primary, 
         phone_secondary, email, priority_order)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        result = execute_query(query, (patient_id, contact_name, relationship,
                                      phone_primary, phone_secondary, email,
                                      priority_order), fetch=False)
        return (True, "Emergency contact added successfully") if result else (False, "Failed to add contact")
    except Exception as e:
        return False, f"Error: {str(e)}"


# ==================== ANALYTICS ====================

def get_summary_stats() -> Dict:
    """Get system summary statistics"""
    queries = {
        'total_patients': "SELECT COUNT(*) as count FROM Patients",
        'total_conditions': "SELECT COUNT(*) as count FROM Medical_Conditions",
        'total_allergies': "SELECT COUNT(*) as count FROM Allergies",
        'active_medications': "SELECT COUNT(*) as count FROM Medications WHERE end_date IS NULL",
        'total_vaccinations': "SELECT COUNT(*) as count FROM Vaccinations",
        'active_insurance': "SELECT COUNT(*) as count FROM Insurance WHERE is_active = TRUE",
        'emergency_contacts': "SELECT COUNT(*) as count FROM Emergency_Contacts",
        'avg_age': "SELECT ROUND(AVG(TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())), 1) as avg_age FROM Patients"
    }
    
    stats = {}
    for key, query in queries.items():
        result = execute_query(query)
        if result:
            stats[key] = result[0].get('count', result[0].get('avg_age', 0))
        else:
            stats[key] = 0
    
    return stats


def get_vaccination_data() -> pd.DataFrame:
    """Get vaccination coverage statistics"""
    query = """
        SELECT 
            vaccine_name,
            COUNT(DISTINCT patient_id) as patients_vaccinated,
            COUNT(vaccination_id) as total_doses,
            MIN(administration_date) as first_dose_date,
            MAX(administration_date) as last_dose_date
        FROM Vaccinations
        GROUP BY vaccine_name
        ORDER BY patients_vaccinated DESC
    """
    return query_to_dataframe(query)


def get_patient_demographics() -> pd.DataFrame:
    """Get patient demographics"""
    query = """
        SELECT 
            patient_id,
            TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) as age,
            state,
            blood_type
        FROM Patients
    """
    return query_to_dataframe(query)


def get_medication_stats() -> pd.DataFrame:
    """Get medication statistics"""
    query = """
        SELECT 
            medication_name,
            COUNT(DISTINCT patient_id) as patient_count,
            COUNT(medication_id) as prescription_count
        FROM Medications
        GROUP BY medication_name
        ORDER BY patient_count DESC
        LIMIT 10
    """
    return query_to_dataframe(query)


def get_allergy_stats() -> pd.DataFrame:
    """Get allergy severity distribution"""
    query = """
        SELECT 
            severity,
            allergy_type,
            COUNT(*) as count
        FROM Allergies
        WHERE severity IS NOT NULL
        GROUP BY severity, allergy_type
        ORDER BY 
            FIELD(severity, 'Life-threatening', 'Severe', 'Moderate', 'Mild'),
            count DESC
    """
    return query_to_dataframe(query)


def get_state_distribution() -> pd.DataFrame:
    """Get geographic distribution"""
    query = """
        SELECT 
            state,
            COUNT(*) as patient_count
        FROM Patients
        WHERE state IS NOT NULL AND state != ''
        GROUP BY state
        ORDER BY patient_count DESC
    """
    return query_to_dataframe(query)


def get_blood_type_distribution() -> pd.DataFrame:
    """Get blood type distribution"""
    query = """
        SELECT 
            blood_type,
            COUNT(*) as count
        FROM Patients
        WHERE blood_type IS NOT NULL AND blood_type != ''
        GROUP BY blood_type
        ORDER BY count DESC
    """
    return query_to_dataframe(query)


# ============================================================================
# DATABASE MANAGEMENT FUNCTIONS
# ============================================================================

def get_all_patients() -> List[Dict]:
    """Get all patients from database"""
    query = """
        SELECT 
            patient_id,
            license_number,
            first_name,
            last_name,
            date_of_birth,
            address,
            city,
            state,
            zip_code,
            phone,
            email,
            blood_type
        FROM Patients
        ORDER BY last_name, first_name
    """
    results = execute_query(query, fetch=True)
    return results if results else []


def search_patients_by_license(license_number: str) -> List[Dict]:
    """Search patients by license number"""
    query = """
        SELECT 
            patient_id,
            license_number,
            first_name,
            last_name,
            date_of_birth,
            address,
            city,
            state,
            zip_code,
            phone,
            email,
            blood_type
        FROM Patients
        WHERE license_number LIKE %s
        ORDER BY last_name, first_name
    """
    results = execute_query(query, (f"%{license_number}%",), fetch=True)
    return results if results else []


def search_patients_by_name(search_term: str, name_type: str = 'first') -> List[Dict]:
    """
    Search patients by name
    
    Args:
        search_term: Name to search for
        name_type: 'first' or 'last'
    """
    field = 'first_name' if name_type == 'first' else 'last_name'
    query = f"""
        SELECT 
            patient_id,
            license_number,
            first_name,
            last_name,
            date_of_birth,
            address,
            city,
            state,
            zip_code,
            phone,
            email,
            blood_type
        FROM Patients
        WHERE {field} LIKE %s
        ORDER BY last_name, first_name
    """
    results = execute_query(query, (f"%{search_term}%",), fetch=True)
    return results if results else []


def search_patients_all_fields(search_term: str) -> List[Dict]:
    """Search patients across all name and license fields"""
    query = """
        SELECT 
            patient_id,
            license_number,
            first_name,
            last_name,
            date_of_birth,
            address,
            city,
            state,
            zip_code,
            phone,
            email,
            blood_type
        FROM Patients
        WHERE 
            first_name LIKE %s OR
            last_name LIKE %s OR
            license_number LIKE %s
        ORDER BY last_name, first_name
    """
    search_pattern = f"%{search_term}%"
    results = execute_query(query, (search_pattern, search_pattern, search_pattern), fetch=True)
    return results if results else []


def delete_patient(patient_id: int) -> Tuple[bool, str]:
    """
    Delete a patient and all associated records
    
    Args:
        patient_id: ID of patient to delete
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        connection = get_connection()
        if not connection:
            return False, "Database connection failed"
        
        with connection.cursor() as cursor:
            try:
                # Get patient info for confirmation message
                cursor.execute("SELECT first_name, last_name, license_number FROM Patients WHERE patient_id = %s", (patient_id,))
                patient = cursor.fetchone()
                
                if not patient:
                    return False, f"Patient ID {patient_id} not found"
                
                patient_name = f"{patient['first_name']} {patient['last_name']}"
                license_num = patient['license_number']
                
                # Temporarily disable foreign key checks to allow deletion
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                
                # Delete related records - wrapped in try/except to handle missing tables gracefully
                tables_to_clean = [
                    "Medical_Conditions",
                    "Allergies", 
                    "Medications",
                    "vaccination_history",
                    "emergency_contacts",
                    "Insurance",
                    "Provider_Access",
                    "Access_Log",
                    "medical_profiles",
                    "Vaccinations",
                    "Healthcare_Providers",
                    "authorized_providers",
                    "driver_licenses",
                    "addresses"
                ]
                
                for table in tables_to_clean:
                    try:
                        cursor.execute(f"DELETE FROM {table} WHERE patient_id = %s", (patient_id,))
                    except Exception as table_error:
                        # Table might not exist or might use different column name
                        pass
                
                # Finally, delete the patient record itself
                cursor.execute("DELETE FROM Patients WHERE patient_id = %s", (patient_id,))
                affected_rows = cursor.rowcount
                
                # Re-enable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                
                # Commit transaction
                connection.commit()
                
                if affected_rows > 0:
                    return True, f"Successfully deleted patient: {patient_name} (License: {license_num})"
                else:
                    return False, "Patient record not found or already deleted"
                
            except Exception as e:
                # Make sure to re-enable foreign key checks even on error
                try:
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                except:
                    pass
                # Rollback on error
                connection.rollback()
                return False, f"Error during deletion: {str(e)}"
                
    except Exception as e:
        return False, f"Database error: {str(e)}"


# ============================================================================
# PATIENT PORTAL AUTHENTICATION FUNCTIONS
# ============================================================================

def authenticate_patient(license_number: str, pin: str) -> Tuple[bool, Optional[int], str]:
    """
    Authenticate patient using license number and PIN
    
    Args:
        license_number: Patient's driver's license number
        pin: Patient's 4-digit PIN
        
    Returns:
        Tuple of (success: bool, patient_id: int or None, message: str)
    """
    try:
        query = """
            SELECT patient_id, first_name, last_name, pin
            FROM Patients
            WHERE license_number = %s
        """
        results = execute_query(query, (license_number,))
        
        if not results or len(results) == 0:
            return False, None, "License number not found"
        
        patient = results[0]
        
        # Check PIN
        if patient['pin'] == pin:
            # Update last login time
            update_query = """
                UPDATE Patients 
                SET last_login = NOW()
                WHERE patient_id = %s
            """
            execute_query(update_query, (patient['patient_id'],), fetch=False)
            
            return True, patient['patient_id'], f"Welcome, {patient['first_name']}!"
        else:
            return False, None, "Incorrect PIN"
            
    except Exception as e:
        return False, None, f"Authentication error: {str(e)}"


def reset_patient_pin(patient_id: int, new_pin: str) -> Tuple[bool, str]:
    """
    Reset patient's PIN (admin function)
    
    Args:
        patient_id: Patient's ID
        new_pin: New 4-digit PIN
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Validate PIN format
        if not new_pin.isdigit() or len(new_pin) != 4:
            return False, "PIN must be exactly 4 digits"
        
        query = """
            UPDATE Patients
            SET pin = %s
            WHERE patient_id = %s
        """
        result = execute_query(query, (new_pin, patient_id), fetch=False)
        
        if result and result > 0:
            return True, "PIN reset successfully"
        return False, "Patient not found or PIN not updated"
        
    except Exception as e:
        return False, f"Error resetting PIN: {str(e)}"


def get_patient_by_id(patient_id: int) -> Optional[Dict]:
    """
    Get complete patient information by patient_id
    
    Args:
        patient_id: Patient's ID
        
    Returns:
        Dictionary with patient data or None
    """
    query = """
        SELECT 
            patient_id, license_number, first_name, last_name,
            date_of_birth, address, city, state, zip_code,
            phone, email, blood_type, last_login
        FROM Patients
        WHERE patient_id = %s
    """
    results = execute_query(query, (patient_id,))
    return results[0] if results else None


def update_patient_medical_info(patient_id: int, field: str, value: str) -> Tuple[bool, str]:
    """
    Update patient's medical information
    Only allows updating medical-related fields, not personal identity info
    
    Args:
        patient_id: Patient's ID
        field: Field name to update (phone, email, blood_type)
        value: New value
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Whitelist of fields patients can update
    allowed_fields = ['phone', 'email', 'blood_type']
    
    if field not in allowed_fields:
        return False, f"Field '{field}' cannot be updated by patients"
    
    try:
        query = f"""
            UPDATE Patients
            SET {field} = %s
            WHERE patient_id = %s
        """
        result = execute_query(query, (value, patient_id), fetch=False)
        
        if result and result > 0:
            return True, f"{field.replace('_', ' ').title()} updated successfully"
        return False, "Update failed"
        
    except Exception as e:
        return False, f"Error updating {field}: {str(e)}"


# ============================================================================
# EMERGENCY QR CODE ACCESS FUNCTIONS
# ============================================================================

def save_emergency_token(patient_id: int, emergency_token: str) -> Tuple[bool, str]:
    """
    Save emergency access token for a patient
    
    Args:
        patient_id: Patient's ID
        emergency_token: Unique emergency access token
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        query = """
            UPDATE Patients
            SET emergency_token = %s
            WHERE patient_id = %s
        """
        result = execute_query(query, (emergency_token, patient_id), fetch=False)
        
        if result and result > 0:
            return True, "Emergency token saved successfully"
        return False, "Failed to save emergency token"
        
    except Exception as e:
        return False, f"Error saving emergency token: {str(e)}"


def get_patient_by_emergency_token(emergency_token: str) -> Optional[Dict]:
    """
    Get patient information using emergency access token
    
    Args:
        emergency_token: Emergency access token from QR code
        
    Returns:
        Dictionary with patient data or None
    """
    query = """
        SELECT *
        FROM Patients
        WHERE emergency_token = %s
    """
    results = execute_query(query, (emergency_token,))
    return results[0] if results else None


def log_emergency_access(patient_id: int, emergency_token: str) -> Tuple[bool, str]:
    """
    Log emergency access to patient record
    
    Args:
        patient_id: Patient's ID
        emergency_token: Emergency access token used
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        from datetime import datetime
        
        # Update last_emergency_access timestamp
        update_query = """
            UPDATE Patients
            SET last_emergency_access = NOW()
            WHERE patient_id = %s
        """
        execute_query(update_query, (patient_id,), fetch=False)
        
        # Log in Access_Log table if it exists
        try:
            log_query = """
                INSERT INTO Access_Log 
                (patient_id, access_type, access_time, notes)
                VALUES (%s, %s, NOW(), %s)
            """
            execute_query(log_query, (
                patient_id, 
                'emergency_qr_access',
                f'Emergency QR code scanned - Token: {emergency_token[:16]}...'
            ), fetch=False)
        except:
            # Access_Log table might not exist, continue anyway
            pass
        
        return True, "Emergency access logged"
        
    except Exception as e:
        return False, f"Error logging emergency access: {str(e)}"


def calculate_age(date_of_birth: str) -> int:
    """
    Calculate age from date of birth
    
    Args:
        date_of_birth: Date of birth as string (YYYY-MM-DD)
        
    Returns:
        Age in years
    """
    try:
        from datetime import datetime
        dob = datetime.strptime(str(date_of_birth), '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return 0


def get_patient_emergency_summary(patient_id: int) -> Dict:
    """
    Get complete emergency summary for a patient
    Includes all critical information needed in emergency situations
    
    Args:
        patient_id: Patient's ID
        
    Returns:
        Dictionary with emergency summary data
    """
    summary = {
        'patient': get_patient_by_id(patient_id),
        'allergies': get_allergies(patient_id),
        'medications': get_medications(patient_id),
        'conditions': get_conditions(patient_id),
        'emergency_contacts': get_emergency_contacts(patient_id)
    }
    
    # ============================================================================
# EMERGENCY QR CODE ACCESS FUNCTIONS
# ============================================================================

def save_emergency_token(patient_id: int, emergency_token: str) -> Tuple[bool, str]:
    """
    Save emergency access token for a patient
    
    Args:
        patient_id: Patient's ID
        emergency_token: Unique emergency access token
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        query = """
            UPDATE Patients
            SET emergency_token = %s
            WHERE patient_id = %s
        """
        result = execute_query(query, (emergency_token, patient_id), fetch=False)
        
        if result and result > 0:
            return True, "Emergency token saved successfully"
        return False, "Failed to save emergency token"
        
    except Exception as e:
        return False, f"Error saving emergency token: {str(e)}"


def get_patient_by_emergency_token(emergency_token: str) -> Optional[Dict]:
    """
    Get patient information using emergency access token
    
    Args:
        emergency_token: Emergency access token from QR code
        
    Returns:
        Dictionary with patient data or None
    """
    query = """
        SELECT *
        FROM Patients
        WHERE emergency_token = %s
    """
    results = execute_query(query, (emergency_token,))
    return results[0] if results else None


def log_emergency_access(patient_id: int, emergency_token: str) -> Tuple[bool, str]:
    """
    Log emergency access to patient record
    
    Args:
        patient_id: Patient's ID
        emergency_token: Emergency access token used
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        from datetime import datetime
        
        # Update last_emergency_access timestamp
        update_query = """
            UPDATE Patients
            SET last_emergency_access = NOW()
            WHERE patient_id = %s
        """
        execute_query(update_query, (patient_id,), fetch=False)
        
        # Log in Access_Log table if it exists
        try:
            log_query = """
                INSERT INTO Access_Log 
                (patient_id, access_type, access_time, notes)
                VALUES (%s, %s, NOW(), %s)
            """
            execute_query(log_query, (
                patient_id, 
                'emergency_qr_access',
                f'Emergency QR code scanned - Token: {emergency_token[:16]}...'
            ), fetch=False)
        except:
            # Access_Log table might not exist, continue anyway
            pass
        
        return True, "Emergency access logged"
        
    except Exception as e:
        return False, f"Error logging emergency access: {str(e)}"
    
    return summary
