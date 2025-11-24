# =====================================================
# Test Script for Eyoyo Scanner Output
# This simulates exactly what your scanner produces
# =====================================================

source("aamva_parser.R")

# This is EXACTLY what your Eyoyo scanner outputs
# (with @ symbol and line breaks)
eyoyo_scanner_output <- "@
ANSI 636015090002DL00410280ZT03210007DLDCACM
DCBNONE
DCDNONE
DBA05252029
DCSBARBER
DDEN
DACBRYAN
DDFN
DADEDWARD
DDGN
DBD06132025
DBB05251977
DBC1
DAYHAZ
DAU072 in
DAG2802 LAKESIDE LN
DAICARROLLTON
DAJTX
DAK75006-4725
DAQ10896644
DCF20629580167103805092
DCGUSA
DAZBRO
DCK10032767923
DCLW
DDAF
DDB07162021
DAW180
DDK1
ZTZTAN"

cat("Testing with EXACT Eyoyo scanner output format...\n")
cat("(includes @ symbol and line breaks)\n\n")

# Parse it
result <- parse_aamva_barcode(eyoyo_scanner_output)

# Display results
if (result$parsed) {
  cat("✅ SUCCESS! Parser handled Eyoyo format correctly!\n\n")
  cat(format_parsed_data(result))
  
  cat("\n\n=== DATABASE-READY FORMAT ===\n")
  db_data <- prepare_for_database(result)
  print(db_data)
  
} else {
  cat("❌ FAILED!\n")
  cat("Error:", result$error, "\n")
}

cat("\n\n=== TESTING NOTES ===\n")
cat("✓ This test uses the EXACT output from your Eyoyo EY-009P scanner\n")
cat("✓ Including the @ symbol at the start\n")
cat("✓ Including all the line breaks throughout the data\n")
cat("✓ The parser automatically cleans this and extracts the data\n")
cat("\nIf you see SUCCESS above, your scanner is ready to use with the Shiny app!\n")
