# MIAS - Python/Streamlit Version

Medical Information Access System (MIAS) - Patient Portal

## Features

- 🔍 Barcode scanner integration for patient registration
- 👤 Secure patient portal (License # + PIN authentication)
- 🏥 Medical information management (conditions, allergies, medications)
- 📊 Analytics dashboard
- 🗄️ Database management tools
- 📞 Emergency contacts management

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.9+
- **Database:** MySQL 8.0 (AWS RDS)
- **Barcode Parser:** Custom AAMVA parser

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials

Create `.streamlit/secrets.toml` file:

```toml
[database]
host = "your-database-host"
port = 3306
user = "your-username"
password = "your-password"
database = "mias_db"
```

**⚠️ NEVER commit secrets.toml to GitHub!**

### 3. Run the Application

```bash
streamlit run app.py
```

## Project Structure

```
Python_Streamlit/
├── app.py                          # Main application
├── database.py                     # Database operations
├── aamva_parser.py                 # Driver's license parser
├── pages/
│   ├── 1_Patient_Registration.py   # Register patients
│   ├── 2_Medical_Info_Manager.py   # Manage medical records
│   ├── 3_Analytics_Dashboard.py    # View analytics
│   ├── 4_Database_Management.py    # Admin tools
│   ├── 5_Patient_Portal.py         # Patient login
│   └── 6_Patient_Dashboard.py      # Patient self-service
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── requirements.txt                # Python dependencies
```

## Team

- Ryan King
- Raphe Burstein
- Bryan Barber

## Course

SMU ITOM 6265 - Database Management | Fall 2025  
Instructor: Professor Kannan
