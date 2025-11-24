-- =====================================================
-- MIAS Database Verification Script
-- Run this to confirm everything is working
-- =====================================================

USE mias_db;

-- 1. Show all tables
SELECT '=== ALL TABLES ===' as Info;
SHOW TABLES;

-- 2. Verify table structures
SELECT '=== TABLE ROW COUNTS ===' as Info;
SELECT 'Patients' as TableName, COUNT(*) as RowCount FROM Patients
UNION ALL
SELECT 'Medical_Conditions', COUNT(*) FROM Medical_Conditions
UNION ALL
SELECT 'Allergies', COUNT(*) FROM Allergies
UNION ALL
SELECT 'Medications', COUNT(*) FROM Medications
UNION ALL
SELECT 'Vaccinations', COUNT(*) FROM Vaccinations
UNION ALL
SELECT 'Insurance', COUNT(*) FROM Insurance
UNION ALL
SELECT 'Emergency_Contacts', COUNT(*) FROM Emergency_Contacts
UNION ALL
SELECT 'Healthcare_Providers', COUNT(*) FROM Healthcare_Providers
UNION ALL
SELECT 'Provider_Access', COUNT(*) FROM Provider_Access
UNION ALL
SELECT 'Access_Log', COUNT(*) FROM Access_Log;

-- 3. Check sample patient data
SELECT '=== SAMPLE PATIENT ===' as Info;
SELECT * FROM Patients LIMIT 1;

-- 4. Check sample provider data
SELECT '=== SAMPLE PROVIDER ===' as Info;
SELECT * FROM Healthcare_Providers LIMIT 1;

-- 5. Test the views
SELECT '=== TESTING VIEWS ===' as Info;
SELECT * FROM Patient_Summary_View LIMIT 5;

-- 6. List all stored procedures
SELECT '=== STORED PROCEDURES ===' as Info;
SHOW PROCEDURE STATUS WHERE Db = 'mias_db';

-- 7. Test foreign key relationships
SELECT '=== RELATIONSHIP TEST ===' as Info;
SELECT 
    p.first_name, 
    p.last_name, 
    COUNT(DISTINCT mc.condition_id) as conditions,
    COUNT(DISTINCT a.allergy_id) as allergies,
    COUNT(DISTINCT m.medication_id) as medications
FROM Patients p
LEFT JOIN Medical_Conditions mc ON p.patient_id = mc.patient_id
LEFT JOIN Allergies a ON p.patient_id = a.patient_id
LEFT JOIN Medications m ON p.patient_id = m.patient_id
GROUP BY p.patient_id;

-- =====================================================
-- If all queries run successfully, your database is ready! ✅
-- =====================================================
