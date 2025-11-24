# =====================================================
# License to Live: MIAS - Patient Registration App
# Shiny Application with Barcode Scanner Integration
# =====================================================

library(shiny)
library(DBI)
library(RMySQL)
library(shinyjs)

# Source the AAMVA parser
source("aamva_parser.R")

# Database connection configuration
db_config <- list(
  host = "mias-db.chwakwqqclzv.us-east-2.rds.amazonaws.com",
  port = 3306,
  user = "admin",
  password = "License2Live",
  dbname = "mias_db"
)

# =====================================================
# Helper Functions
# =====================================================

#' Connect to the database
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

#' Check if license number already exists
license_exists <- function(license_number) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- sprintf("SELECT COUNT(*) as count FROM Patients WHERE license_number = '%s'", 
                   license_number)
  result <- dbGetQuery(conn, query)
  return(result$count > 0)
}

#' Insert patient into database
insert_patient <- function(patient_data) {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  # Build INSERT query
  fields <- paste(names(patient_data), collapse = ", ")
  
  # Prepare values - handle NAs and quote strings
  values <- sapply(patient_data, function(x) {
    if (is.na(x)) {
      return("NULL")
    } else {
      return(paste0("'", gsub("'", "''", as.character(x)), "'"))
    }
  })
  values_str <- paste(values, collapse = ", ")
  
  query <- sprintf("INSERT INTO Patients (%s) VALUES (%s)", fields, values_str)
  
  tryCatch({
    dbExecute(conn, query)
    return(list(success = TRUE, message = "Patient registered successfully!"))
  }, error = function(e) {
    return(list(success = FALSE, message = paste("Database error:", e$message)))
  })
}

# =====================================================
# UI Definition
# =====================================================

ui <- fluidPage(
  useShinyjs(),
  
  # Custom CSS
  tags$head(
    tags$style(HTML("
      .main-title {
        color: #2E7D32;
        text-align: center;
        padding: 20px;
        background-color: #E8F5E9;
        border-radius: 5px;
        margin-bottom: 30px;
      }
      .scan-box {
        border: 3px dashed #2196F3;
        padding: 20px;
        margin: 20px 0;
        background-color: #E3F2FD;
        border-radius: 5px;
      }
      .parsed-data {
        background-color: #F5F5F5;
        padding: 15px;
        border-left: 4px solid #4CAF50;
        font-family: monospace;
        white-space: pre-wrap;
      }
      .error-box {
        background-color: #FFEBEE;
        padding: 15px;
        border-left: 4px solid #F44336;
        margin: 10px 0;
      }
      .success-box {
        background-color: #E8F5E9;
        padding: 15px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
      }
      .warning-box {
        background-color: #FFF3E0;
        padding: 15px;
        border-left: 4px solid #FF9800;
        margin: 10px 0;
      }
    "))
  ),
  
  # Title
  div(class = "main-title",
    h1("🏥 License to Live: MIAS"),
    h3("Patient Registration - Barcode Scanner")
  ),
  
  # Main content
  fluidRow(
    column(12,
      # Instructions
      wellPanel(
        h4("📋 Instructions:"),
        tags$ol(
          tags$li("Click in the 'Barcode Input' field below"),
          tags$li("Scan the driver's license 2D barcode with your Eyoyo scanner"),
          tags$li("Data will automatically populate and parse"),
          tags$li("Review the parsed information"),
          tags$li("Add missing information (phone, email, blood type)"),
          tags$li("Click 'Register Patient' to save to database")
        )
      )
    )
  ),
  
  fluidRow(
    # Left column - Scanner input
    column(6,
      div(class = "scan-box",
        h4("🔍 Step 1: Scan Driver's License"),
        helpText(
          icon("info-circle"),
          " The Eyoyo scanner outputs @ symbol and line breaks. This is normal - the parser will clean it automatically."
        ),
        textAreaInput("barcode_input", 
                     "Barcode Input:",
                     value = "",
                     rows = 8,
                     placeholder = "Click here and scan driver's license...\n\nScanner will output:\n@\n[barcode data with line breaks]\n\nThis is normal!"),
        actionButton("parse_btn", "Parse Barcode", 
                    class = "btn-primary btn-lg btn-block",
                    icon = icon("qrcode"))
      ),
      
      # Status messages
      uiOutput("status_message")
    ),
    
    # Right column - Parsed data display
    column(6,
      h4("📄 Step 2: Review Parsed Data"),
      verbatimTextOutput("parsed_display"),
      
      # Additional fields not in barcode
      wellPanel(
        h5("Additional Information (Optional)"),
        textInput("phone", "Phone Number:", 
                 placeholder = "e.g., 972-555-0100"),
        textInput("email", "Email Address:", 
                 placeholder = "e.g., patient@email.com"),
        selectInput("blood_type", "Blood Type:",
                   choices = c("", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"),
                   selected = "")
      )
    )
  ),
  
  fluidRow(
    column(12,
      # Action buttons
      wellPanel(
        h4("📥 Step 3: Save to Database"),
        fluidRow(
          column(6,
            actionButton("register_btn", 
                        "Register Patient",
                        class = "btn-success btn-lg btn-block",
                        icon = icon("user-plus"))
          ),
          column(6,
            actionButton("clear_btn", 
                        "Clear Form",
                        class = "btn-warning btn-lg btn-block",
                        icon = icon("eraser"))
          )
        )
      )
    )
  )
)

# =====================================================
# Server Logic
# =====================================================

server <- function(input, output, session) {
  
  # Reactive values to store parsed data
  parsed_data <- reactiveVal(NULL)
  
  # Parse barcode when button clicked
  observeEvent(input$parse_btn, {
    
    if (nchar(input$barcode_input) == 0) {
      output$status_message <- renderUI({
        div(class = "warning-box",
          icon("exclamation-triangle"),
          " Please scan a barcode first!"
        )
      })
      return()
    }
    
    # Parse the barcode
    result <- parse_aamva_barcode(input$barcode_input)
    
    if (result$parsed) {
      parsed_data(result)
      
      # Display success message
      output$status_message <- renderUI({
        div(class = "success-box",
          icon("check-circle"),
          " Barcode parsed successfully!"
        )
      })
      
      # Check if license already exists
      if (license_exists(result$fields$license_number)) {
        output$status_message <- renderUI({
          div(class = "warning-box",
            icon("exclamation-triangle"),
            strong(" Warning: "),
            "This license number already exists in the database!",
            br(),
            "License Number: ", result$fields$license_number
          )
        })
        shinyjs::disable("register_btn")
      } else {
        shinyjs::enable("register_btn")
      }
      
    } else {
      output$status_message <- renderUI({
        div(class = "error-box",
          icon("times-circle"),
          " Error parsing barcode: ",
          result$error
        )
      })
      parsed_data(NULL)
    }
  })
  
  # Display parsed data
  output$parsed_display <- renderText({
    if (is.null(parsed_data())) {
      return("No data parsed yet. Scan a barcode to begin.")
    }
    
    format_parsed_data(parsed_data())
  })
  
  # Register patient button
  observeEvent(input$register_btn, {
    
    if (is.null(parsed_data())) {
      output$status_message <- renderUI({
        div(class = "error-box",
          icon("times-circle"),
          " Please parse a barcode first!"
        )
      })
      return()
    }
    
    # Prepare data for database
    patient_data <- prepare_for_database(parsed_data())
    
    # Add optional fields
    if (nchar(input$phone) > 0) {
      patient_data$phone <- input$phone
    }
    if (nchar(input$email) > 0) {
      patient_data$email <- input$email
    }
    if (nchar(input$blood_type) > 0) {
      patient_data$blood_type <- input$blood_type
    }
    
    # Insert into database
    result <- insert_patient(patient_data)
    
    if (result$success) {
      output$status_message <- renderUI({
        div(class = "success-box",
          icon("check-circle"),
          strong(" Success! "),
          result$message,
          br(),
          "Patient: ", patient_data$first_name, " ", patient_data$last_name,
          br(),
          "License: ", patient_data$license_number
        )
      })
      
      # Clear form after successful registration
      Sys.sleep(2)
      updateTextAreaInput(session, "barcode_input", value = "")
      updateTextInput(session, "phone", value = "")
      updateTextInput(session, "email", value = "")
      updateSelectInput(session, "blood_type", selected = "")
      parsed_data(NULL)
      
    } else {
      output$status_message <- renderUI({
        div(class = "error-box",
          icon("times-circle"),
          " Registration failed: ",
          result$message
        )
      })
    }
  })
  
  # Clear form button
  observeEvent(input$clear_btn, {
    updateTextAreaInput(session, "barcode_input", value = "")
    updateTextInput(session, "phone", value = "")
    updateTextInput(session, "email", value = "")
    updateSelectInput(session, "blood_type", selected = "")
    parsed_data(NULL)
    
    output$status_message <- renderUI({
      div(class = "warning-box",
        icon("info-circle"),
        " Form cleared. Ready for next patient."
      )
    })
    
    shinyjs::enable("register_btn")
  })
}

# =====================================================
# Run the application
# =====================================================

shinyApp(ui = ui, server = server)
