# GITHUB UPLOAD GUIDE - MIAS Python/Streamlit

## 🎯 Goal
Upload your Python/Streamlit MIAS application to GitHub securely (without exposing database credentials)

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### STEP 1: Prepare Your Local Folder Structure

On your computer, create this structure:

```
Python_Streamlit/
├── app.py
├── database.py
├── aamva_parser.py
├── requirements.txt          ← DOWNLOAD THIS
├── .gitignore                ← DOWNLOAD THIS
├── README.md                 ← DOWNLOAD THIS (rename from README_Python.md)
├── pages/
│   ├── 1_Patient_Registration.py
│   ├── 2_Medical_Info_Manager.py
│   ├── 3_Analytics_Dashboard.py
│   ├── 4_Database_Management.py
│   ├── 5_Patient_Portal.py
│   └── 6_Patient_Dashboard.py
└── .streamlit/
    └── config.toml
```

**Files to download from outputs:**
- ✅ requirements.txt
- ✅ .gitignore
- ✅ README_Python.md (rename to README.md)

**Files you already have:**
- ✅ app.py
- ✅ aamva_parser.py
- ✅ All page files (1-6)
- ✅ config.toml (from earlier)

**CRITICAL: Do NOT include secrets.toml in this folder!**

---

### STEP 2: Modify database.py for Security

**Replace the top of your database.py file** with this:

```python
"""
Database Connection Helper
License to Live: MIAS - Python/Streamlit Version
"""

import pymysql
import pandas as pd
from typing import Dict, List, Optional, Tuple
import streamlit as st

# SECURE: Uses Streamlit secrets instead of hardcoded credentials
try:
    DB_CONFIG = {
        'host': st.secrets["database"]["host"],
        'port': st.secrets["database"]["port"],
        'user': st.secrets["database"]["user"],
        'password': st.secrets["database"]["password"],
        'database': st.secrets["database"]["database"],
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
except:
    # Fallback for local development (if secrets not configured yet)
    st.error("⚠️ Database secrets not configured!")
    DB_CONFIG = {}

# ... rest of your database.py code stays the same ...
```

**Keep everything else in database.py the same!**

---

### STEP 3: Upload to GitHub

#### Option A: Via GitHub Web Interface (Easiest)

1. **Go to your GitHub repository:**
   ```
   https://github.com/bryanbarber214/MIAS-License-to-Live
   ```

2. **Click "Add file" → "Upload files"**

3. **Drag and drop your entire `Python_Streamlit/` folder**

4. **Add commit message:**
   ```
   Add Python/Streamlit patient portal application
   ```

5. **Click "Commit changes"**

Done! ✅

---

#### Option B: Via Git Command Line

```bash
cd "C:\Users\bryan\OneDrive\SMU MSBA\Fall Mod B - 2025\ITOM 6265 - Database Design for Business (Kannan)\Final Project"

# Clone your repo
git clone https://github.com/bryanbarber214/MIAS-License-to-Live.git
cd MIAS-License-to-Live

# Copy your Python_Streamlit folder here
# (manually copy the folder)

# Add files
git add Python_Streamlit/

# Commit
git commit -m "Add Python/Streamlit patient portal application"

# Push
git push origin main
```

---

### STEP 4: Verify Upload

Go to GitHub and check:
- ✅ `Python_Streamlit/` folder exists
- ✅ All Python files are there
- ✅ `.gitignore` is present
- ✅ `requirements.txt` is present
- ✅ **NO** `secrets.toml` file (this should be hidden by .gitignore)

---

### STEP 5: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Configure:**
   - Repository: `bryanbarber214/MIAS-License-to-Live`
   - Branch: `main`
   - Main file path: `Python_Streamlit/app.py`

5. **Click "Advanced settings"**

6. **Add secrets** (paste this):
   ```toml
   [database]
   host = "mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com"
   port = 3306
   user = "admin"
   password = "License2Live"
   database = "mias_db"
   ```

7. **Click "Deploy"**

8. **Wait 3-5 minutes** for deployment

9. **Get your URL:** `your-app-name.streamlit.app`

---

## 🔐 SECURITY CHECKLIST

Before uploading, verify:
- [ ] Database credentials are NOT in any Python file
- [ ] `.gitignore` includes `.streamlit/secrets.toml`
- [ ] `database.py` uses `st.secrets` instead of hardcoded values
- [ ] No passwords in any committed files

---

## ✅ SUCCESS CRITERIA

You're done when:
- [ ] Code is on GitHub
- [ ] App is deployed to Streamlit Cloud
- [ ] You have a live URL
- [ ] Database credentials are secure (in Streamlit secrets, not GitHub)
- [ ] App connects to AWS RDS successfully

---

## 🆘 TROUBLESHOOTING

### "Database connection failed"
- Check that secrets are configured in Streamlit Cloud
- Verify AWS RDS allows connections from Streamlit's IP

### "Module not found"
- Make sure `requirements.txt` is in the correct location
- Check that all dependencies are listed

### Can't see app on Streamlit Cloud
- Verify main file path: `Python_Streamlit/app.py`
- Check that repository is public

---

## 📞 NEED HELP?

If you get stuck:
1. Check the Streamlit Cloud logs
2. Verify all files are uploaded correctly
3. Make sure secrets are configured
4. Test locally first: `streamlit run Python_Streamlit/app.py`

---

**You're ready to go!** 🚀
