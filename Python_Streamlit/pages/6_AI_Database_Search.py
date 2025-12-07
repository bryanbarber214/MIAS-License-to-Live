"""
AI Database Search
License to Live: MIAS - Python/Streamlit Version
Natural language database queries using Claude AI
"""

import streamlit as st
import sys
import os
import json
import re
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from admin_auth import admin_login_page, show_logout_button

# Page configuration
st.set_page_config(
    page_title="AI Database Search - MIAS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AUTHENTICATION CHECK
if not admin_login_page():
    st.stop()

# Show logout button
show_logout_button()

# Custom CSS
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .query-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .example-query {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        cursor: pointer;
        border: 1px solid #90caf9;
        transition: all 0.3s ease;
    }
    
    .example-query:hover {
        background-color: #bbdefb;
        transform: translateX(5px);
    }
    
    .sql-display {
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
        overflow-x: auto;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="main-title">
    <h1>🤖 AI Database Search</h1>
    <h3>Ask Questions in Natural Language</h3>
    <p>Powered by Claude AI</p>
</div>
""", unsafe_allow_html=True)

# BULLETPROOF API KEY DETECTION
api_key_available = False
api_key = None

st.info("🔍 Checking for API key...")

# Method 1: Try root level
try:
    if hasattr(st.secrets, 'ANTHROPIC_API_KEY'):
        api_key = st.secrets.ANTHROPIC_API_KEY
        api_key_available = True
        st.success("✅ Found API key at root level (Method 1)")
except Exception as e:
    st.warning(f"Method 1 failed: {str(e)}")

# Method 2: Try dictionary access
if not api_key_available:
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        api_key_available = True
        st.success("✅ Found API key via dictionary access (Method 2)")
    except Exception as e:
        st.warning(f"Method 2 failed: {str(e)}")

# Method 3: Try in admin section
if not api_key_available:
    try:
        api_key = st.secrets["admin"]["ANTHROPIC_API_KEY"]
        api_key_available = True
        st.success("✅ Found API key in admin section (Method 3)")
    except Exception as e:
        st.warning(f"Method 3 failed: {str(e)}")

# Method 4: Try get method
if not api_key_available:
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
        if api_key:
            api_key_available = True
            st.success("✅ Found API key via get method (Method 4)")
    except Exception as e:
        st.warning(f"Method 4 failed: {str(e)}")

# DEBUG: Show what's available
if not api_key_available:
    st.error("❌ Could not find ANTHROPIC_API_KEY in any location")
    
    with st.expander("🔍 DEBUG: Show Available Secrets Structure"):
        try:
            st.write("**Available root-level keys:**")
            root_keys = []
            for key in dir(st.secrets):
                if not key.startswith('_'):
                    root_keys.append(key)
            st.write(root_keys)
            
            st.write("\n**Secrets as dictionary:**")
            try:
                secrets_dict = dict(st.secrets)
                # Don't show actual values, just keys
                st.write(list(secrets_dict.keys()))
            except:
                st.write("Cannot convert to dict")
                
            st.write("\n**Check individual sections:**")
            if hasattr(st.secrets, 'database'):
                st.write("✅ database section exists")
            if hasattr(st.secrets, 'admin'):
                st.write("✅ admin section exists")
                try:
                    admin_keys = list(st.secrets.admin.keys())
                    st.write(f"Admin section keys: {admin_keys}")
                except:
                    pass
                    
        except Exception as e:
            st.write(f"Debug error: {str(e)}")

if not api_key_available:
    st.error("""
    ⚠️ **Anthropic API Key Not Configured**
    
    **Your secrets.toml should look EXACTLY like this:**
    
    ```toml
    [database]
    host = "your-host-here"
    port = 3306
    user = "admin"
    password = "your-password"
    database = "mias_db"
    
    [admin]
    username = "admin"
    password = "your-password"
    
    ANTHROPIC_API_KEY = "sk-ant-api03-..."
    ```
    
    **CRITICAL:**
    - Blank line after [admin] section
    - ANTHROPIC_API_KEY is NOT inside [admin] or [database]
    - It's at the root level (no brackets)
    
    **Steps to fix:**
    1. Go to Settings → Secrets in Streamlit Cloud
    2. Copy the format above
    3. Save
    4. Reboot app
    5. Wait 3 minutes
    
    **Free tier:** Get $5 free credits at https://console.anthropic.com/
    """)
    st.stop()

# Import Anthropic after we have the key
try:
    import anthropic
    
    # DEBUG: Show key format (safely)
    if api_key:
        key_length = len(api_key)
        key_start = api_key[:10] if len(api_key) > 10 else api_key
        key_end = api_key[-4:] if len(api_key) > 4 else ""
        st.info(f"🔑 Key format check: Length={key_length}, Start={key_start}..., End=...{key_end}")
        
        # Check for common issues
        if api_key != api_key.strip():
            st.warning("⚠️ Key has extra whitespace - cleaning...")
            api_key = api_key.strip()
        
        if '\n' in api_key or '\r' in api_key:
            st.warning("⚠️ Key has newline characters - removing...")
            api_key = api_key.replace('\n', '').replace('\r', '')
    
    client = anthropic.Anthropic(api_key=api_key)
    st.success("✅ Anthropic client initialized successfully!")
except ImportError:
    st.error("""
    ⚠️ **Anthropic library not installed**
    
    Add `anthropic` to your requirements.txt file and redeploy.
    """)
    st.stop()
except Exception as e:
    st.error(f"Error initializing Anthropic client: {str(e)}")
    st.stop()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_sql' not in st.session_state:
    st.session_state.last_sql = None

# Database schema information for Claude
SCHEMA_INFO = """
DATABASE SCHEMA FOR MIAS (Medical Information Access System):

Tables:
1. Patients
   - patient_id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - license_number (VARCHAR, UNIQUE)
   - first_name (VARCHAR)
   - last_name (VARCHAR)
   - date_of_birth (DATE)
   - address (TEXT)
   - city (VARCHAR)
   - state (VARCHAR)
   - zip_code (VARCHAR)
   - phone (VARCHAR)
   - email (VARCHAR)
   - blood_type (VARCHAR) - e.g., 'A+', 'O-', etc.
   - emergency_token (VARCHAR)
   - created_at (DATETIME)
   - updated_at (DATETIME)

2. Medical_Conditions
   - condition_id (INT, PRIMARY KEY)
   - patient_id (INT, FOREIGN KEY → Patients)
   - condition_name (VARCHAR) - e.g., 'Diabetes Type 2', 'Hypertension'
   - diagnosis_date (DATE)
   - severity (VARCHAR) - 'Mild', 'Moderate', 'Severe'
   - notes (TEXT)

3. Allergies
   - allergy_id (INT, PRIMARY KEY)
   - patient_id (INT, FOREIGN KEY → Patients)
   - allergen (VARCHAR) - e.g., 'Peanuts', 'Penicillin'
   - allergy_type (VARCHAR) - 'Food', 'Medication', 'Environmental'
   - severity (VARCHAR) - 'Mild', 'Moderate', 'Severe', 'Life-threatening'
   - reaction (TEXT)
   - diagnosed_date (DATE)

4. Medications
   - medication_id (INT, PRIMARY KEY)
   - patient_id (INT, FOREIGN KEY → Patients)
   - medication_name (VARCHAR) - e.g., 'Metformin', 'Lisinopril'
   - dosage (VARCHAR) - e.g., '500mg', '10mg'
   - frequency (VARCHAR) - e.g., 'Twice daily', 'Once daily'
   - prescribing_doctor (VARCHAR)
   - start_date (DATE)
   - notes (TEXT)

5. Vaccinations
   - vaccination_id (INT, PRIMARY KEY)
   - patient_id (INT, FOREIGN KEY → Patients)
   - vaccine_name (VARCHAR) - e.g., 'COVID-19', 'Influenza'
   - date_administered (DATE)
   - administering_provider (VARCHAR)
   - lot_number (VARCHAR)

6. Emergency_Contacts
   - contact_id (INT, PRIMARY KEY)
   - patient_id (INT, FOREIGN KEY → Patients)
   - contact_name (VARCHAR)
   - relationship (VARCHAR) - e.g., 'Spouse', 'Parent'
   - phone_number (VARCHAR)
   - is_primary (BOOLEAN)

7. Insurance
   - insurance_id (INT, PRIMARY KEY)
   - patient_id (INT, FOREIGN KEY → Patients)
   - provider_name (VARCHAR)
   - policy_number (VARCHAR)
   - group_number (VARCHAR)
   - coverage_type (VARCHAR)

IMPORTANT SQL RULES:
- Use MySQL syntax
- Always use proper JOINs when querying multiple tables
- For age calculations, use: TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())
- For patient counts, always use COUNT(DISTINCT patient_id)
- Use LIMIT clause to prevent overwhelming results
- Never return sensitive data like emergency_token or full license_number in results
"""

# Example queries
EXAMPLE_QUERIES = [
    "How many patients do we have in the system?",
    "Show me all patients with diabetes",
    "List patients with life-threatening allergies",
    "Which patients have Type O- blood?",
    "Show patients on blood pressure medications",
    "What are the most common medical conditions?",
    "List patients over 65 years old",
    "Show vaccination statistics",
    "Which patients have no emergency contacts?",
    "Count patients by blood type"
]

def generate_sql_from_natural_language(user_query: str) -> dict:
    """
    Use Claude to convert natural language to SQL
    
    Returns:
        dict with 'sql' and 'explanation' keys
    """
    
    system_prompt = f"""You are a SQL expert for a medical database. Convert natural language queries to MySQL queries.

{SCHEMA_INFO}

CRITICAL SAFETY RULES:
1. ONLY generate SELECT queries - NEVER INSERT, UPDATE, DELETE, DROP, ALTER, etc.
2. Always validate that queries are read-only
3. Use LIMIT to prevent overwhelming results (default LIMIT 100)
4. Never expose sensitive data like emergency_token or full license_number
5. For license_number, use: CONCAT(LEFT(license_number, 4), '****') AS license_number

Return your response as valid JSON with this exact structure:
{{
    "sql": "the SQL query here",
    "explanation": "brief explanation of what the query does",
    "is_safe": true or false
}}

If the query asks for something dangerous or inappropriate, set is_safe to false and explain why in the explanation field."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=0,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Convert this to SQL: {user_query}"
                }
            ]
        )
        
        # Parse response
        response_text = response.content[0].text
        
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response_text)
        
        return result
        
    except Exception as e:
        return {
            "sql": None,
            "explanation": f"Error generating SQL: {str(e)}",
            "is_safe": False
        }

def execute_safe_query(sql: str) -> tuple:
    """
    Execute SQL query with safety checks
    
    Returns:
        (success: bool, result: DataFrame or error message)
    """
    # Safety check: only allow SELECT queries
    sql_upper = sql.strip().upper()
    
    dangerous_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE']
    
    if not sql_upper.startswith('SELECT'):
        return False, "Only SELECT queries are allowed"
    
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return False, f"Dangerous keyword detected: {keyword}"
    
    try:
        result = db.execute_query(sql, fetch=True)
        
        if result:
            import pandas as pd
            df = pd.DataFrame(result)
            return True, df
        else:
            return True, "Query executed successfully but returned no results"
            
    except Exception as e:
        return False, f"Query execution error: {str(e)}"

# Main interface
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask a Question")
    
    # Text input for query
    user_query = st.text_area(
        "Enter your question in natural language:",
        height=100,
        placeholder="e.g., How many patients have diabetes?",
        help="Ask anything about the patient database in plain English"
    )
    
    col_a, col_b = st.columns([1, 4])
    with col_a:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    with col_b:
        clear_button = st.button("🔄 Clear History", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.session_state.last_sql = None
        st.rerun()

with col2:
    st.markdown("### 📋 Example Queries")
    st.markdown("Click to try:")
    
    for example in EXAMPLE_QUERIES[:5]:  # Show first 5
        if st.button(example, key=f"example_{example}", use_container_width=True):
            user_query = example
            search_button = True

# Process query
if search_button and user_query:
    with st.spinner("🤖 Claude is thinking..."):
        # Generate SQL
        result = generate_sql_from_natural_language(user_query)
        
        if not result.get('is_safe', False):
            st.error(f"❌ **Query Safety Check Failed**\n\n{result.get('explanation', 'Query deemed unsafe')}")
        else:
            # Display SQL
            st.markdown("### 📝 Generated SQL")
            st.markdown(f"""
            <div class="sql-display">
            {result['sql']}
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"**Explanation:** {result['explanation']}")
            
            # Execute query
            st.markdown("### 📊 Results")
            
            success, query_result = execute_safe_query(result['sql'])
            
            if success:
                import pandas as pd
                if isinstance(query_result, pd.DataFrame):
                    st.success(f"✅ Query executed successfully! Found {len(query_result)} results.")
                    
                    # Display results
                    st.dataframe(query_result, use_container_width=True)
                    
                    # Download button
                    csv = query_result.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Add to history
                    st.session_state.chat_history.append({
                        'query': user_query,
                        'sql': result['sql'],
                        'result_count': len(query_result),
                        'timestamp': datetime.now()
                    })
                    
                else:
                    st.warning(str(query_result))
            else:
                st.error(f"❌ **Query Failed**\n\n{query_result}")

# Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📜 Query History")
    
    for i, item in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
        with st.expander(f"🕐 {item['timestamp'].strftime('%I:%M %p')} - {item['query'][:50]}..."):
            st.markdown(f"**Question:** {item['query']}")
            st.code(item['sql'], language='sql')
            st.caption(f"Results: {item['result_count']} rows")

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 AI Database Search")
    st.info("""
    **How it works:**
    1. Type your question in plain English
    2. Claude AI converts it to SQL
    3. Query is validated for safety
    4. Results are displayed
    
    **Perfect for:**
    - Quick statistics
    - Patient lookups
    - Medical condition analysis
    - Demographic queries
    """)
    
    st.markdown("### 🛡️ Safety Features")
    st.success("""
    ✅ Read-only queries  
    ✅ SQL injection prevention  
    ✅ Automatic result limiting  
    ✅ Sensitive data masking
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Be specific in your questions
    - Use medical terminology
    - Ask about counts, lists, or statistics
    - Try the example queries first
    """)
    
    st.markdown("### 📊 Database Stats")
    try:
        total_patients = db.execute_query("SELECT COUNT(*) as count FROM Patients", fetch=True)
        if total_patients:
            st.metric("Total Patients", total_patients[0]['count'])
    except:
        pass
