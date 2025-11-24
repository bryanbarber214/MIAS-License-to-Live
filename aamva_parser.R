# =====================================================
# AAMVA Driver's License Barcode Parser
# License to Live: MIAS Project
# =====================================================

library(stringr)
library(lubridate)

#' Parse AAMVA Driver's License Barcode
#'
#' @param barcode_data Raw string from 2D barcode scanner
#' @return List with parsed fields
#' @export
parse_aamva_barcode <- function(barcode_data) {
  
  # Initialize result list
  result <- list(
    raw_data = barcode_data,
    parsed = FALSE,
    error = NULL
  )
  
  # Try to parse the barcode
  tryCatch({
    
    # CRITICAL: Clean up Eyoyo scanner output
    # 1. Remove leading @ symbol
    barcode_data <- gsub("^@\\s*", "", barcode_data)
    
    # 2. Remove ALL line breaks and newlines (scanner splits data across lines)
    barcode_data <- gsub("[\r\n]+", "", barcode_data)
    
    # 3. Remove any remaining whitespace at start/end
    barcode_data <- str_trim(barcode_data)
    
    # AAMVA Field Codes
    fields <- list(
      # Personal Information
      first_name = extract_field(barcode_data, "DAC"),
      middle_name = extract_field(barcode_data, "DAD"),
      last_name = extract_field(barcode_data, "DCS"),
      
      # License Information
      license_number = extract_field(barcode_data, "DAQ"),
      
      # Date Information
      date_of_birth = parse_aamva_date(extract_field(barcode_data, "DBB")),
      issue_date = parse_aamva_date(extract_field(barcode_data, "DBD")),
      expiration_date = parse_aamva_date(extract_field(barcode_data, "DBA")),
      
      # Address Information
      address_street = extract_field(barcode_data, "DAG"),
      address_city = extract_field(barcode_data, "DAI"),
      address_state = extract_field(barcode_data, "DAJ"),
      address_zip = extract_field(barcode_data, "DAK"),
      
      # Physical Description
      sex = decode_sex(extract_field(barcode_data, "DBC")),
      height_inches = extract_field(barcode_data, "DAU"),
      weight_lbs = extract_field(barcode_data, "DAW"),
      eye_color = decode_eye_color(extract_field(barcode_data, "DAY")),
      hair_color = decode_hair_color(extract_field(barcode_data, "DAZ")),
      
      # Additional Information
      country = extract_field(barcode_data, "DCG"),
      document_discriminator = extract_field(barcode_data, "DCF")
    )
    
    result$fields <- fields
    result$parsed <- TRUE
    
  }, error = function(e) {
    result$error <- paste("Parse error:", e$message)
    result$parsed <- FALSE
  })
  
  return(result)
}

#' Extract a specific field from AAMVA barcode data
#'
#' @param data Barcode string
#' @param code AAMVA field code (e.g., "DAC", "DCS")
#' @return Extracted value or NA
extract_field <- function(data, code) {
  # Pattern: code followed by data until next code or end
  pattern <- paste0(code, "([^D]*?)(?=D[A-Z]{2}|$)")
  match <- str_match(data, pattern)
  
  if (!is.na(match[1, 2])) {
    value <- str_trim(match[1, 2])
    # Remove trailing non-alphanumeric except spaces and hyphens
    value <- str_replace(value, "[^A-Za-z0-9 -]+$", "")
    return(value)
  }
  return(NA)
}

#' Parse AAMVA date format (MMDDYYYY)
#'
#' @param date_str Date string in MMDDYYYY format
#' @return Date object or NA
parse_aamva_date <- function(date_str) {
  if (is.na(date_str) || nchar(date_str) != 8) {
    return(NA)
  }
  
  tryCatch({
    month <- substr(date_str, 1, 2)
    day <- substr(date_str, 3, 4)
    year <- substr(date_str, 5, 8)
    date_string <- paste(year, month, day, sep = "-")
    return(as.Date(date_string))
  }, error = function(e) {
    return(NA)
  })
}

#' Decode sex code
#'
#' @param code Sex code (1 = Male, 2 = Female)
#' @return "Male", "Female", or NA
decode_sex <- function(code) {
  if (is.na(code)) return(NA)
  
  sex_map <- c("1" = "Male", "2" = "Female", "M" = "Male", "F" = "Female")
  return(sex_map[code])
}

#' Decode eye color code
#'
#' @param code Eye color abbreviation
#' @return Full eye color name
decode_eye_color <- function(code) {
  if (is.na(code)) return(NA)
  
  eye_colors <- c(
    "BLK" = "Black",
    "BLU" = "Blue",
    "BRO" = "Brown",
    "GRY" = "Gray",
    "GRN" = "Green",
    "HAZ" = "Hazel",
    "MAR" = "Maroon",
    "PNK" = "Pink",
    "DIC" = "Dichromatic"
  )
  
  result <- eye_colors[code]
  return(ifelse(is.na(result), code, result))
}

#' Decode hair color code
#'
#' @param code Hair color abbreviation
#' @return Full hair color name
decode_hair_color <- function(code) {
  if (is.na(code)) return(NA)
  
  hair_colors <- c(
    "BAL" = "Bald",
    "BLK" = "Black",
    "BLN" = "Blond",
    "BRO" = "Brown",
    "GRY" = "Gray",
    "RED" = "Red/Auburn",
    "SDY" = "Sandy",
    "WHI" = "White"
  )
  
  result <- hair_colors[code]
  return(ifelse(is.na(result), code, result))
}

#' Convert parsed AAMVA data to database-ready format
#'
#' @param parsed_data Result from parse_aamva_barcode()
#' @return Data frame ready for database insertion
prepare_for_database <- function(parsed_data) {
  
  if (!parsed_data$parsed) {
    stop("Cannot prepare unparsed data for database")
  }
  
  fields <- parsed_data$fields
  
  # Create data frame matching Patients table structure
  patient_data <- data.frame(
    license_number = as.character(fields$license_number),
    first_name = as.character(fields$first_name),
    last_name = as.character(fields$last_name),
    date_of_birth = as.character(fields$date_of_birth),
    address = as.character(fields$address_street),
    city = as.character(fields$address_city),
    state = as.character(fields$address_state),
    zip_code = as.character(fields$address_zip),
    phone = NA_character_,  # Not in barcode - will be entered manually
    email = NA_character_,  # Not in barcode - will be entered manually
    blood_type = NA_character_,  # Not in barcode - will be entered manually
    stringsAsFactors = FALSE
  )
  
  return(patient_data)
}

#' Format parsed data for display
#'
#' @param parsed_data Result from parse_aamva_barcode()
#' @return Formatted string for display
format_parsed_data <- function(parsed_data) {
  
  if (!parsed_data$parsed) {
    return(paste("Error:", parsed_data$error))
  }
  
  fields <- parsed_data$fields
  
  output <- paste0(
    "=== PARSED DRIVER'S LICENSE DATA ===\n\n",
    "PERSONAL INFORMATION:\n",
    "  Name: ", fields$first_name, " ", 
    ifelse(is.na(fields$middle_name), "", paste0(fields$middle_name, " ")),
    fields$last_name, "\n",
    "  Date of Birth: ", format(fields$date_of_birth, "%B %d, %Y"), "\n",
    "  Sex: ", fields$sex, "\n\n",
    
    "LICENSE INFORMATION:\n",
    "  License Number: ", fields$license_number, "\n",
    "  State: ", fields$address_state, "\n",
    "  Issue Date: ", format(fields$issue_date, "%B %d, %Y"), "\n",
    "  Expiration Date: ", format(fields$expiration_date, "%B %d, %Y"), "\n\n",
    
    "ADDRESS:\n",
    "  Street: ", fields$address_street, "\n",
    "  City: ", fields$address_city, "\n",
    "  State: ", fields$address_state, "\n",
    "  ZIP Code: ", fields$address_zip, "\n\n",
    
    "PHYSICAL DESCRIPTION:\n",
    "  Height: ", fields$height_inches, " inches\n",
    "  Weight: ", fields$weight_lbs, " lbs\n",
    "  Eye Color: ", fields$eye_color, "\n",
    "  Hair Color: ", fields$hair_color, "\n"
  )
  
  return(output)
}

# =====================================================
# TESTING FUNCTION
# =====================================================

#' Test the parser with sample data
test_parser <- function() {
  
  # Your actual Texas license scan
  test_data <- "ANSI 636015090002DL00410280ZT03210007DLDCACMDCBNONEDCDNONEDBA05252029DCSBARBERDDENDACBRYANDDFNDADEDWARDDDGNDBD06132025DBB05251977DBC1DAYHAZDAU072 inDAG2802 LAKESIDE LNDAICARROLLTONDAJTXDAK75006-4725DAQ10896644DCF20629580167103805092DCGUSADAZBRODCK10032767923DCLWDDAFDDB07162021DAW180DDK1ZTZTAN"
  
  cat("Testing AAMVA Parser with Texas Driver's License...\n\n")
  
  # Parse the data
  result <- parse_aamva_barcode(test_data)
  
  if (result$parsed) {
    cat(format_parsed_data(result))
    cat("\n\n=== DATABASE-READY FORMAT ===\n")
    db_data <- prepare_for_database(result)
    print(db_data)
    cat("\n✅ Parser test successful!\n")
  } else {
    cat("❌ Parser test failed:\n")
    cat(result$error, "\n")
  }
  
  return(result)
}

# Run test if this script is executed directly
if (!interactive()) {
  test_parser()
}
