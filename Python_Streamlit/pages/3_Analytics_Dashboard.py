"""
Analytics Dashboard Page
License to Live: MIAS - Python/Streamlit Version
Real-time data visualization and insights
"""

import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard - MIAS",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Analytics Dashboard")
st.markdown("### Real-time Data Visualization & Insights")

# Refresh button
col1, col2, col3 = st.columns([4, 1, 1])
with col3:
    if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# Get summary statistics
stats = db.get_summary_stats()

# Summary Statistics Cards
st.markdown("### 📈 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Patients",
        value=f"{stats.get('total_patients', 0):,}"
    )

with col2:
    st.metric(
        label="🩺 Medical Conditions",
        value=f"{stats.get('total_conditions', 0):,}"
    )

with col3:
    st.metric(
        label="💊 Active Medications",
        value=f"{stats.get('active_medications', 0):,}"
    )

with col4:
    st.metric(
        label="💉 Vaccinations Given",
        value=f"{stats.get('total_vaccinations', 0):,}"
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="⚠️ Known Allergies",
        value=f"{stats.get('total_allergies', 0):,}"
    )

with col2:
    st.metric(
        label="🏥 Active Insurance",
        value=f"{stats.get('active_insurance', 0):,}"
    )

with col3:
    st.metric(
        label="📞 Emergency Contacts",
        value=f"{stats.get('emergency_contacts', 0):,}"
    )

with col4:
    avg_age = stats.get('avg_age', 0)
    st.metric(
        label="📅 Average Patient Age",
        value=f"{avg_age:.1f} yrs" if avg_age else "N/A"
    )

st.markdown("---")

# Tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💉 Vaccination Coverage",
    "👥 Patient Demographics",
    "💊 Medication Trends",
    "⚠️ Allergy Analysis",
    "📈 Comprehensive Report"
])

# TAB 1: Vaccination Coverage
with tab1:
    st.subheader("Vaccination Coverage Analysis")
    
    vacc_df = db.get_vaccination_data()
    
    if not vacc_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Patients vaccinated chart
            fig1 = px.bar(
                vacc_df,
                x='vaccine_name',
                y='patients_vaccinated',
                title="Patients Vaccinated by Vaccine Type",
                labels={'vaccine_name': 'Vaccine', 'patients_vaccinated': 'Number of Patients'},
                color='patients_vaccinated',
                color_continuous_scale='Greens'
            )
            fig1.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Total doses chart
            fig2 = px.bar(
                vacc_df,
                x='vaccine_name',
                y='total_doses',
                title="Total Doses Administered",
                labels={'vaccine_name': 'Vaccine', 'total_doses': 'Number of Doses'},
                color='total_doses',
                color_continuous_scale='Blues'
            )
            fig2.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Data table
        st.markdown("#### Vaccination Data Table")
        st.dataframe(vacc_df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ No vaccination data available. Add vaccinations using the Medical Information Manager.")

# TAB 2: Patient Demographics
with tab2:
    st.subheader("Patient Demographics")
    
    demo_df = db.get_patient_demographics()
    
    if not demo_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            st.markdown("#### Age Distribution")
            fig3 = px.histogram(
                demo_df,
                x='age',
                nbins=15,
                title="Patient Age Distribution",
                labels={'age': 'Age (years)', 'count': 'Number of Patients'},
                color_discrete_sequence=['#667eea']
            )
            fig3.add_vline(
                x=demo_df['age'].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Avg: {demo_df['age'].mean():.1f} years",
                annotation_position="top"
            )
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Blood type distribution
            st.markdown("#### Blood Type Distribution")
            blood_df = db.get_blood_type_distribution()
            
            if not blood_df.empty:
                fig4 = px.pie(
                    blood_df,
                    values='count',
                    names='blood_type',
                    title="Blood Type Breakdown",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig4.update_layout(height=400)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No blood type data available")
        
        # Geographic distribution
        st.markdown("#### Geographic Distribution")
        state_df = db.get_state_distribution()
        
        if not state_df.empty:
            fig5 = px.bar(
                state_df,
                x='patient_count',
                y='state',
                orientation='h',
                title="Patient Distribution by State",
                labels={'patient_count': 'Number of Patients', 'state': 'State'},
                color='patient_count',
                color_continuous_scale='Oranges'
            )
            fig5.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("No geographic data available")
    else:
        st.info("ℹ️ No patient demographic data available.")

# TAB 3: Medication Trends
with tab3:
    st.subheader("Top 10 Most Prescribed Medications")
    
    med_df = db.get_medication_stats()
    
    if not med_df.empty:
        fig6 = px.bar(
            med_df,
            x='patient_count',
            y='medication_name',
            orientation='h',
            title="Most Commonly Prescribed Medications",
            labels={'patient_count': 'Number of Patients', 'medication_name': 'Medication'},
            color='patient_count',
            color_continuous_scale='Purples',
            text='patient_count'
        )
        fig6.update_traces(textposition='outside')
        fig6.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)
        
        # Insights
        st.markdown("#### 💡 Insights")
        if len(med_df) > 0:
            top_med = med_df.iloc[0]
            st.info(f"""
            **Most Prescribed:** {top_med['medication_name']} ({top_med['patient_count']} patients)
            
            This indicates common treatment patterns in your patient population.
            """)
        
        # Data table
        st.markdown("#### Medication Data Table")
        st.dataframe(med_df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ No medication data available. Add medications using the Medical Information Manager.")

# TAB 4: Allergy Analysis
with tab4:
    st.subheader("Allergy Severity Distribution")
    
    allergy_df = db.get_allergy_stats()
    
    if not allergy_df.empty:
        # Create grouped bar chart
        fig7 = px.bar(
            allergy_df,
            x='allergy_type',
            y='count',
            color='severity',
            barmode='group',
            title="Allergies by Type and Severity",
            labels={'allergy_type': 'Allergy Type', 'count': 'Number of Allergies', 'severity': 'Severity'},
            color_discrete_map={
                'Life-threatening': '#e74c3c',
                'Severe': '#e67e22',
                'Moderate': '#f39c12',
                'Mild': '#3498db'
            },
            category_orders={'severity': ['Life-threatening', 'Severe', 'Moderate', 'Mild']}
        )
        fig7.update_layout(height=500)
        st.plotly_chart(fig7, use_container_width=True)
        
        # Critical allergies alert
        life_threatening = allergy_df[allergy_df['severity'] == 'Life-threatening']
        if not life_threatening.empty:
            total_lt = life_threatening['count'].sum()
            st.error(f"""
            ⚠️ **CRITICAL ALERT:** {total_lt} life-threatening allergies recorded!
            
            These require immediate attention in emergency situations.
            """)
        
        # Data table
        st.markdown("#### Allergy Data Table")
        st.dataframe(allergy_df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ No allergy data available. Add allergies using the Medical Information Manager.")

# TAB 5: Comprehensive Report
with tab5:
    st.subheader("Comprehensive Analytics Report")
    st.markdown("All visualizations in one view for presentations and reporting")
    
    # Check if we have data
    has_vacc = not db.get_vaccination_data().empty
    has_demo = not db.get_patient_demographics().empty
    has_meds = not db.get_medication_stats().empty
    has_allergy = not db.get_allergy_stats().empty
    
    if has_vacc or has_demo or has_meds or has_allergy:
        # Create 2x2 grid of charts
        col1, col2 = st.columns(2)
        
        with col1:
            if has_vacc:
                vacc_df = db.get_vaccination_data()
                fig_v = px.bar(
                    vacc_df,
                    x='vaccine_name',
                    y='patients_vaccinated',
                    title="Vaccination Coverage",
                    color_discrete_sequence=['#4CAF50']
                )
                fig_v.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_v, use_container_width=True)
            
            if has_demo:
                demo_df = db.get_patient_demographics()
                fig_d = px.histogram(
                    demo_df,
                    x='age',
                    nbins=10,
                    title="Age Distribution",
                    color_discrete_sequence=['#667eea']
                )
                fig_d.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_d, use_container_width=True)
        
        with col2:
            if has_meds:
                med_df = db.get_medication_stats()
                fig_m = px.bar(
                    med_df.head(5),
                    x='patient_count',
                    y='medication_name',
                    orientation='h',
                    title="Top 5 Medications",
                    color_discrete_sequence=['#9C27B0']
                )
                fig_m.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_m, use_container_width=True)
            
            if has_allergy:
                allergy_df = db.get_allergy_stats()
                fig_a = px.bar(
                    allergy_df,
                    x='allergy_type',
                    y='count',
                    color='severity',
                    title="Allergy Severity",
                    color_discrete_map={
                        'Life-threatening': '#e74c3c',
                        'Severe': '#e67e22',
                        'Moderate': '#f39c12',
                        'Mild': '#3498db'
                    }
                )
                fig_a.update_layout(height=350)
                st.plotly_chart(fig_a, use_container_width=True)
        
        # Export button
        st.markdown("---")
        st.markdown("💡 **Tip:** Right-click any chart to download as PNG for your presentation!")
        
    else:
        st.warning("""
        ⚠️ **No data available for comprehensive report**
        
        Add medical information using the Medical Info Manager to see visualizations here.
        
        Required data:
        - Vaccinations
        - Patient demographics  
        - Medications
        - Allergies
        """)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Analytics Dashboard")
    st.info("""
    Real-time visualization of healthcare data.
    
    **Features:**
    - 8 summary metrics
    - Vaccination coverage
    - Patient demographics
    - Medication trends
    - Allergy analysis
    - Comprehensive reporting
    """)
    
    st.markdown("### 🔄 Data Refresh")
    st.success("✅ Data updates in real-time")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Click tabs to explore different analytics
    - Hover over charts for details
    - Right-click charts to export
    - Use 'Refresh Data' button to update
    """)
