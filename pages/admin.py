import streamlit as st
import sqlite3

# Initialize connection to SQLite
def init_db():
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, email TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()

# Fetch all users from the database
def fetch_all_users():
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    c.execute("SELECT username, email, created_at FROM users")
    users = c.fetchall()
    conn.close()
    return users

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Admin login
def admin_login(username, password):
    # Replace with a check for admin credentials (hardcoded or fetched from a config/db)
    return username == "Kashish" and password == "Harekrishna123@#$"  # Example for simplicity

# Page config
st.set_page_config(page_title="Admin - Linqify", layout="wide", page_icon="🔐")

# Custom CSS
st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Admin login form
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🔐 Admin Login")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if admin_username and admin_password:
                if admin_login(admin_username, admin_password):
                    st.session_state.logged_in = True
                    st.session_state.username = admin_username  # Store admin username in session state
                    st.success("Login successful!")
                    st.rerun()  # Refresh the page to show admin content
                else:
                    st.error("Invalid admin credentials")
            else:
                st.warning("Please fill in both fields")

else:
    # Admin is logged in, display the registered users
    st.title(f"Welcome, {st.session_state.username}!")
    st.write("Here is the list of all registered users:")

    # Fetch users and display them in a table
    users = fetch_all_users()
    if users:
        user_data = []
        for user in users:
            user_data.append([user[0], user[1], user[2]])

        st.table(user_data)
    else:
        st.write("No registered users found.")
