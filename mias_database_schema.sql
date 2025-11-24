-- =====================================================
-- License to Live: Medical Information Access System (MIAS)
-- Database Schema - SQL DDL Script
-- Database: mias_db
-- MySQL 8.0.43
-- =====================================================

-- Use the mias_db database
USE mias_db;

-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS Access_Log;
DROP TABLE IF EXISTS Provider_Access;
DROP TABLE IF EXISTS Healthcare_Providers;
DROP TABLE IF EXISTS Emergency_Contacts;
DROP TABLE IF EXISTS Insurance;
DROP TABLE IF EXISTS Vaccinations;
DROP TABLE IF EXISTS Medications;
DROP TABLE IF EXISTS Allergies;
DROP TABLE IF EXISTS Medical_Conditions;
DROP TABLE IF EXISTS Patients;

-- =====================================================
-- TABLE 1: Patients (Central Entity)
-- =====================================================
CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    license_number VARCHAR(50) UNIQUE NOT NULL COMMENT 'Unique driver license number from 2D barcode',
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    phone VARCHAR(15),
    email VARCHAR(150),
    blood_type VARCHAR(5) COMMENT 'A+, A-, B+, B-, AB+, AB-, O+, O-',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_license_number (license_number),
    INDEX idx_last_name (last_name),
    INDEX idx_dob (date_of_birth)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Central patient table containing driver license and personal identification data';

-- =====================================================
-- TABLE 2: Medical_Conditions
-- =====================================================
CREATE TABLE Medical_Conditions (
    condition_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    condition_name VARCHAR(200) NOT NULL COMMENT 'e.g., Diabetes Type 2, Hypertension',
    diagnosis_date DATE,
    severity VARCHAR(20) COMMENT 'Mild, Moderate, Severe, Critical',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_condition_name (condition_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores chronic medical conditions and diagnoses for each patient';

-- =====================================================
-- TABLE 3: Allergies
-- =====================================================
CREATE TABLE Allergies (
    allergy_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    allergen VARCHAR(150) NOT NULL COMMENT 'e.g., Penicillin, Peanuts, Latex',
    allergy_type VARCHAR(50) COMMENT 'Medication, Food, Environmental, Other',
    reaction VARCHAR(255) COMMENT 'e.g., Anaphylaxis, Hives, Difficulty breathing',
    severity VARCHAR(20) COMMENT 'Mild, Moderate, Severe, Life-threatening',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_allergen (allergen),
    INDEX idx_severity (severity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Records all known allergies including medication, food, and environmental allergies';

-- =====================================================
-- TABLE 4: Medications
-- =====================================================
CREATE TABLE Medications (
    medication_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    medication_name VARCHAR(200) NOT NULL,
    dosage VARCHAR(100) COMMENT 'e.g., 500mg, 10ml',
    frequency VARCHAR(100) COMMENT 'e.g., Twice daily, Every 6 hours',
    start_date DATE NOT NULL,
    end_date DATE COMMENT 'NULL if currently active',
    prescribing_doctor VARCHAR(150),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_medication_name (medication_name),
    INDEX idx_active_medications (patient_id, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks current and historical medications prescribed to patients';

-- =====================================================
-- TABLE 5: Vaccinations
-- =====================================================
CREATE TABLE Vaccinations (
    vaccination_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    vaccine_name VARCHAR(150) NOT NULL COMMENT 'e.g., COVID-19, Influenza, Tetanus',
    administration_date DATE NOT NULL,
    next_due_date DATE COMMENT 'For booster shots',
    lot_number VARCHAR(50),
    administered_by VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_vaccine_name (vaccine_name),
    INDEX idx_administration_date (administration_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Records vaccination history for immunization tracking and compliance';

-- =====================================================
-- TABLE 6: Insurance
-- =====================================================
CREATE TABLE Insurance (
    insurance_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    provider_name VARCHAR(150) NOT NULL,
    policy_number VARCHAR(100) NOT NULL,
    group_number VARCHAR(100),
    effective_date DATE,
    expiration_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_policy_number (policy_number),
    INDEX idx_active_insurance (patient_id, is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores healthcare insurance information for billing and coverage verification';

-- =====================================================
-- TABLE 7: Emergency_Contacts
-- =====================================================
CREATE TABLE Emergency_Contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    contact_name VARCHAR(150) NOT NULL,
    relationship VARCHAR(50) COMMENT 'Spouse, Parent, Sibling, Friend, Other',
    phone_primary VARCHAR(15) NOT NULL,
    phone_secondary VARCHAR(15),
    email VARCHAR(150),
    priority_order INT COMMENT '1=primary, 2=secondary, etc.',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_priority (patient_id, priority_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Maintains emergency contact information for patient notification in critical situations';

-- =====================================================
-- TABLE 8: Healthcare_Providers
-- =====================================================
CREATE TABLE Healthcare_Providers (
    provider_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) COMMENT 'e.g., Cardiologist, Emergency Medicine',
    license_number VARCHAR(50) UNIQUE NOT NULL COMMENT 'Medical license number',
    facility_name VARCHAR(200),
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_license_number (license_number),
    INDEX idx_last_name (last_name),
    INDEX idx_specialty (specialty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Records authorized medical professionals who can access patient data';

-- =====================================================
-- TABLE 9: Provider_Access (Junction Table)
-- =====================================================
CREATE TABLE Provider_Access (
    access_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    provider_id INT NOT NULL,
    granted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_date TIMESTAMP NULL COMMENT 'NULL = currently active',
    access_level VARCHAR(20) DEFAULT 'ReadOnly' COMMENT 'Full, ReadOnly, Emergency',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES Healthcare_Providers(provider_id) ON DELETE CASCADE,
    UNIQUE KEY unique_active_access (patient_id, provider_id, revoked_date),
    INDEX idx_patient_provider (patient_id, provider_id),
    INDEX idx_provider_patient (provider_id, patient_id),
    INDEX idx_active_access (revoked_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Links healthcare providers to patients they are authorized to access (Many-to-Many relationship)';

-- =====================================================
-- TABLE 10: Access_Log (Audit Trail)
-- =====================================================
CREATE TABLE Access_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    provider_id INT,
    access_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_type VARCHAR(50) COMMENT 'View, Update, Create, Delete',
    ip_address VARCHAR(45) COMMENT 'Supports IPv6',
    details TEXT COMMENT 'Description of what was accessed/changed',
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (provider_id) REFERENCES Healthcare_Providers(provider_id) ON DELETE SET NULL,
    INDEX idx_patient_id (patient_id),
    INDEX idx_provider_id (provider_id),
    INDEX idx_timestamp (access_timestamp),
    INDEX idx_action_type (action_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tracks all access to patient records for security, compliance, and audit purposes (HIPAA requirement)';

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View: Active Medications per Patient
CREATE OR REPLACE VIEW Active_Medications_View AS
SELECT 
    p.patient_id,
    p.first_name,
    p.last_name,
    m.medication_name,
    m.dosage,
    m.frequency,
    m.start_date,
    m.prescribing_doctor
FROM Patients p
INNER JOIN Medications m ON p.patient_id = m.patient_id
WHERE m.end_date IS NULL
ORDER BY p.last_name, p.first_name, m.medication_name;

-- View: Patient Summary with Critical Information
CREATE OR REPLACE VIEW Patient_Summary_View AS
SELECT 
    p.patient_id,
    p.license_number,
    p.first_name,
    p.last_name,
    p.date_of_birth,
    p.blood_type,
    p.phone,
    p.email,
    COUNT(DISTINCT mc.condition_id) as condition_count,
    COUNT(DISTINCT a.allergy_id) as allergy_count,
    COUNT(DISTINCT m.medication_id) as active_medication_count,
    COUNT(DISTINCT ec.contact_id) as emergency_contact_count
FROM Patients p
LEFT JOIN Medical_Conditions mc ON p.patient_id = mc.patient_id
LEFT JOIN Allergies a ON p.patient_id = a.patient_id
LEFT JOIN Medications m ON p.patient_id = m.patient_id AND m.end_date IS NULL
LEFT JOIN Emergency_Contacts ec ON p.patient_id = ec.patient_id
GROUP BY p.patient_id;

-- View: Provider Access Summary
CREATE OR REPLACE VIEW Provider_Access_Summary AS
SELECT 
    hp.provider_id,
    hp.first_name,
    hp.last_name,
    hp.specialty,
    hp.facility_name,
    COUNT(DISTINCT pa.patient_id) as total_patients_authorized,
    COUNT(DISTINCT CASE WHEN pa.revoked_date IS NULL THEN pa.patient_id END) as active_patients
FROM Healthcare_Providers hp
LEFT JOIN Provider_Access pa ON hp.provider_id = pa.provider_id
WHERE hp.is_active = TRUE
GROUP BY hp.provider_id;

-- View: Vaccination Coverage Analysis (for analytics requirement)
CREATE OR REPLACE VIEW Vaccination_Coverage_View AS
SELECT 
    v.vaccine_name,
    COUNT(DISTINCT v.patient_id) as patients_vaccinated,
    COUNT(v.vaccination_id) as total_doses_administered,
    MIN(v.administration_date) as first_dose_date,
    MAX(v.administration_date) as last_dose_date
FROM Vaccinations v
GROUP BY v.vaccine_name
ORDER BY patients_vaccinated DESC;

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Procedure: Log Patient Access
DELIMITER //
CREATE PROCEDURE Log_Patient_Access(
    IN p_patient_id INT,
    IN p_provider_id INT,
    IN p_action_type VARCHAR(50),
    IN p_ip_address VARCHAR(45),
    IN p_details TEXT
)
BEGIN
    INSERT INTO Access_Log (patient_id, provider_id, action_type, ip_address, details)
    VALUES (p_patient_id, p_provider_id, p_action_type, p_ip_address, p_details);
END //
DELIMITER ;

-- Procedure: Grant Provider Access
DELIMITER //
CREATE PROCEDURE Grant_Provider_Access(
    IN p_patient_id INT,
    IN p_provider_id INT,
    IN p_access_level VARCHAR(20)
)
BEGIN
    INSERT INTO Provider_Access (patient_id, provider_id, access_level)
    VALUES (p_patient_id, p_provider_id, p_access_level);
    
    -- Log the access grant
    CALL Log_Patient_Access(
        p_patient_id, 
        p_provider_id, 
        'Access Granted', 
        NULL, 
        CONCAT('Provider granted ', p_access_level, ' access')
    );
END //
DELIMITER ;

-- Procedure: Revoke Provider Access
DELIMITER //
CREATE PROCEDURE Revoke_Provider_Access(
    IN p_access_id INT
)
BEGIN
    DECLARE v_patient_id INT;
    DECLARE v_provider_id INT;
    
    -- Get patient and provider IDs before revoking
    SELECT patient_id, provider_id INTO v_patient_id, v_provider_id
    FROM Provider_Access
    WHERE access_id = p_access_id;
    
    -- Update revoked date
    UPDATE Provider_Access
    SET revoked_date = CURRENT_TIMESTAMP
    WHERE access_id = p_access_id;
    
    -- Log the revocation
    CALL Log_Patient_Access(
        v_patient_id, 
        v_provider_id, 
        'Access Revoked', 
        NULL, 
        'Provider access revoked'
    );
END //
DELIMITER ;

-- Procedure: Get Patient Emergency Information
DELIMITER //
CREATE PROCEDURE Get_Emergency_Info(
    IN p_license_number VARCHAR(50)
)
BEGIN
    DECLARE v_patient_id INT;
    
    -- Get patient ID from license number
    SELECT patient_id INTO v_patient_id
    FROM Patients
    WHERE license_number = p_license_number;
    
    -- Return patient basic info
    SELECT * FROM Patients WHERE patient_id = v_patient_id;
    
    -- Return allergies
    SELECT * FROM Allergies WHERE patient_id = v_patient_id;
    
    -- Return active medications
    SELECT * FROM Medications WHERE patient_id = v_patient_id AND end_date IS NULL;
    
    -- Return medical conditions
    SELECT * FROM Medical_Conditions WHERE patient_id = v_patient_id;
    
    -- Return emergency contacts
    SELECT * FROM Emergency_Contacts WHERE patient_id = v_patient_id ORDER BY priority_order;
END //
DELIMITER ;

-- =====================================================
-- SAMPLE DATA INSERTION (Optional - for testing)
-- =====================================================

-- Insert sample patient
INSERT INTO Patients (license_number, first_name, last_name, date_of_birth, address, city, state, zip_code, phone, email, blood_type)
VALUES ('TX12345678', 'John', 'Doe', '1985-06-15', '123 Main St', 'Carrollton', 'TX', '75006', '972-555-0100', 'john.doe@email.com', 'O+');

-- Insert sample provider
INSERT INTO Healthcare_Providers (first_name, last_name, specialty, license_number, facility_name, email, phone)
VALUES ('Jane', 'Smith', 'Emergency Medicine', 'MD987654', 'Carrollton Regional Medical Center', 'jane.smith@hospital.com', '972-555-0200');

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Show all tables
SHOW TABLES;

-- Show table structures
-- DESCRIBE Patients;
-- DESCRIBE Medical_Conditions;
-- DESCRIBE Allergies;
-- DESCRIBE Medications;
-- DESCRIBE Vaccinations;
-- DESCRIBE Insurance;
-- DESCRIBE Emergency_Contacts;
-- DESCRIBE Healthcare_Providers;
-- DESCRIBE Provider_Access;
-- DESCRIBE Access_Log;

-- =====================================================
-- END OF SCHEMA CREATION SCRIPT
-- =====================================================
