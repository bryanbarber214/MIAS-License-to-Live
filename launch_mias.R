# =====================================================
# LICENSE TO LIVE: MIAS - SYSTEM LAUNCHER
# Master launcher for all MIAS applications
# =====================================================

library(shiny)

cat("
╔════════════════════════════════════════════════╗
║     LICENSE TO LIVE: MIAS SYSTEM LAUNCHER     ║
╚════════════════════════════════════════════════╝

Welcome to the Medical Information Access System!

Select an application to launch:

1. 🔍 Patient Registration (Barcode Scanner)
   └─ Scan driver's licenses and register new patients

2. 🏥 Medical Information Manager
   └─ Add/view medical histories, allergies, medications

3. 📊 Analytics Dashboard
   └─ View real-time statistics and visualizations

4. 🚪 Exit

")

choice <- readline(prompt = "Enter your choice (1-4): ")

if (choice == "1") {
  cat("\n")
  cat("════════════════════════════════════════════════\n")
  cat("🔍 LAUNCHING PATIENT REGISTRATION APP...\n")
  cat("════════════════════════════════════════════════\n")
  cat("\n✓ App will open in your web browser\n")
  cat("✓ Click in the barcode input field\n")
  cat("✓ Scan driver's license with Eyoyo scanner\n")
  cat("✓ Click 'Parse Barcode' then 'Register Patient'\n\n")
  Sys.sleep(2)
  runApp("patient_registration_app.R")
  
} else if (choice == "2") {
  cat("\n")
  cat("════════════════════════════════════════════════\n")
  cat("🏥 LAUNCHING MEDICAL INFORMATION MANAGER...\n")
  cat("════════════════════════════════════════════════\n")
  cat("\n✓ App will open in your web browser\n")
  cat("✓ Search for a patient\n")
  cat("✓ Click on patient row to select\n")
  cat("✓ Use tabs to add medical information\n\n")
  Sys.sleep(2)
  runApp("medical_info_manager.R")
  
} else if (choice == "3") {
  cat("\n")
  cat("════════════════════════════════════════════════\n")
  cat("📊 LAUNCHING ANALYTICS DASHBOARD...\n")
  cat("════════════════════════════════════════════════\n")
  cat("\n✓ App will open in your web browser\n")
  cat("✓ View summary statistics at the top\n")
  cat("✓ Explore 5 visualization tabs\n")
  cat("✓ Click 'Refresh Data' to update charts\n\n")
  Sys.sleep(2)
  runApp("analytics_dashboard.R")
  
} else if (choice == "4") {
  cat("\n")
  cat("════════════════════════════════════════════════\n")
  cat("👋 EXITING MIAS SYSTEM\n")
  cat("════════════════════════════════════════════════\n")
  cat("\nThank you for using License to Live: MIAS!\n")
  cat("All patient data is securely stored on AWS.\n\n")
  
} else {
  cat("\n")
  cat("════════════════════════════════════════════════\n")
  cat("❌ INVALID CHOICE\n")
  cat("════════════════════════════════════════════════\n")
  cat("\nPlease enter a number between 1 and 4.\n")
  cat("Run the launcher again: source('launch_mias.R')\n\n")
}
