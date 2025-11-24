# =====================================================
# License to Live: MIAS - Medical Information Manager
# Phase 3: Medical History Entry & Management
# =====================================================

library(shiny)
library(DBI)
library(RMySQL)
library(shinyjs)
library(DT)

# Database connection configuration
db_config <- list(
  host = "mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com",
  port = 3306,
  user = "admin",
  password = "License2Live",
  dbname = "mias_db"
)

# =====================================================
# Database Helper Functions
# =====================================================

get_db_connection <- function() {
  dbConnect(
    MySQL(),
    host = db_config$host,
    port = db_config$port,
    user = db_config$user,
    password = db_config$password,
    dbname = db_config$dbname
  )
}

# Search patients
search_patients <- function(search_term) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  if (nchar(search_term) == 0) {
    query <- "SELECT patient_id, license_number, first_name, last_name, date_of_birth, 
              city, state FROM Patients ORDER BY last_name, first_name LIMIT 50"
  } else {
    query <- sprintf(
      "SELECT patient_id, license_number, first_name, last_name, date_of_birth, 
       city, state FROM Patients 
       WHERE license_number LIKE '%%%s%%' 
       OR first_name LIKE '%%%s%%' 
       OR last_name LIKE '%%%s%%'
       ORDER BY last_name, first_name",
      search_term, search_term, search_term
    )
  }
  
  dbGetQuery(conn, query)
}

# Get patient details
get_patient_details <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Patients WHERE patient_id = %d", patient_id)
  dbGetQuery(conn, query)
}

# Get medical conditions
get_conditions <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Medical_Conditions WHERE patient_id = %d ORDER BY diagnosis_date DESC", patient_id)
  dbGetQuery(conn, query)
}

# Add medical condition
add_condition <- function(patient_id, condition_name, diagnosis_date, severity, notes) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf(
    "INSERT INTO Medical_Conditions (patient_id, condition_name, diagnosis_date, severity, notes) 
     VALUES (%d, '%s', %s, %s, %s)",
    patient_id,
    gsub("'", "''", condition_name),
    if(is.na(diagnosis_date) || diagnosis_date == "") "NULL" else paste0("'", diagnosis_date, "'"),
    if(is.na(severity) || severity == "") "NULL" else paste0("'", severity, "'"),
    if(is.na(notes) || notes == "") "NULL" else paste0("'", gsub("'", "''", notes), "'")
  )
  
  tryCatch({
    dbExecute(conn, query)
    list(success = TRUE, message = "Condition added successfully")
  }, error = function(e) {
    list(success = FALSE, message = paste("Error:", e$message))
  })
}

# Get allergies
get_allergies <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Allergies WHERE patient_id = %d", patient_id)
  dbGetQuery(conn, query)
}

# Add allergy
add_allergy <- function(patient_id, allergen, allergy_type, reaction, severity) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf(
    "INSERT INTO Allergies (patient_id, allergen, allergy_type, reaction, severity) 
     VALUES (%d, '%s', %s, %s, %s)",
    patient_id,
    gsub("'", "''", allergen),
    if(is.na(allergy_type) || allergy_type == "") "NULL" else paste0("'", allergy_type, "'"),
    if(is.na(reaction) || reaction == "") "NULL" else paste0("'", gsub("'", "''", reaction), "'"),
    if(is.na(severity) || severity == "") "NULL" else paste0("'", severity, "'")
  )
  
  tryCatch({
    dbExecute(conn, query)
    list(success = TRUE, message = "Allergy added successfully")
  }, error = function(e) {
    list(success = FALSE, message = paste("Error:", e$message))
  })
}

# Get medications
get_medications <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Medications WHERE patient_id = %d ORDER BY start_date DESC", patient_id)
  dbGetQuery(conn, query)
}

# Add medication
add_medication <- function(patient_id, medication_name, dosage, frequency, start_date, 
                          end_date, prescribing_doctor, notes) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf(
    "INSERT INTO Medications (patient_id, medication_name, dosage, frequency, start_date, 
     end_date, prescribing_doctor, notes) 
     VALUES (%d, '%s', %s, %s, '%s', %s, %s, %s)",
    patient_id,
    gsub("'", "''", medication_name),
    if(is.na(dosage) || dosage == "") "NULL" else paste0("'", dosage, "'"),
    if(is.na(frequency) || frequency == "") "NULL" else paste0("'", frequency, "'"),
    start_date,
    if(is.na(end_date) || end_date == "") "NULL" else paste0("'", end_date, "'"),
    if(is.na(prescribing_doctor) || prescribing_doctor == "") "NULL" else paste0("'", gsub("'", "''", prescribing_doctor), "'"),
    if(is.na(notes) || notes == "") "NULL" else paste0("'", gsub("'", "''", notes), "'")
  )
  
  tryCatch({
    dbExecute(conn, query)
    list(success = TRUE, message = "Medication added successfully")
  }, error = function(e) {
    list(success = FALSE, message = paste("Error:", e$message))
  })
}

# Get vaccinations
get_vaccinations <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Vaccinations WHERE patient_id = %d ORDER BY administration_date DESC", patient_id)
  dbGetQuery(conn, query)
}

# Add vaccination
add_vaccination <- function(patient_id, vaccine_name, administration_date, next_due_date, 
                           lot_number, administered_by) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf(
    "INSERT INTO Vaccinations (patient_id, vaccine_name, administration_date, next_due_date, 
     lot_number, administered_by) 
     VALUES (%d, '%s', '%s', %s, %s, %s)",
    patient_id,
    gsub("'", "''", vaccine_name),
    administration_date,
    if(is.na(next_due_date) || next_due_date == "") "NULL" else paste0("'", next_due_date, "'"),
    if(is.na(lot_number) || lot_number == "") "NULL" else paste0("'", lot_number, "'"),
    if(is.na(administered_by) || administered_by == "") "NULL" else paste0("'", gsub("'", "''", administered_by), "'")
  )
  
  tryCatch({
    dbExecute(conn, query)
    list(success = TRUE, message = "Vaccination added successfully")
  }, error = function(e) {
    list(success = FALSE, message = paste("Error:", e$message))
  })
}

# Get insurance
get_insurance <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Insurance WHERE patient_id = %d ORDER BY is_active DESC, effective_date DESC", patient_id)
  dbGetQuery(conn, query)
}

# Add insurance
add_insurance <- function(patient_id, provider_name, policy_number, group_number, 
                         effective_date, expiration_date, is_active) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf(
    "INSERT INTO Insurance (patient_id, provider_name, policy_number, group_number, 
     effective_date, expiration_date, is_active) 
     VALUES (%d, '%s', '%s', %s, %s, %s, %d)",
    patient_id,
    gsub("'", "''", provider_name),
    gsub("'", "''", policy_number),
    if(is.na(group_number) || group_number == "") "NULL" else paste0("'", group_number, "'"),
    if(is.na(effective_date) || effective_date == "") "NULL" else paste0("'", effective_date, "'"),
    if(is.na(expiration_date) || expiration_date == "") "NULL" else paste0("'", expiration_date, "'"),
    if(is_active) 1 else 0
  )
  
  tryCatch({
    dbExecute(conn, query)
    list(success = TRUE, message = "Insurance added successfully")
  }, error = function(e) {
    list(success = FALSE, message = paste("Error:", e$message))
  })
}

# Get emergency contacts
get_emergency_contacts <- function(patient_id) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT * FROM Emergency_Contacts WHERE patient_id = %d ORDER BY priority_order", patient_id)
  dbGetQuery(conn, query)
}

# Add emergency contact
add_emergency_contact <- function(patient_id, contact_name, relationship, phone_primary, 
                                 phone_secondary, email, priority_order) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf(
    "INSERT INTO Emergency_Contacts (patient_id, contact_name, relationship, phone_primary, 
     phone_secondary, email, priority_order) 
     VALUES (%d, '%s', %s, '%s', %s, %s, %s)",
    patient_id,
    gsub("'", "''", contact_name),
    if(is.na(relationship) || relationship == "") "NULL" else paste0("'", relationship, "'"),
    phone_primary,
    if(is.na(phone_secondary) || phone_secondary == "") "NULL" else paste0("'", phone_secondary, "'"),
    if(is.na(email) || email == "") "NULL" else paste0("'", email, "'"),
    if(is.na(priority_order) || priority_order == "") "NULL" else priority_order
  )
  
  tryCatch({
    dbExecute(conn, query)
    list(success = TRUE, message = "Emergency contact added successfully")
  }, error = function(e) {
    list(success = FALSE, message = paste("Error:", e$message))
  })
}

# =====================================================
# UI Definition
# =====================================================

ui <- fluidPage(
  useShinyjs(),
  
  tags$head(
    tags$style(HTML("
      .main-title {
        color: #1565C0;
        text-align: center;
        padding: 20px;
        background-color: #E3F2FD;
        border-radius: 5px;
        margin-bottom: 20px;
      }
      .patient-card {
        background-color: #F5F5F5;
        padding: 15px;
        border-left: 4px solid #2196F3;
        margin-bottom: 20px;
      }
      .success-box {
        background-color: #E8F5E9;
        padding: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
      }
      .error-box {
        background-color: #FFEBEE;
        padding: 10px;
        border-left: 4px solid #F44336;
        margin: 10px 0;
      }
      .info-label {
        font-weight: bold;
        color: #1565C0;
      }
    "))
  ),
  
  div(class = "main-title",
    h1("🏥 Medical Information Manager"),
    h3("License to Live: MIAS - Phase 3")
  ),
  
  # Patient Search Section
  fluidRow(
    column(12,
      wellPanel(
        h4("🔍 Step 1: Find Patient"),
        fluidRow(
          column(8,
            textInput("search_term", "Search by License Number, First Name, or Last Name:",
                     placeholder = "e.g., 10896644 or BRYAN or BARBER")
          ),
          column(4,
            br(),
            actionButton("search_btn", "Search Patients", 
                        class = "btn-primary btn-block",
                        icon = icon("search"))
          )
        ),
        DTOutput("patient_table")
      )
    )
  ),
  
  # Selected Patient Display
  uiOutput("patient_display"),
  
  # Medical Information Tabs
  uiOutput("medical_tabs")
)

# =====================================================
# Server Logic
# =====================================================

server <- function(input, output, session) {
  
  # Reactive values
  selected_patient <- reactiveVal(NULL)
  
  # Search patients
  observeEvent(input$search_btn, {
    results <- search_patients(input$search_term)
    
    output$patient_table <- renderDT({
      datatable(
        results,
        selection = 'single',
        options = list(pageLength = 10, scrollX = TRUE),
        rownames = FALSE
      )
    })
  })
  
  # Load initial patient list
  observe({
    results <- search_patients("")
    output$patient_table <- renderDT({
      datatable(
        results,
        selection = 'single',
        options = list(pageLength = 10, scrollX = TRUE),
        rownames = FALSE
      )
    })
  })
  
  # Select patient from table
  observeEvent(input$patient_table_rows_selected, {
    row_selected <- input$patient_table_rows_selected
    if (length(row_selected) > 0) {
      results <- search_patients(input$search_term)
      patient_id <- results[row_selected, "patient_id"]
      patient_data <- get_patient_details(patient_id)
      selected_patient(patient_data)
    }
  })
  
  # Display selected patient
  output$patient_display <- renderUI({
    patient <- selected_patient()
    if (is.null(patient) || nrow(patient) == 0) {
      return(NULL)
    }
    
    div(class = "patient-card",
      h4(icon("user"), " Selected Patient"),
      fluidRow(
        column(3, span(class = "info-label", "Name:"), br(), 
               paste(patient$first_name, patient$last_name)),
        column(3, span(class = "info-label", "DOB:"), br(), patient$date_of_birth),
        column(3, span(class = "info-label", "License:"), br(), patient$license_number),
        column(3, span(class = "info-label", "Blood Type:"), br(), 
               ifelse(is.na(patient$blood_type), "Not specified", patient$blood_type))
      )
    )
  })
  
  # Medical Information Tabs
  output$medical_tabs <- renderUI({
    patient <- selected_patient()
    if (is.null(patient)) {
      return(
        wellPanel(
          h4(icon("info-circle"), " Please select a patient above to manage medical information")
        )
      )
    }
    
    tabsetPanel(
      id = "medical_tabs",
      
      # Medical Conditions Tab
      tabPanel("Medical Conditions",
        br(),
        h4("📋 Medical Conditions"),
        fluidRow(
          column(6,
            wellPanel(
              h5("Add New Condition"),
              textInput("condition_name", "Condition Name:", 
                       placeholder = "e.g., Diabetes Type 2"),
              dateInput("condition_diagnosis_date", "Diagnosis Date:"),
              selectInput("condition_severity", "Severity:",
                         choices = c("", "Mild", "Moderate", "Severe", "Critical")),
              textAreaInput("condition_notes", "Notes:", rows = 3),
              actionButton("add_condition_btn", "Add Condition",
                          class = "btn-success btn-block", icon = icon("plus"))
            ),
            uiOutput("condition_status")
          ),
          column(6,
            h5("Existing Conditions"),
            DTOutput("conditions_table")
          )
        )
      ),
      
      # Allergies Tab
      tabPanel("Allergies",
        br(),
        h4("⚠️ Allergies"),
        fluidRow(
          column(6,
            wellPanel(
              h5("Add New Allergy"),
              textInput("allergen", "Allergen:", 
                       placeholder = "e.g., Penicillin"),
              selectInput("allergy_type", "Type:",
                         choices = c("", "Medication", "Food", "Environmental", "Other")),
              textInput("allergy_reaction", "Reaction:", 
                       placeholder = "e.g., Hives, Difficulty breathing"),
              selectInput("allergy_severity", "Severity:",
                         choices = c("", "Mild", "Moderate", "Severe", "Life-threatening")),
              actionButton("add_allergy_btn", "Add Allergy",
                          class = "btn-success btn-block", icon = icon("plus"))
            ),
            uiOutput("allergy_status")
          ),
          column(6,
            h5("Existing Allergies"),
            DTOutput("allergies_table")
          )
        )
      ),
      
      # Medications Tab
      tabPanel("Medications",
        br(),
        h4("💊 Medications"),
        fluidRow(
          column(6,
            wellPanel(
              h5("Add New Medication"),
              textInput("medication_name", "Medication Name:", 
                       placeholder = "e.g., Metformin"),
              textInput("medication_dosage", "Dosage:", 
                       placeholder = "e.g., 500mg"),
              textInput("medication_frequency", "Frequency:", 
                       placeholder = "e.g., Twice daily"),
              dateInput("medication_start_date", "Start Date:", value = Sys.Date()),
              dateInput("medication_end_date", "End Date (leave blank if current):"),
              textInput("medication_doctor", "Prescribing Doctor:", 
                       placeholder = "e.g., Dr. Smith"),
              textAreaInput("medication_notes", "Notes:", rows = 2),
              actionButton("add_medication_btn", "Add Medication",
                          class = "btn-success btn-block", icon = icon("plus"))
            ),
            uiOutput("medication_status")
          ),
          column(6,
            h5("Existing Medications"),
            DTOutput("medications_table")
          )
        )
      ),
      
      # Vaccinations Tab
      tabPanel("Vaccinations",
        br(),
        h4("💉 Vaccinations"),
        fluidRow(
          column(6,
            wellPanel(
              h5("Add New Vaccination"),
              textInput("vaccine_name", "Vaccine Name:", 
                       placeholder = "e.g., COVID-19, Influenza"),
              dateInput("vaccine_admin_date", "Administration Date:", value = Sys.Date()),
              dateInput("vaccine_due_date", "Next Due Date (for boosters):"),
              textInput("vaccine_lot", "Lot Number:", 
                       placeholder = "Optional"),
              textInput("vaccine_admin_by", "Administered By:", 
                       placeholder = "e.g., CVS Pharmacy"),
              actionButton("add_vaccination_btn", "Add Vaccination",
                          class = "btn-success btn-block", icon = icon("plus"))
            ),
            uiOutput("vaccination_status")
          ),
          column(6,
            h5("Vaccination History"),
            DTOutput("vaccinations_table")
          )
        )
      ),
      
      # Insurance Tab
      tabPanel("Insurance",
        br(),
        h4("🏥 Insurance Information"),
        fluidRow(
          column(6,
            wellPanel(
              h5("Add Insurance Policy"),
              textInput("insurance_provider", "Provider Name:", 
                       placeholder = "e.g., Blue Cross Blue Shield"),
              textInput("insurance_policy", "Policy Number:", 
                       placeholder = "Required"),
              textInput("insurance_group", "Group Number:", 
                       placeholder = "Optional"),
              dateInput("insurance_effective", "Effective Date:"),
              dateInput("insurance_expiration", "Expiration Date:"),
              checkboxInput("insurance_active", "Currently Active", value = TRUE),
              actionButton("add_insurance_btn", "Add Insurance",
                          class = "btn-success btn-block", icon = icon("plus"))
            ),
            uiOutput("insurance_status")
          ),
          column(6,
            h5("Insurance Policies"),
            DTOutput("insurance_table")
          )
        )
      ),
      
      # Emergency Contacts Tab
      tabPanel("Emergency Contacts",
        br(),
        h4("📞 Emergency Contacts"),
        fluidRow(
          column(6,
            wellPanel(
              h5("Add Emergency Contact"),
              textInput("contact_name", "Contact Name:", 
                       placeholder = "e.g., Jane Doe"),
              selectInput("contact_relationship", "Relationship:",
                         choices = c("", "Spouse", "Parent", "Sibling", "Child", "Friend", "Other")),
              textInput("contact_phone1", "Primary Phone:", 
                       placeholder = "Required"),
              textInput("contact_phone2", "Secondary Phone:", 
                       placeholder = "Optional"),
              textInput("contact_email", "Email:", 
                       placeholder = "Optional"),
              numericInput("contact_priority", "Priority Order:", 
                          value = 1, min = 1, max = 10),
              actionButton("add_contact_btn", "Add Contact",
                          class = "btn-success btn-block", icon = icon("plus"))
            ),
            uiOutput("contact_status")
          ),
          column(6,
            h5("Emergency Contacts"),
            DTOutput("contacts_table")
          )
        )
      )
    )
  })
  
  # Add Medical Condition
  observeEvent(input$add_condition_btn, {
    patient <- selected_patient()
    if (is.null(patient)) return()
    
    if (nchar(input$condition_name) == 0) {
      output$condition_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " Please enter a condition name")
      })
      return()
    }
    
    result <- add_condition(
      patient$patient_id,
      input$condition_name,
      input$condition_diagnosis_date,
      input$condition_severity,
      input$condition_notes
    )
    
    if (result$success) {
      output$condition_status <- renderUI({
        div(class = "success-box", icon("check-circle"), " ", result$message)
      })
      
      # Refresh table
      output$conditions_table <- renderDT({
        datatable(get_conditions(patient$patient_id), options = list(pageLength = 5))
      })
      
      # Clear form
      updateTextInput(session, "condition_name", value = "")
      updateTextAreaInput(session, "condition_notes", value = "")
    } else {
      output$condition_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " ", result$message)
      })
    }
  })
  
  # Load conditions table when patient selected
  observe({
    patient <- selected_patient()
    if (!is.null(patient)) {
      output$conditions_table <- renderDT({
        datatable(get_conditions(patient$patient_id), options = list(pageLength = 5))
      })
    }
  })
  
  # Add Allergy
  observeEvent(input$add_allergy_btn, {
    patient <- selected_patient()
    if (is.null(patient)) return()
    
    if (nchar(input$allergen) == 0) {
      output$allergy_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " Please enter an allergen")
      })
      return()
    }
    
    result <- add_allergy(
      patient$patient_id,
      input$allergen,
      input$allergy_type,
      input$allergy_reaction,
      input$allergy_severity
    )
    
    if (result$success) {
      output$allergy_status <- renderUI({
        div(class = "success-box", icon("check-circle"), " ", result$message)
      })
      
      output$allergies_table <- renderDT({
        datatable(get_allergies(patient$patient_id), options = list(pageLength = 5))
      })
      
      updateTextInput(session, "allergen", value = "")
      updateTextInput(session, "allergy_reaction", value = "")
    } else {
      output$allergy_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " ", result$message)
      })
    }
  })
  
  observe({
    patient <- selected_patient()
    if (!is.null(patient)) {
      output$allergies_table <- renderDT({
        datatable(get_allergies(patient$patient_id), options = list(pageLength = 5))
      })
    }
  })
  
  # Add Medication
  observeEvent(input$add_medication_btn, {
    patient <- selected_patient()
    if (is.null(patient)) return()
    
    if (nchar(input$medication_name) == 0) {
      output$medication_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " Please enter a medication name")
      })
      return()
    }
    
    result <- add_medication(
      patient$patient_id,
      input$medication_name,
      input$medication_dosage,
      input$medication_frequency,
      input$medication_start_date,
      input$medication_end_date,
      input$medication_doctor,
      input$medication_notes
    )
    
    if (result$success) {
      output$medication_status <- renderUI({
        div(class = "success-box", icon("check-circle"), " ", result$message)
      })
      
      output$medications_table <- renderDT({
        datatable(get_medications(patient$patient_id), options = list(pageLength = 5))
      })
      
      updateTextInput(session, "medication_name", value = "")
      updateTextInput(session, "medication_dosage", value = "")
      updateTextInput(session, "medication_frequency", value = "")
      updateTextInput(session, "medication_doctor", value = "")
      updateTextAreaInput(session, "medication_notes", value = "")
    } else {
      output$medication_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " ", result$message)
      })
    }
  })
  
  observe({
    patient <- selected_patient()
    if (!is.null(patient)) {
      output$medications_table <- renderDT({
        datatable(get_medications(patient$patient_id), options = list(pageLength = 5))
      })
    }
  })
  
  # Add Vaccination
  observeEvent(input$add_vaccination_btn, {
    patient <- selected_patient()
    if (is.null(patient)) return()
    
    if (nchar(input$vaccine_name) == 0) {
      output$vaccination_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " Please enter a vaccine name")
      })
      return()
    }
    
    result <- add_vaccination(
      patient$patient_id,
      input$vaccine_name,
      input$vaccine_admin_date,
      input$vaccine_due_date,
      input$vaccine_lot,
      input$vaccine_admin_by
    )
    
    if (result$success) {
      output$vaccination_status <- renderUI({
        div(class = "success-box", icon("check-circle"), " ", result$message)
      })
      
      output$vaccinations_table <- renderDT({
        datatable(get_vaccinations(patient$patient_id), options = list(pageLength = 5))
      })
      
      updateTextInput(session, "vaccine_name", value = "")
      updateTextInput(session, "vaccine_lot", value = "")
      updateTextInput(session, "vaccine_admin_by", value = "")
    } else {
      output$vaccination_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " ", result$message)
      })
    }
  })
  
  observe({
    patient <- selected_patient()
    if (!is.null(patient)) {
      output$vaccinations_table <- renderDT({
        datatable(get_vaccinations(patient$patient_id), options = list(pageLength = 5))
      })
    }
  })
  
  # Add Insurance
  observeEvent(input$add_insurance_btn, {
    patient <- selected_patient()
    if (is.null(patient)) return()
    
    if (nchar(input$insurance_provider) == 0 || nchar(input$insurance_policy) == 0) {
      output$insurance_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " Please enter provider name and policy number")
      })
      return()
    }
    
    result <- add_insurance(
      patient$patient_id,
      input$insurance_provider,
      input$insurance_policy,
      input$insurance_group,
      input$insurance_effective,
      input$insurance_expiration,
      input$insurance_active
    )
    
    if (result$success) {
      output$insurance_status <- renderUI({
        div(class = "success-box", icon("check-circle"), " ", result$message)
      })
      
      output$insurance_table <- renderDT({
        datatable(get_insurance(patient$patient_id), options = list(pageLength = 5))
      })
      
      updateTextInput(session, "insurance_provider", value = "")
      updateTextInput(session, "insurance_policy", value = "")
      updateTextInput(session, "insurance_group", value = "")
    } else {
      output$insurance_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " ", result$message)
      })
    }
  })
  
  observe({
    patient <- selected_patient()
    if (!is.null(patient)) {
      output$insurance_table <- renderDT({
        datatable(get_insurance(patient$patient_id), options = list(pageLength = 5))
      })
    }
  })
  
  # Add Emergency Contact
  observeEvent(input$add_contact_btn, {
    patient <- selected_patient()
    if (is.null(patient)) return()
    
    if (nchar(input$contact_name) == 0 || nchar(input$contact_phone1) == 0) {
      output$contact_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " Please enter contact name and primary phone")
      })
      return()
    }
    
    result <- add_emergency_contact(
      patient$patient_id,
      input$contact_name,
      input$contact_relationship,
      input$contact_phone1,
      input$contact_phone2,
      input$contact_email,
      input$contact_priority
    )
    
    if (result$success) {
      output$contact_status <- renderUI({
        div(class = "success-box", icon("check-circle"), " ", result$message)
      })
      
      output$contacts_table <- renderDT({
        datatable(get_emergency_contacts(patient$patient_id), options = list(pageLength = 5))
      })
      
      updateTextInput(session, "contact_name", value = "")
      updateTextInput(session, "contact_phone1", value = "")
      updateTextInput(session, "contact_phone2", value = "")
      updateTextInput(session, "contact_email", value = "")
    } else {
      output$contact_status <- renderUI({
        div(class = "error-box", icon("times-circle"), " ", result$message)
      })
    }
  })
  
  observe({
    patient <- selected_patient()
    if (!is.null(patient)) {
      output$contacts_table <- renderDT({
        datatable(get_emergency_contacts(patient$patient_id), options = list(pageLength = 5))
      })
    }
  })
}

# =====================================================
# Run the application
# =====================================================

shinyApp(ui = ui, server = server)
