# =====================================================
# License to Live: MIAS - Analytics Dashboard
# Phase 4: Data Analysis & Visualization
# =====================================================

library(shiny)
library(DBI)
library(RMySQL)
library(ggplot2)
library(dplyr)
library(scales)
library(gridExtra)

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

# Get vaccination coverage data
get_vaccination_data <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- "
    SELECT 
      vaccine_name,
      COUNT(DISTINCT patient_id) as patients_vaccinated,
      COUNT(vaccination_id) as total_doses,
      MIN(administration_date) as first_dose_date,
      MAX(administration_date) as last_dose_date
    FROM Vaccinations
    GROUP BY vaccine_name
    ORDER BY patients_vaccinated DESC
  "
  
  dbGetQuery(conn, query)
}

# Get patient demographics
get_patient_demographics <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- "
    SELECT 
      patient_id,
      TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) as age,
      state,
      blood_type
    FROM Patients
  "
  
  dbGetQuery(conn, query)
}

# Get medication statistics
get_medication_stats <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- "
    SELECT 
      medication_name,
      COUNT(DISTINCT patient_id) as patient_count,
      COUNT(medication_id) as prescription_count
    FROM Medications
    GROUP BY medication_name
    ORDER BY patient_count DESC
    LIMIT 10
  "
  
  dbGetQuery(conn, query)
}

# Get allergy severity distribution
get_allergy_stats <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- "
    SELECT 
      severity,
      allergy_type,
      COUNT(*) as count
    FROM Allergies
    WHERE severity IS NOT NULL
    GROUP BY severity, allergy_type
    ORDER BY 
      FIELD(severity, 'Life-threatening', 'Severe', 'Moderate', 'Mild'),
      count DESC
  "
  
  dbGetQuery(conn, query)
}

# Get system summary statistics
get_summary_stats <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  queries <- list(
    total_patients = "SELECT COUNT(*) as count FROM Patients",
    total_conditions = "SELECT COUNT(*) as count FROM Medical_Conditions",
    total_allergies = "SELECT COUNT(*) as count FROM Allergies",
    total_medications = "SELECT COUNT(*) as count FROM Medications WHERE end_date IS NULL",
    total_vaccinations = "SELECT COUNT(*) as count FROM Vaccinations",
    total_insurance = "SELECT COUNT(*) as count FROM Insurance WHERE is_active = TRUE",
    total_contacts = "SELECT COUNT(*) as count FROM Emergency_Contacts",
    avg_age = "SELECT ROUND(AVG(TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())), 1) as avg_age FROM Patients"
  )
  
  stats <- lapply(queries, function(q) dbGetQuery(conn, q))
  
  list(
    total_patients = stats$total_patients$count,
    total_conditions = stats$total_conditions$count,
    total_allergies = stats$total_allergies$count,
    active_medications = stats$total_medications$count,
    total_vaccinations = stats$total_vaccinations$count,
    active_insurance = stats$total_insurance$count,
    emergency_contacts = stats$total_contacts$count,
    avg_age = stats$avg_age$avg_age
  )
}

# Get geographic distribution
get_state_distribution <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- "
    SELECT 
      state,
      COUNT(*) as patient_count
    FROM Patients
    WHERE state IS NOT NULL AND state != ''
    GROUP BY state
    ORDER BY patient_count DESC
  "
  
  dbGetQuery(conn, query)
}

# Get blood type distribution
get_blood_type_distribution <- function() {
  conn <- get_db_connection()
  on.exit(dbDisconnect(conn))
  
  query <- "
    SELECT 
      blood_type,
      COUNT(*) as count
    FROM Patients
    WHERE blood_type IS NOT NULL AND blood_type != ''
    GROUP BY blood_type
    ORDER BY count DESC
  "
  
  dbGetQuery(conn, query)
}

# =====================================================
# UI Definition
# =====================================================

ui <- fluidPage(
  
  tags$head(
    tags$style(HTML("
      .main-title {
        color: #FFFFFF;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      }
      .stat-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
      }
      .stat-number {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
      }
      .stat-label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
      }
      .chart-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
      }
      .info-box {
        background-color: #E3F2FD;
        padding: 15px;
        border-left: 4px solid #2196F3;
        margin-bottom: 20px;
      }
    "))
  ),
  
  div(class = "main-title",
    h1("📊 Analytics Dashboard"),
    h3("License to Live: MIAS - Phase 4")
  ),
  
  # Refresh button
  fluidRow(
    column(12,
      div(class = "info-box",
        icon("info-circle"),
        " This dashboard displays real-time analytics from your MIAS database. ",
        actionButton("refresh_btn", "Refresh Data", 
                    icon = icon("sync"),
                    style = "float: right; background-color: #2196F3; color: white;")
      )
    )
  ),
  
  # Summary Statistics
  fluidRow(
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_patients")),
        div(class = "stat-label", "Total Patients")
      )
    ),
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_conditions")),
        div(class = "stat-label", "Medical Conditions")
      )
    ),
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_medications")),
        div(class = "stat-label", "Active Medications")
      )
    ),
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_vaccinations")),
        div(class = "stat-label", "Vaccinations Given")
      )
    )
  ),
  
  fluidRow(
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_allergies")),
        div(class = "stat-label", "Known Allergies")
      )
    ),
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_insurance")),
        div(class = "stat-label", "Active Insurance Policies")
      )
    ),
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_contacts")),
        div(class = "stat-label", "Emergency Contacts")
      )
    ),
    column(3,
      div(class = "stat-box",
        div(class = "stat-number", textOutput("stat_avg_age")),
        div(class = "stat-label", "Average Patient Age")
      )
    )
  ),
  
  # Analytics Tabs
  tabsetPanel(
    
    # Vaccination Coverage Tab
    tabPanel("💉 Vaccination Coverage",
      br(),
      fluidRow(
        column(12,
          div(class = "chart-container",
            h4("Vaccination Coverage Analysis"),
            p("This chart shows the number of patients vaccinated for each vaccine type and total doses administered."),
            plotOutput("vaccination_chart", height = "500px")
          )
        )
      )
    ),
    
    # Patient Demographics Tab
    tabPanel("👥 Patient Demographics",
      br(),
      fluidRow(
        column(6,
          div(class = "chart-container",
            h4("Age Distribution"),
            p("Distribution of patient ages in the system."),
            plotOutput("age_distribution_chart", height = "400px")
          )
        ),
        column(6,
          div(class = "chart-container",
            h4("Blood Type Distribution"),
            p("Breakdown of blood types among registered patients."),
            plotOutput("blood_type_chart", height = "400px")
          )
        )
      ),
      fluidRow(
        column(12,
          div(class = "chart-container",
            h4("Geographic Distribution"),
            p("Patient distribution by state."),
            plotOutput("state_distribution_chart", height = "400px")
          )
        )
      )
    ),
    
    # Medication Analysis Tab
    tabPanel("💊 Medication Trends",
      br(),
      fluidRow(
        column(12,
          div(class = "chart-container",
            h4("Top 10 Most Prescribed Medications"),
            p("Medications most commonly prescribed to patients in the system."),
            plotOutput("medication_chart", height = "500px")
          )
        )
      )
    ),
    
    # Allergy Analysis Tab
    tabPanel("⚠️ Allergy Analysis",
      br(),
      fluidRow(
        column(12,
          div(class = "chart-container",
            h4("Allergy Severity Distribution"),
            p("Breakdown of allergies by severity level and type. Critical for emergency preparedness."),
            plotOutput("allergy_chart", height = "500px")
          )
        )
      )
    ),
    
    # Comprehensive Report Tab
    tabPanel("📈 Comprehensive Report",
      br(),
      fluidRow(
        column(12,
          div(class = "chart-container",
            h4("System Overview - All Visualizations"),
            p("Combined view of all analytics for presentation and reporting."),
            plotOutput("comprehensive_report", height = "1200px")
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
  
  # Reactive data that updates on refresh
  summary_stats <- reactiveVal()
  vaccination_data <- reactiveVal()
  demographics_data <- reactiveVal()
  medication_data <- reactiveVal()
  allergy_data <- reactiveVal()
  state_data <- reactiveVal()
  blood_type_data <- reactiveVal()
  
  # Load data on startup
  observe({
    summary_stats(get_summary_stats())
    vaccination_data(get_vaccination_data())
    demographics_data(get_patient_demographics())
    medication_data(get_medication_stats())
    allergy_data(get_allergy_stats())
    state_data(get_state_distribution())
    blood_type_data(get_blood_type_distribution())
  })
  
  # Refresh data button
  observeEvent(input$refresh_btn, {
    summary_stats(get_summary_stats())
    vaccination_data(get_vaccination_data())
    demographics_data(get_patient_demographics())
    medication_data(get_medication_stats())
    allergy_data(get_allergy_stats())
    state_data(get_state_distribution())
    blood_type_data(get_blood_type_distribution())
    
    showNotification("Data refreshed!", type = "message", duration = 3)
  })
  
  # Summary Statistics Outputs
  output$stat_patients <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$total_patients, big.mark = ",") else "0"
  })
  
  output$stat_conditions <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$total_conditions, big.mark = ",") else "0"
  })
  
  output$stat_medications <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$active_medications, big.mark = ",") else "0"
  })
  
  output$stat_vaccinations <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$total_vaccinations, big.mark = ",") else "0"
  })
  
  output$stat_allergies <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$total_allergies, big.mark = ",") else "0"
  })
  
  output$stat_insurance <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$active_insurance, big.mark = ",") else "0"
  })
  
  output$stat_contacts <- renderText({
    stats <- summary_stats()
    if (!is.null(stats)) format(stats$emergency_contacts, big.mark = ",") else "0"
  })
  
  output$stat_avg_age <- renderText({
    stats <- summary_stats()
    if (!is.null(stats) && !is.na(stats$avg_age)) {
      paste0(round(stats$avg_age, 1), " yrs")
    } else {
      "N/A"
    }
  })
  
  # Vaccination Coverage Chart
  output$vaccination_chart <- renderPlot({
    data <- vaccination_data()
    
    if (is.null(data) || nrow(data) == 0) {
      return(ggplot() + 
        annotate("text", x = 0.5, y = 0.5, 
                label = "No vaccination data available.\nAdd vaccinations using the Medical Information Manager.",
                size = 6, color = "gray50") +
        theme_void())
    }
    
    # Create side-by-side bar chart
    p1 <- ggplot(data, aes(x = reorder(vaccine_name, patients_vaccinated), y = patients_vaccinated)) +
      geom_bar(stat = "identity", fill = "#4CAF50", alpha = 0.8) +
      geom_text(aes(label = patients_vaccinated), hjust = -0.2, size = 4) +
      coord_flip() +
      labs(title = "Patients Vaccinated by Vaccine Type",
           x = "",
           y = "Number of Patients") +
      theme_minimal(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16),
            axis.text.y = element_text(size = 12))
    
    p2 <- ggplot(data, aes(x = reorder(vaccine_name, total_doses), y = total_doses)) +
      geom_bar(stat = "identity", fill = "#2196F3", alpha = 0.8) +
      geom_text(aes(label = total_doses), hjust = -0.2, size = 4) +
      coord_flip() +
      labs(title = "Total Doses Administered",
           x = "",
           y = "Number of Doses") +
      theme_minimal(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16),
            axis.text.y = element_text(size = 12))
    
    grid.arrange(p1, p2, ncol = 2)
  })
  
  # Age Distribution Chart
  output$age_distribution_chart <- renderPlot({
    data <- demographics_data()
    
    if (is.null(data) || nrow(data) == 0) {
      return(ggplot() + 
        annotate("text", x = 0.5, y = 0.5, label = "No patient data available", size = 6) +
        theme_void())
    }
    
    ggplot(data, aes(x = age)) +
      geom_histogram(binwidth = 5, fill = "#667eea", color = "white", alpha = 0.8) +
      geom_vline(aes(xintercept = mean(age, na.rm = TRUE)), 
                color = "#e74c3c", linetype = "dashed", size = 1) +
      labs(title = "Patient Age Distribution",
           subtitle = paste("Average Age:", round(mean(data$age, na.rm = TRUE), 1), "years"),
           x = "Age (years)",
           y = "Number of Patients") +
      theme_minimal(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16),
            plot.subtitle = element_text(color = "#e74c3c"))
  })
  
  # Blood Type Chart
  output$blood_type_chart <- renderPlot({
    data <- blood_type_data()
    
    if (is.null(data) || nrow(data) == 0) {
      return(ggplot() + 
        annotate("text", x = 0.5, y = 0.5, label = "No blood type data available", size = 6) +
        theme_void())
    }
    
    ggplot(data, aes(x = "", y = count, fill = blood_type)) +
      geom_bar(stat = "identity", width = 1, color = "white") +
      coord_polar("y", start = 0) +
      geom_text(aes(label = paste0(blood_type, "\n", count)), 
               position = position_stack(vjust = 0.5),
               color = "white", fontface = "bold", size = 4) +
      scale_fill_brewer(palette = "Set3") +
      labs(title = "Blood Type Distribution",
           fill = "Blood Type") +
      theme_void(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
            legend.position = "right")
  })
  
  # State Distribution Chart
  output$state_distribution_chart <- renderPlot({
    data <- state_data()
    
    if (is.null(data) || nrow(data) == 0) {
      return(ggplot() + 
        annotate("text", x = 0.5, y = 0.5, label = "No state data available", size = 6) +
        theme_void())
    }
    
    ggplot(data, aes(x = reorder(state, patient_count), y = patient_count)) +
      geom_bar(stat = "identity", fill = "#FF9800", alpha = 0.8) +
      geom_text(aes(label = patient_count), hjust = -0.2, size = 4) +
      coord_flip() +
      labs(title = "Patient Distribution by State",
           x = "State",
           y = "Number of Patients") +
      theme_minimal(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16))
  })
  
  # Medication Chart
  output$medication_chart <- renderPlot({
    data <- medication_data()
    
    if (is.null(data) || nrow(data) == 0) {
      return(ggplot() + 
        annotate("text", x = 0.5, y = 0.5, 
                label = "No medication data available.\nAdd medications using the Medical Information Manager.",
                size = 6, color = "gray50") +
        theme_void())
    }
    
    ggplot(data, aes(x = reorder(medication_name, patient_count), y = patient_count)) +
      geom_bar(stat = "identity", fill = "#9C27B0", alpha = 0.8) +
      geom_text(aes(label = patient_count), hjust = -0.2, size = 4) +
      coord_flip() +
      labs(title = "Top 10 Most Prescribed Medications",
           subtitle = "Number of patients prescribed each medication",
           x = "",
           y = "Number of Patients") +
      theme_minimal(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16),
            axis.text.y = element_text(size = 12))
  })
  
  # Allergy Chart
  output$allergy_chart <- renderPlot({
    data <- allergy_data()
    
    if (is.null(data) || nrow(data) == 0) {
      return(ggplot() + 
        annotate("text", x = 0.5, y = 0.5, 
                label = "No allergy data available.\nAdd allergies using the Medical Information Manager.",
                size = 6, color = "gray50") +
        theme_void())
    }
    
    # Define severity order and colors
    severity_order <- c("Life-threatening", "Severe", "Moderate", "Mild")
    severity_colors <- c("Life-threatening" = "#e74c3c", 
                        "Severe" = "#e67e22",
                        "Moderate" = "#f39c12",
                        "Mild" = "#3498db")
    
    data$severity <- factor(data$severity, levels = severity_order)
    
    ggplot(data, aes(x = allergy_type, y = count, fill = severity)) +
      geom_bar(stat = "identity", position = "dodge", alpha = 0.9) +
      geom_text(aes(label = count), position = position_dodge(width = 0.9), 
               vjust = -0.5, size = 3.5) +
      scale_fill_manual(values = severity_colors) +
      labs(title = "Allergy Distribution by Type and Severity",
           subtitle = "Critical information for emergency response",
           x = "Allergy Type",
           y = "Number of Allergies",
           fill = "Severity") +
      theme_minimal(base_size = 14) +
      theme(plot.title = element_text(face = "bold", size = 16),
            axis.text.x = element_text(angle = 45, hjust = 1),
            legend.position = "right")
  })
  
  # Comprehensive Report
  output$comprehensive_report <- renderPlot({
    # Create all plots
    vacc_data <- vaccination_data()
    demo_data <- demographics_data()
    med_data <- medication_data()
    allergy_data_plot <- allergy_data()
    
    plots <- list()
    
    # Plot 1: Vaccination Coverage
    if (!is.null(vacc_data) && nrow(vacc_data) > 0) {
      p1 <- ggplot(vacc_data, aes(x = reorder(vaccine_name, patients_vaccinated), 
                                  y = patients_vaccinated)) +
        geom_bar(stat = "identity", fill = "#4CAF50", alpha = 0.8) +
        coord_flip() +
        labs(title = "Vaccination Coverage", x = "", y = "Patients") +
        theme_minimal(base_size = 10)
      plots[[length(plots) + 1]] <- p1
    }
    
    # Plot 2: Age Distribution
    if (!is.null(demo_data) && nrow(demo_data) > 0) {
      p2 <- ggplot(demo_data, aes(x = age)) +
        geom_histogram(binwidth = 5, fill = "#667eea", alpha = 0.8) +
        labs(title = "Age Distribution", x = "Age", y = "Count") +
        theme_minimal(base_size = 10)
      plots[[length(plots) + 1]] <- p2
    }
    
    # Plot 3: Medication Trends
    if (!is.null(med_data) && nrow(med_data) > 0) {
      p3 <- ggplot(med_data, aes(x = reorder(medication_name, patient_count), 
                                 y = patient_count)) +
        geom_bar(stat = "identity", fill = "#9C27B0", alpha = 0.8) +
        coord_flip() +
        labs(title = "Top Medications", x = "", y = "Patients") +
        theme_minimal(base_size = 10)
      plots[[length(plots) + 1]] <- p3
    }
    
    # Plot 4: Allergy Severity
    if (!is.null(allergy_data_plot) && nrow(allergy_data_plot) > 0) {
      severity_order <- c("Life-threatening", "Severe", "Moderate", "Mild")
      allergy_data_plot$severity <- factor(allergy_data_plot$severity, levels = severity_order)
      
      p4 <- ggplot(allergy_data_plot, aes(x = allergy_type, y = count, fill = severity)) +
        geom_bar(stat = "identity", position = "dodge", alpha = 0.9) +
        scale_fill_manual(values = c("Life-threatening" = "#e74c3c", 
                                     "Severe" = "#e67e22",
                                     "Moderate" = "#f39c12",
                                     "Mild" = "#3498db")) +
        labs(title = "Allergy Severity", x = "", y = "Count") +
        theme_minimal(base_size = 10) +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
      plots[[length(plots) + 1]] <- p4
    }
    
    # Arrange plots
    if (length(plots) > 0) {
      do.call(grid.arrange, c(plots, ncol = 2))
    } else {
      ggplot() + 
        annotate("text", x = 0.5, y = 0.5, 
                label = "Add medical data to see comprehensive analytics",
                size = 8, color = "gray50") +
        theme_void()
    }
  })
}

# =====================================================
# Run the application
# =====================================================

shinyApp(ui = ui, server = server)
