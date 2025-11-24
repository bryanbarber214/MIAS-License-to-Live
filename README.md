# 🏥 License to Live: MIAS
## Medical Information Access System

**Healthcare Database with Emergency Medical Access**

[![Status](https://img.shields.io/badge/Status-Complete-success)]()
[![Database](https://img.shields.io/badge/Database-AWS%20RDS%20MySQL-blue)]()
[![Platform](https://img.shields.io/badge/Platform-R%20Shiny-orange)]()

**Team:** Ryan King, Raphe Burstein, Bryan Barber  
**Course:** SMU ITOM 6265 - Database Management | Fall 2025  
**Instructor:** Professor Kannan

---

## 🚀 **START HERE - 3 STEPS TO RUN**

### **Step 1: Install R Packages** (2 minutes)
Open RStudio and paste this into the Console:
```r
install.packages(c("shiny", "DBI", "RMySQL", "shinyjs", 
                   "stringr", "lubridate", "DT", "ggplot2", 
                   "gridExtra", "dplyr", "scales"))
```

### **Step 2: Download Project Files** (1 minute)
Click the green **"Code"** button above → **Download ZIP** → Extract to your computer

Or use your MIAS_Core folder if you already have the files.

### **Step 3: Launch the System** (30 seconds)
In RStudio Console:
```r
setwd("C:/path/to/MIAS_Core")  # Change to YOUR folder path
source("launch_mias.R")         # This launches the menu!
```

**You'll see this menu:**
```
╔════════════════════════════════════════════════╗
║     LICENSE TO LIVE: MIAS SYSTEM LAUNCHER     ║
╚════════════════════════════════════════════════╝

Select an application to launch:

1. 🔍 Patient Registration (Barcode Scanner)
2. 🏥 Medical Information Manager
3. 📊 Analytics Dashboard  ⭐ RECOMMENDED FIRST
4. 🚪 Exit

Enter your choice (1-4): 
```

**Type 3 and press Enter** to see the Analytics Dashboard!

---

## 📊 **What This System Does**

License to Live: MIAS enables emergency medical access by linking driver's licenses to critical health information.

**Key Features:**
- ✅ **AWS Cloud Database** - 10 tables with patient medical records
- ✅ **Barcode Scanner** - Scan driver's license to register patients
- ✅ **Medical Manager** - Add allergies, medications, conditions, vaccinations
- ✅ **Analytics Dashboard** - Real-time visualizations with ggplot2

**Use Case:** EMT scans unconscious patient's driver's license → System retrieves critical allergies, medications, conditions, blood type, emergency contacts → Informed treatment decisions save lives.

---

## 🎯 **For Professors/Reviewers**

### **Quick Demo (10 minutes)**

**Best place to start:** Analytics Dashboard (shows everything working)

```r
source("launch_mias.R")
# Type: 3
# Press: Enter
```

**You'll see:**
- 8 summary statistics (patients, medications, allergies, etc.)
- 5 visualization tabs with ggplot2 charts
- Real-time data from AWS database

**Then explore:**
- Medical Information Manager (Type: 2) - Search "BRYAN" to see demo patient
- Patient Registration (Type: 1) - Requires physical barcode scanner

### **Evaluate These:**
- [ ] **Phase 1:** Database design ([ERD](MIAS_ERD_Design.docx), [Schema](mias_database_schema.sql))
- [ ] **Phase 2:** Barcode scanner integration ([Guide](Barcode_Scanner_Integration_Guide.docx))
- [ ] **Phase 3:** Medical info management ([Docs](Phase_3_Medical_Information_Manager.docx))
- [ ] **Phase 4:** Analytics dashboard ([Docs](Phase_4_Analytics_Dashboard.docx)) ⭐ **MS Analytics Requirement**

**Full Review Guide:** Open [QUICK_START_FOR_REVIEWERS.txt](QUICK_START_FOR_REVIEWERS.txt)

---

## 🗄️ **Database Access**

**AWS RDS MySQL Connection:**
```
Host: mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com
Port: 3306
Database: mias_db
Username: admin
Password: License2Live
```

**Test Query (VS Code or MySQL Workbench):**
```sql
USE mias_db;
SELECT * FROM Patients;
```

---

## 📁 **Project Structure**

```
MIAS_Core/
│
├── 🚀 launch_mias.R                    # START HERE - Master launcher
│
├── 📱 Applications
│   ├── patient_registration_app.R      # Barcode scanner registration
│   ├── medical_info_manager.R          # Medical history management
│   └── analytics_dashboard.R           # Real-time visualizations
│
├── 🔧 Core Components
│   ├── aamva_parser.R                  # Driver's license parser
│   └── test_eyoyo_format.R             # Scanner testing
│
├── 🗄️ Database
│   ├── mias_database_schema.sql        # Complete DDL (10 tables, 4 views, 4 procedures)
│   └── database_verification.sql       # Test queries
│
└── 📚 Documentation
    ├── QUICK_START_FOR_REVIEWERS.txt   # 5-minute setup guide
    ├── SUBMISSION_README.txt            # Complete project documentation
    ├── PROJECT_COMPLETE_README.txt      # Project summary
    ├── MIAS_ERD_Design.docx             # Database design
    ├── Phase_2/3/4 Guides               # Phase-specific documentation
    └── Setup files                      # Installation instructions
```

---

## 🎓 **MS Analytics Requirement - EXCEEDED**

**Project Requirement:**  
*"Build at least one analytics function into the application. This could be a graph (ggplot2) or results of running a model."*

**What We Delivered:**
- ✅ **8 real-time summary metrics**
- ✅ **7 ggplot2 visualizations** (bar charts, histograms, pie charts)
- ✅ **5 comprehensive analysis tabs**
  - 💉 Vaccination Coverage Analysis
  - 👥 Patient Demographics (age, blood type, geography)
  - 💊 Medication Trends (top 10 prescribed)
  - ⚠️ Allergy Severity Distribution
  - 📈 Comprehensive Report (all charts)
- ✅ **Interactive dashboard** with data refresh
- ✅ **Actionable healthcare insights**

**Result:** Requirement significantly exceeded with production-quality analytics platform.

---

## 🏗️ **Technical Architecture**

### **Database Layer**
- **Platform:** AWS RDS MySQL 8.0.43
- **Region:** us-east-2 (Ohio)
- **Tables:** 10 (fully normalized)
- **Views:** 4 (for common queries)
- **Procedures:** 4 (for complex operations)
- **Security:** VPC, encrypted storage, audit logging

### **Application Layer**
- **Framework:** R Shiny
- **Visualization:** ggplot2, gridExtra
- **Database:** DBI, RMySQL
- **UI/UX:** shinyjs, DT (DataTables)

### **Hardware Integration**
- **Scanner:** Eyoyo EY-009P (2D barcode, Bluetooth)
- **Standard:** AAMVA (all US driver's licenses)

---

## 📊 **Database Schema**

**10 Tables:**
1. **Patients** - Central registry (license_number as unique key)
2. **Medical_Conditions** - Chronic conditions with severity
3. **Allergies** - Critical allergy information
4. **Medications** - Current and historical prescriptions
5. **Vaccinations** - Immunization records
6. **Insurance** - Healthcare coverage policies
7. **Emergency_Contacts** - Prioritized contact list
8. **Healthcare_Providers** - Authorized medical professionals
9. **Provider_Access** - Authorization tracking (many-to-many)
10. **Access_Log** - HIPAA audit trail

**Full ERD:** [MIAS_ERD_Design.docx](MIAS_ERD_Design.docx)

---

## 🎬 **Demo Workflow**

**For Presentations (12 minutes):**

1. **Show ERD** (2 min) - Database design and relationships
2. **Demo Medical Info Manager** (3 min) - Search patient, add medical data
3. **Demo Analytics Dashboard** (5 min) ⭐ **KEY DELIVERABLE**
   - Summary statistics
   - All 5 visualization tabs
   - Explain insights
4. **Show Database in VS Code** (2 min) - Live queries, populated tables

---

## 🔧 **Troubleshooting**

**Problem:** Package installation fails  
**Solution:** Install one at a time: `install.packages("shiny")`

**Problem:** "Cannot find file 'launch_mias.R'"  
**Solution:** Check working directory: `getwd()` and `setwd()`

**Problem:** Database connection fails  
**Solution:** Check internet connection and credentials

**Problem:** Charts show "No data available"  
**Solution:** Normal! Use medical_info_manager.R to add test data first

**More help:** See [QUICK_START_FOR_REVIEWERS.txt](QUICK_START_FOR_REVIEWERS.txt)

---

## 📞 **Contact & Support**

**Team Members:**
- Bryan Barber - bryanbarber214@gmail.com
- Ryan King
- Raphe Burstein

**Course:** SMU ITOM 6265 - Database Management  
**Instructor:** Professor Kannan

---

## 📄 **License & Academic Use**

This project was developed as coursework for SMU's MS Analytics program.  
All data is synthetic for demonstration purposes.

---

## ⭐ **Star This Repo**

If you find this project useful or interesting, please give it a star! ⭐

---

**Ready to run?** → Scroll up to **START HERE** and follow the 3 steps! 🚀

---

<div align="center">

**Built with ❤️ by Team Barber-King-Burstein**

*Healthcare Information Systems | Database Management | Real-time Analytics*

</div>
