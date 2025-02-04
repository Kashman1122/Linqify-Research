# import streamlit as st
# import hashlib
# import sqlite3
# from datetime import datetime
# import os
#
#
# # Initialize connection to SQLite
# def init_db():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS users
#                  (username TEXT PRIMARY KEY, password TEXT, email TEXT, created_at TEXT)''')
#     conn.commit()
#     conn.close()
#
#
# # Hash password
# def make_hashed_password(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()
#
#
# # User registration
# def register_user(username, password, email):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     try:
#         hashed_pwd = make_hashed_password(password)
#         c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
#                   (username, hashed_pwd, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
#     finally:
#         conn.close()
#
#
# # User login verification
# def login_user(username, password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     hashed_pwd = make_hashed_password(password)
#     c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pwd))
#     result = c.fetchone()
#     conn.close()
#     return result is not None
#
#
# # Initialize session state
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
#
# # Initialize database
# init_db()
#
# # Page config
# st.set_page_config(page_title="Linqify - Login", layout="wide", page_icon="🔍")
#
# # Custom CSS
# st.markdown("""
#     <style>
#     .main {
#         padding: 2rem;
#     }
#     .stTitle {
#         font-size: 3rem !important;
#         color: #1E88E5;
#         text-align: center;
#     }
#     .auth-box {
#         max-width: 500px;
#         margin: auto;
#         padding: 2rem;
#         background-color: #f8f9fa;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .centered {
#         text-align: center;
#     }
#     .stButton button {
#         width: 100%;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
# if not st.session_state.logged_in:
#     col1, col2, col3 = st.columns([1, 2, 1])
#
#     with col2:
#         st.title("🔍 Linqify")
#         st.markdown("<p class='centered'>Your Intelligent Research Assistant</p>", unsafe_allow_html=True)
#
#         # Login/Register tabs
#         tab1, tab2 = st.tabs(["Login", "Register"])
#
#         with tab1:
#             with st.form("login_form"):
#                 st.subheader("Login")
#                 username = st.text_input("Username")
#                 password = st.text_input("Password", type="password")
#                 login_button = st.form_submit_button("Login")
#
#                 if login_button:
#                     if username and password:
#                         if login_user(username, password):
#                             st.session_state.logged_in = True
#                             st.success("Login successful!")
#                             st.rerun()  # Use the updated version of the rerun function
#                         else:
#                             st.error("Invalid username or password")
#                     else:
#                         st.warning("Please fill in all fields")
#
#         with tab2:
#             with st.form("register_form"):
#                 st.subheader("Register")
#                 new_username = st.text_input("Choose Username")
#                 new_email = st.text_input("Email")
#                 new_password = st.text_input("Choose Password", type="password")
#                 confirm_password = st.text_input("Confirm Password", type="password")
#                 register_button = st.form_submit_button("Register")
#
#                 if register_button:
#                     if new_username and new_email and new_password and confirm_password:
#                         if new_password == confirm_password:
#                             if register_user(new_username, new_password, new_email):
#                                 st.success("Registration successful! Please login.")
#                             else:
#                                 st.error("Username already exists")
#                         else:
#                             st.error("Passwords do not match")
#                     else:
#                         st.warning("Please fill in all fields")
#
# else:
#     # Import and run the main application
#     import main_app


import streamlit as st
import hashlib
import sqlite3
from datetime import datetime


# Initialize connection to SQLite
def init_db():
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, email TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()

# Hash password
def make_hashed_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# User registration
def register_user(username, password, email):
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    try:
        hashed_pwd = make_hashed_password(password)
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                  (username, hashed_pwd, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# User login verification
def login_user(username, password):
    conn = sqlite3.connect('../users.db')
    c = conn.cursor()
    hashed_pwd = make_hashed_password(password)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pwd))
    result = c.fetchone()
    conn.close()
    return result is not None

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Initialize database
init_db()

# Page config
st.set_page_config(page_title="Linqify - Login", layout="wide", page_icon="🔍")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        font-size: 3rem !important;
        color: #1E88E5;
        text-align: center;
    }
    .auth-box {
        max-width: 500px;
        margin: auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .centered {
        text-align: center;
    }
    .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🔍 Linqify")
        st.markdown("<p class='centered'>Your Intelligent Research Assistant</p>", unsafe_allow_html=True)

        # Login/Register tabs
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login")

                if login_button:
                    if username and password:
                        if login_user(username, password):
                            st.session_state.logged_in = True
                            st.session_state.username = username  # Save the username in session state
                            st.success("Login successful!")
                            st.rerun()  # Refresh the page to show logged-in content
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.warning("Please fill in all fields")

        with tab2:
            with st.form("register_form"):
                st.subheader("Register")
                new_username = st.text_input("Choose Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                register_button = st.form_submit_button("Register")

                if register_button:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password == confirm_password:
                            if register_user(new_username, new_password, new_email):
                                st.success("Registration successful! Please login.")
                            else:
                                st.error("Username already exists")
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.warning("Please fill in all fields")

else:
    # User is logged in, display the main app or logged-in content
    st.title(f"Hey! , {st.session_state.username}!")
    st.write("You are now logged in and can access the full features of Linqify.")

    # Import and run the main application
    import main_app

    main_app.run()
