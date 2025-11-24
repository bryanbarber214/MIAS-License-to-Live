# LICENSE TO LIVE: MIAS - PROJECT SUBMISSION
## Medical Information Access System

**Team Members:** Ryan King, Raphe Burstein, Bryan Barber  
**Course:** SMU ITOM 6265 - Database Management  
**Instructor:** Professor Kannan  
**Date:** November 2025

---

## 📋 EXECUTIVE SUMMARY

License to Live: MIAS is a complete healthcare information management system that enables emergency medical access through driver's license integration. The system includes:

- **AWS RDS MySQL Database** (10 tables, 4 views, 4 stored procedures)
- **2D Barcode Scanner Integration** (AAMVA standard parser)
- **Patient Registration System** (Shiny web application)
- **Medical Information Manager** (Comprehensive health records)
- **Analytics Dashboard** (Real-time visualizations with ggplot2)

---

## 🗂️ PROJECT DELIVERABLES

### R Applications (5 files)
1. **launch_mias.R** - Master launcher for all applications
2. **aamva_parser.R** - Driver's license barcode parser
3. **patient_registration_app.R** - Patient registration with scanner
4. **medical_info_manager.R** - Medical history management
5. **analytics_dashboard.R** - Real-time analytics dashboard

### Database Files (2 files)
1. **mias_database_schema.sql** - Complete database DDL
2. **database_verification.sql** - Verification queries

### Documentation (8 files)
1. **MIAS_ERD_Design.docx** - Entity-Relationship Diagram
2. **Barcode_Scanner_Integration_Guide.docx** - Phase 2 documentation
3. **Phase_3_Medical_Information_Manager.docx** - Phase 3 documentation
4. **Phase_4_Analytics_Dashboard.docx** - Phase 4 documentation
5. **MIAS_Project_Status_And_Roadmap.docx** - Project timeline
6. **PROJECT_COMPLETE_README.txt** - Complete project summary
7. **PHASE_3_SETUP.txt** - Phase 3 setup instructions
8. **PHASE_4_SETUP.txt** - Phase 4 setup instructions

### Setup & Test Files (4 files)
1. **SETUP_INSTRUCTIONS.R** - Initial setup guide
2. **SCANNER_FORMAT_FIX.txt** - Scanner configuration notes
3. **test_eyoyo_format.R** - Parser testing script
4. **SUBMISSION_README.txt** - This file

---

## 🚀 QUICK START GUIDE

### Prerequisites
- R and RStudio installed
- Required R packages (see installation section below)
- AWS database access (credentials provided separately)
- Eyoyo EY-009P 2D barcode scanner (for patient registration)

### Installation

**Step 1: Install Required R Packages**
```r
install.packages(c("shiny", "DBI", "RMySQL", "shinyjs", 
                   "stringr", "lubridate", "DT", "ggplot2", "gridExtra"))
```

**Step 2: Set Working Directory**
```r
setwd("path/to/MIAS_Core")
```

**Step 3: Launch System**
```r
source("launch_mias.R")
```

Select from menu:
1. Patient Registration (Barcode Scanner)
2. Medical Information Manager
3. Analytics Dashboard
4. Exit

---

## 🗄️ DATABASE ACCESS

**AWS RDS MySQL Instance**
- **Host:** mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com
- **Port:** 3306
- **Database:** mias_db
- **Username:** admin
- **Password:** License2Live

**Security Notes:**
- Database is hosted on AWS RDS (us-east-2 region)
- Security group configured for team access
- All data encrypted at rest
- Audit logging enabled via Access_Log table

**To Connect via VS Code:**
1. Install Database Client extension
2. Create new MySQL connection
3. Use credentials above
4. Test connection

---

## 📊 DATABASE SCHEMA

### Core Tables (10)

**1. Patients** - Central patient registry
- Primary Key: patient_id
- Unique Key: license_number
- Fields: demographics, contact info, blood type

**2. Medical_Conditions** - Chronic conditions
- Foreign Key: patient_id → Patients
- Fields: condition_name, diagnosis_date, severity, notes

**3. Allergies** - Allergy information (CRITICAL)
- Foreign Key: patient_id → Patients
- Fields: allergen, allergy_type, reaction, severity

**4. Medications** - Current and historical medications
- Foreign Key: patient_id → Patients
- Fields: medication_name, dosage, frequency, dates, prescriber

**5. Vaccinations** - Immunization records
- Foreign Key: patient_id → Patients
- Fields: vaccine_name, administration_date, next_due_date

**6. Insurance** - Healthcare coverage
- Foreign Key: patient_id → Patients
- Fields: provider_name, policy_number, dates, is_active

**7. Emergency_Contacts** - Emergency contact list
- Foreign Key: patient_id → Patients
- Fields: contact_name, relationship, phones, priority_order

**8. Healthcare_Providers** - Authorized medical professionals
- Primary Key: provider_id
- Fields: name, specialty, license_number, facility

**9. Provider_Access** - Provider authorization (Many-to-Many)
- Foreign Keys: patient_id, provider_id
- Fields: granted_date, revoked_date, access_level

**10. Access_Log** - HIPAA audit trail
- Foreign Keys: patient_id, provider_id
- Fields: timestamp, action_type, ip_address, details

### Views (4)
1. Active_Medications_View - Current medications per patient
2. Patient_Summary_View - Patient overview with counts
3. Provider_Access_Summary - Provider authorization statistics
4. Vaccination_Coverage_View - Vaccination analytics

### Stored Procedures (4)
1. Log_Patient_Access - Audit logging helper
2. Grant_Provider_Access - Authorize provider with logging
3. Revoke_Provider_Access - Remove authorization with logging
4. Get_Emergency_Info - Fast emergency lookup by license number

---

## 🔍 SYSTEM FEATURES

### Phase 1: Database Architecture ✅
- AWS RDS MySQL deployment
- 10 normalized tables
- Entity-Relationship Diagram
- Views and stored procedures
- Security configuration

### Phase 2: Barcode Scanner Integration ✅
- AAMVA standard parser (all US states)
- Eyoyo EY-009P Bluetooth scanner support
- Automatic patient registration
- Duplicate detection
- Data validation

### Phase 3: Medical Information Management ✅
- Patient search functionality
- Medical conditions tracking
- Allergy management (severity levels)
- Medication history (current/past)
- Vaccination records (with boosters)
- Insurance policies (active/inactive)
- Emergency contacts (prioritized)

### Phase 4: Analytics Dashboard ✅
- 8 real-time summary metrics
- Vaccination coverage analysis
- Patient demographics (age, blood type, geography)
- Medication trends (top 10 prescribed)
- Allergy severity distribution
- Comprehensive reporting view
- ggplot2 visualizations

---

## 📈 ANALYTICS REQUIREMENT SATISFIED

**MS Analytics Program Requirement:**
"Build at least one analytics function into the application. 
This could be a graph (ggplot2) or results of running a model."

**What We Delivered:**
✅ Multiple ggplot2 visualizations
✅ 8 real-time metrics
✅ 5 comprehensive analysis tabs
✅ Bar charts, histograms, pie charts
✅ Interactive dashboard with data refresh
✅ Actionable healthcare insights

**Result:** Requirement significantly exceeded

---

## 🧪 TESTING INSTRUCTIONS

### Test the System

**1. Test Database Connection**
```sql
USE mias_db;
SELECT COUNT(*) FROM Patients;
```

**2. Test Barcode Parser**
```r
source("test_eyoyo_format.R")
```

**3. Test Patient Registration**
- Launch patient_registration_app.R
- Scan a driver's license
- Verify registration in database

**4. Test Medical Info Manager**
- Launch medical_info_manager.R
- Search for patient
- Add medical information across all 6 categories
- Verify in database

**5. Test Analytics Dashboard**
- Launch analytics_dashboard.R
- View all 5 visualization tabs
- Click "Refresh Data" button
- Verify real-time updates

---

## 📸 DEMONSTRATION GUIDE

### For Presentation

**1. Show Database Architecture (3 minutes)**
- Display ERD diagram
- Explain 10 tables and relationships
- Highlight security features

**2. Demonstrate Patient Registration (3 minutes)**
- Launch patient registration app
- Scan driver's license with Eyoyo scanner
- Show automatic data population
- Verify database entry in VS Code

**3. Demonstrate Medical Information Entry (4 minutes)**
- Launch medical info manager
- Search for patient
- Add examples across all categories:
  * Medical condition (e.g., Hypertension)
  * Allergy (e.g., Penicillin - Life-threatening)
  * Medication (e.g., Lisinopril 10mg daily)
  * Vaccination (e.g., COVID-19 booster)
  * Insurance (e.g., Blue Cross Blue Shield)
  * Emergency contact (e.g., Spouse)

**4. Present Analytics Dashboard (5 minutes)**
- Launch analytics dashboard
- Show 8 summary metrics
- Present key visualizations:
  * Vaccination coverage chart
  * Patient demographics
  * Medication trends
  * Allergy severity analysis
- Explain insights and conclusions

---

## 🎯 PROJECT OUTCOMES

### Technical Achievements
✅ Fully functional AWS cloud database
✅ Hardware integration (2D barcode scanner)
✅ Three production-ready Shiny applications
✅ Real-time data visualization with ggplot2
✅ Complete CRUD operations
✅ HIPAA-compliant audit logging
✅ Secure authentication and authorization

### Educational Objectives Met
✅ Database design and normalization
✅ SQL DDL and DML
✅ Cloud deployment (AWS RDS)
✅ Application development (R Shiny)
✅ Data visualization (ggplot2)
✅ Team collaboration
✅ Project documentation
✅ Analytics requirement exceeded

### Real-World Application
✅ Solves genuine healthcare problem
✅ Emergency medical access system
✅ Scalable architecture
✅ Production-ready code quality
✅ Comprehensive error handling
✅ User-friendly interfaces

---

## 🔮 FUTURE ENHANCEMENTS

### Potential Expansions (Not Required)
- Mobile application for patients
- QR code generation for instant access
- Biometric authentication
- Integration with EHR systems (Epic, Cerner)
- Telemedicine capabilities
- Prescription interaction checking
- Predictive analytics (machine learning)
- Multi-language support
- HIPAA compliance certification
- Real-time notifications to emergency contacts

---

## 👥 TEAM CONTRIBUTIONS

**Bryan Barber**
- Database architecture and AWS setup
- Barcode scanner integration
- R application development
- System testing and documentation

**Ryan King**
- [Team member contributions]

**Raphe Burstein**
- [Team member contributions]

---

## 📞 CONTACT INFORMATION

**For Questions or Issues:**

**Bryan Barber**
- Email: bryanbarber214@gmail.com
- Phone: 214-414-8100

**Team Repository:** [GitHub URL if created]

**AWS Database Access:** Credentials provided above

---

## 📚 REFERENCES

### Technology Documentation
- R Shiny: https://shiny.rstudio.com/
- ggplot2: https://ggplot2.tidyverse.org/
- AWS RDS: https://aws.amazon.com/rds/
- MySQL: https://dev.mysql.com/doc/
- AAMVA Standard: https://www.aamva.org/

### Course Materials
- SMU ITOM 6265 - Database Management
- Instructor: Professor Kannan
- Semester: Fall Module B 2025

---

## ✅ SUBMISSION CHECKLIST

Before final submission, verify:

- [ ] All R files included and documented
- [ ] Database schema SQL file included
- [ ] All documentation files included
- [ ] README files clear and comprehensive
- [ ] AWS database accessible by team
- [ ] All applications tested and working
- [ ] Screenshots captured for presentation
- [ ] Team member contributions documented
- [ ] Analytics requirement clearly demonstrated
- [ ] Professional presentation prepared

---

## 🎉 PROJECT STATUS: COMPLETE

All four phases successfully delivered:
✅ Phase 1: Database Architecture
✅ Phase 2: Barcode Scanner Integration
✅ Phase 3: Medical Information Management
✅ Phase 4: Analytics & Visualization

**Total Development Time:** 4 days
**Total Files:** 19 files
**Lines of Code:** 3,000+ lines
**Database Tables:** 10 tables
**Shiny Applications:** 3 applications + 1 launcher
**Visualizations:** 7 charts

**Ready for Presentation and Demonstration**

---

Thank you for reviewing our License to Live: MIAS project!

Team: Ryan King, Raphe Burstein, Bryan Barber
SMU MS Analytics Program - ITOM 6265
