import streamlit as st
import json
import os

# Constants
ADMIN_CONFIG_FILE = "admin_config.json"

# Initialize session state
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

def load_admin_config():
    """Load admin configuration"""
    try:
        with open(ADMIN_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default config if file doesn't exist
        default_config = {
            "admin_credentials": {
                "username": "admin",
                "password": "admin123"
            },
            "restricted_keywords": [
                "hack",
                "exploit",
                "illegal",
                "crack",
                "password"
            ],
            "max_users": 100,
            "active_users": 0
        }
        with open(ADMIN_CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def check_authentication(username, password):
    """Check admin credentials"""
    config = load_admin_config()
    if config and 'admin_credentials' in config:
        return (username == config['admin_credentials']['username'] and 
                password == config['admin_credentials']['password'])
    return False

# Create searches directory if it doesn't exist
if not os.path.exists('searches'):
    os.makedirs('searches')

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🎛️0//4",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #1C1C1C;
    }
    .main {
        color: white;
    }
    .stButton button {
        background-color: #2962ff;
        color: white;
    }
    .stTextInput input {
        color: white;
    }
    .css-1d391kg {
        background-color: #1C1C1C;
    }
</style>
""", unsafe_allow_html=True)

# Authentication
if not st.session_state.admin_authenticated:
    st.title("🔐 Admin Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if check_authentication(username, password):
                st.session_state.admin_authenticated = True
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid credentials!")
                
        st.info("Default credentials: username='admin', password='admin123'")
else:
    st.title("🎛️ Admin Dashboard")
    
    # Welcome message
    st.markdown("""
    Welcome to the Admin Dashboard! Use the sidebar to navigate between different sections:
    
    ### 📊 Search Monitoring
    - View all search queries
    - Filter by date and location
    - Export search data
    
    ### 🚫 Keyword Management
    - Add/remove restricted keywords
    - Import/export keyword lists
    - Manage content filtering
    
    ### 👥 User Statistics
    - Monitor user activity
    - Set user limits
    - View usage patterns
    """)
    
    # Quick Stats
    st.header("Quick Statistics")
    
    config = load_admin_config()
    if config:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Users", config['active_users'])
        
        with col2:
            st.metric("Maximum Users", config['max_users'])
        
        with col3:
            st.metric("Restricted Keywords", len(config['restricted_keywords']))
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.admin_authenticated = False
        st.rerun() 