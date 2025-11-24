# =====================================================
# License to Live: MIAS - Barcode Scanner Setup
# Installation & Testing Guide
# =====================================================

# PART 1: Install Required R Packages
# =====================================

# Run these commands in your R console or RStudio:

install.packages("shiny")
install.packages("DBI")
install.packages("RMySQL")
install.packages("shinyjs")
install.packages("stringr")
install.packages("lubridate")

# PART 2: Test the AAMVA Parser
# ==============================

# This tests if the parser can correctly extract data from your license scan

# Set your working directory to where you saved the files
# setwd("path/to/your/files")

# Source the parser
source("aamva_parser.R")

# Test with your actual license data
test_result <- test_parser()

# You should see output like:
# === PARSED DRIVER'S LICENSE DATA ===
# 
# PERSONAL INFORMATION:
#   Name: BRYAN EDWARD BARBER
#   Date of Birth: May 25, 1977
#   Sex: Male
# 
# LICENSE INFORMATION:
#   License Number: 10896644
#   State: TX
#   Issue Date: June 13, 2025
#   Expiration Date: May 25, 2029
# 
# ADDRESS:
#   Street: 2802 LAKESIDE LN
#   City: CARROLLTON
#   State: TX
#   ZIP Code: 75006-4725
# 
# PHYSICAL DESCRIPTION:
#   Height: 72 inches
#   Weight: 180 lbs
#   Eye Color: Hazel
#   Hair Color: Brown

# PART 3: Test Database Connection
# =================================

library(DBI)
library(RMySQL)

# Database configuration
db_config <- list(
  host = "mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com",
  port = 3306,
  user = "admin",
  password = "License2Live",
  dbname = "mias_db"
)

# Test connection
conn <- dbConnect(
  MySQL(),
  host = db_config$host,
  port = db_config$port,
  user = db_config$user,
  password = db_config$password,
  dbname = db_config$dbname
)

# Check if Patients table exists
tables <- dbListTables(conn)
print(tables)

# Check current patient count
patient_count <- dbGetQuery(conn, "SELECT COUNT(*) as count FROM Patients")
cat("\nCurrent patients in database:", patient_count$count, "\n")

# Close connection
dbDisconnect(conn)

cat("\n✅ Database connection test successful!\n")

# PART 4: Run the Shiny App
# ==========================

# Make sure both files are in the same directory:
# - aamva_parser.R
# - patient_registration_app.R

# Run the app
library(shiny)
runApp("patient_registration_app.R")

# The app should open in your web browser
# You can now test with your Eyoyo scanner!

# PART 5: Testing Workflow
# =========================

# 1. Open the Shiny app
# 2. Click in the "Barcode Input" text field
# 3. Scan a driver's license with your Eyoyo scanner
# 4. Click "Parse Barcode"
# 5. Review the extracted information
# 6. Add phone, email, and blood type (optional)
# 7. Click "Register Patient"
# 8. Verify success message
# 9. Check database in VS Code to confirm patient was added

# Query to check new patient in VS Code:
# SELECT * FROM Patients ORDER BY created_at DESC LIMIT 5;

# TROUBLESHOOTING
# ===============

# Problem: Parser doesn't recognize barcode format
# Solution: Check that the barcode starts with "ANSI 636"
#           Texas licenses use AAMVA version 6
#           Make sure the entire barcode is captured

# Problem: Database connection fails
# Solution: Verify your AWS security group allows connections
#           Check that credentials are correct
#           Ensure VS Code can connect successfully first

# Problem: Duplicate license number error
# Solution: This is expected! The system prevents duplicate registrations
#           Use the clear button and try a different license

# Problem: Shiny app doesn't load
# Solution: Make sure all packages are installed
#           Check that both R files are in the same directory
#           Look at the R console for error messages

# NEXT STEPS
# ==========

# After successful testing:
# 1. Register 10-15 test patients
# 2. Verify data in database using VS Code
# 3. Test the duplicate detection
# 4. Move to Phase 3: Medical information entry forms
