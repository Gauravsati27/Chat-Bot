bimport streamlit as st
import google.generativeai as genai
from datetime import datetime
import os
import geocoder
import json
import glob
import hashlib
import re

import db  # Import to initialize MongoDB connection

# --- Constants ---
SEARCHES_DIR = "searches"
ADMIN_CONFIG_FILE = "admin_config.json"
USERS_FILE = "users.json" # From auth.py

# --- Ensure Directories Exist ---
if not os.path.exists(SEARCHES_DIR):
    os.makedirs(SEARCHES_DIR)

# --- API Key Configuration (Consider using environment variables for security) ---
try:
    from config import GOOGLE_API_KEY
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY": # Basic check
         st.error("⚠️ Google API Key not configured in config.py. Please set it.")
         st.stop()
except ImportError:
    st.error("⚠️ config.py not found. Please create it and add your GOOGLE_API_KEY.")
    st.stop()
except AttributeError:
    st.error("⚠️ GOOGLE_API_KEY not found in config.py. Please add it.")
    st.stop()

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Loads user data from the JSON file."""
    if not os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump({}, f)
            return {}
        except IOError as e:
            st.error(f"Error creating user file ({USERS_FILE}): {e}")
            return None
    try:
        with open(USERS_FILE, 'r') as f:
            content = f.read()
            if not content:
                return {}
            data = json.loads(content)
            if data and isinstance(data, dict):
                first_value = next(iter(data.values()))
                if isinstance(first_value, str):
                    migrated = {user: {"password": pwd_hash, "email": ""} for user, pwd_hash in data.items()}
                    save_users(migrated)
                    return migrated
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        st.error(f"Error reading user file ({USERS_FILE}): {e}. Please check the file format.")
        return None
    except IOError as e:
        st.error(f"Error accessing user file ({USERS_FILE}): {e}")
        return None

def save_users(users_data):
    """Saves user data to the JSON file."""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
        return True
    except IOError as e:
        st.error(f"Error saving user data: {e}")
        return False

def verify_user(username, password):
    """Verifies username and password against stored data."""
    users = load_users()
    if users is None:
        st.error("Could not load user data for verification.")
        return False
    if username in users:
        stored_hashed_password = users[username].get("password") if isinstance(users[username], dict) else users[username]
        entered_hashed_password = hash_password(password)
        return stored_hashed_password == entered_hashed_password
    return False

def is_valid_email(email):
    """Basic email format validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def register_user(username, password, email):
    """Registers a new user with email."""
    users = load_users()
    if users is None:
        return False, "Could not load user data for registration."
    if not username or not password or not email:
        return False, "Username, password, and email cannot be empty."
    if not is_valid_email(email):
        return False, "Invalid email format."
    if username in users:
        return False, "Username already exists."

    hashed_password = hash_password(password)
    users[username] = {"password": hashed_password, "email": email}
    if save_users(users):
        return True, "Registration successful!"
    else:
        return False, "Failed to save user data."

# Other helper functions and app logic remain unchanged...

# --- Main Application Flow ---

if not st.session_state.get('logged_in', False):
    st.title("Welcome to the AI Assistant!")
    st.markdown("Please log in or register to continue.")

    choice = st.radio("Choose Action:", ("Login", "Register"), horizontal=True, key="auth_choice")

    if choice == "Login":
        st.subheader("Login")
        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                if verify_user(login_username, login_password):
                    if update_user_count(increment=True):
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.user_counted = True
                        st.session_state.messages = []
                        st.session_state.location = get_current_location()
                        st.rerun()
                    else:
                        st.error("Maximum user limit reached or failed to update count. Please try again later.")
                else:
                    st.error("Invalid username or password.")

    elif choice == "Register":
        st.subheader("Register New User")
        with st.form("register_form"):
            reg_email = st.text_input("Enter your Email", key="reg_email")
            reg_password = st.text_input("Choose a Password", type="password", key="reg_pass")
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")
            register_submitted = st.form_submit_button("Register")

            if register_submitted:
                if not reg_email or not reg_password:
                    st.warning("Please enter email and password.")
                elif reg_password != reg_password_confirm:
                    st.warning("Passwords do not match.")
                elif not is_valid_email(reg_email):
                    st.warning("Please enter a valid email address.")
                else:
                    # Extract username from email (part before '@')
                    extracted_username = reg_email.split('@')[0]
                    success, message = register_user(extracted_username, reg_password, reg_email)
                    if success:
                        st.success(message + f" Your username is '{extracted_username}'. You can now log in.")
                    else:
                        st.error(message)

# The rest of the app logic remains unchanged...
