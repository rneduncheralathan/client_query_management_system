import streamlit as st
import pandas as pd
import hashlib
import re
import db_connection as cqms_con
import time


st.set_page_config(page_title="Client Query Management System")

# main style
st.markdown("""
        <style>
            .st-emotion-cache-tn0cau{
                margin-top:-50px
            }
            .st-emotion-cache-1w723zb {
                max-width:1200px
            }
            .st-emotion-cache-gi0tri{
            display:none
            }

            .st-emotion-cache-ua1rfn h3{
                    font-size: large;
                    margin-top: -25px;
                }
            .st-emotion-cache-ua1rfn h1{
                 
                    font-size: 16px;
                    padding-top: 0px;
            
            }
            .st-emotion-cache-1ksltpv{
                display: none;
            }
            textarea {
                min-height: 40px !important;
                max-height: 0px !important;
            }
            </style>
        """,unsafe_allow_html=True)

# Page Header
st.header("Client Query Management System")
 
# st.subheader("Organizing,Tracking,and Closing Support Queries")

#By default LonIn Page is TRUE and This is The Intial Declaration Of Navigation BOOLEAN
  
if 'show_login_block' not in st.session_state:
    st.session_state.show_login_block = True
if 'show_client_block' not in st.session_state:
    st.session_state.show_client_block = False
if 'show_support_block' not in st.session_state:
    st.session_state.show_support_block = False
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

# Block Of LogIn Page CODE

#Hash Password
def hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User LogIn Logic 
def logIn(log_in):
    hashed_pwd = hashed_password(log_in["pass_word"]) 
    user_data = cqms_con.fetch_users(True)
    login_success = False
    for row in user_data:
        if (log_in["user_name"] == row["user_name"]) and (hashed_pwd == row["pass_word"]):
            if((log_in["user_role"] == row["user_role"])):
                login_success = True
                if row["user_role"] == "client":
                    st.session_state.logged_user = row["user_name"]
                    st.session_state.show_login_block = False
                    st.session_state.show_support_block = False
                    st.session_state.show_client_block = True
                    st.toast(f"Login Successfuly,***{row['user_role']}***",icon="✅")
                    time.sleep(1)
                    st.rerun()
                if((log_in["user_role"] == "support")):
                    st.session_state.logged_user = row["user_name"]
                    st.session_state.show_login_block = False
                    st.session_state.show_client_block = False
                    st.session_state.show_support_block = True
                    st.toast(f"Login Successfuly,***{row['user_role']}***",icon="✅")
                    time.sleep(1)
                    st.rerun()
            break
    if not login_success:
        st.toast(" Invalid User Name , Password and Role", icon="❌")

#User Regiser Logic
def register(log_in):
    hashed_pwd = hashed_password(log_in["pass_word"]) 
    user_data = {"user_name":log_in["user_name"],"pass_word":hashed_pwd,"user_role":log_in["user_role"]}
    register_success = False
    print(user_data)
    register_user = cqms_con.fetch_users(True)
    for row in register_user:
        if log_in["user_name"] == row["user_name"] and hashed_pwd == row["pass_word"] and log_in["user_role"] == row["user_role"]:
            register_success = True
            st.toast("User Already Exist",icon="❌")
            break
    if not register_success:
            cqms_con.user_register(user_data)
            st.toast("User Register successfully",icon="✅")

# Register Form clear
def register_clear():
    st.session_state["reg_username"] = ""
    st.session_state["reg_password"] = ""
    st.session_state["reg_role"] = None
        

if st.session_state.show_login_block:

# LogIn Page Style
    st.markdown("""
        <style>
                .stForm{
                    margin: 4% 10% 10% 20%;
                    width:40%;
                }
              
                .stButton{   
                    margin-top:10px;
                    width:unset;
                } 
                .st-c7{
                    display:inline;
                }
                .st-ar{
                    margin-left:245px;
                }
            </style>
        """,unsafe_allow_html=True)
    
    #Login & Register Tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        # Log-In Form
        with st.form("login_form"):
            username = st.text_input("User Name")
            password = st.text_input("Password", type="password")
            user_role = st.selectbox("Role", ["client", "support"], index=None, placeholder="Choose Role")
            submit = st.form_submit_button("Login")

            if submit:
                log_in = {"user_name": username,"pass_word": password,"user_role": user_role}
                logIn(log_in)

    with tab2:
        # Register Form
        with st.form("register_form"):
            username = st.text_input("User Name",key="reg_username")
            password = st.text_input("Password", type="password",key="reg_password")
            user_role = st.selectbox("Role", ["client", "support"], index=None, placeholder="Choose Role",key="reg_role")
            # submit = st.form_submit_button("Register")

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Register")
            with col2:
                st.form_submit_button("Clear",on_click=register_clear)
            
            # Register button action
            if submit:
                log_in = {"user_name": username,"pass_word": password,"user_role": user_role}
                register(log_in)
        


# Client Query Submission Page
if st.session_state.show_client_block:
    # Client Page Style
    st.markdown("""
        <style>
                .stForm{
                    margin: 0% 10% 10% 20%;
                    width:42%;
                }
                .stTextInput {
                    width: 450px;
                }
                .stTextArea {
                    width: 450px;
                }
                .stButton {
                    margin-top:10px;
                    width:unset;
                }
                </style>
        """, unsafe_allow_html=True)

    # Client Header
    st.title("Query Submission Interface")

    # Client Log-Out function   
    def client_log_out():
        st.session_state.show_login_block = True
        st.session_state.show_client_block = False
        st.session_state.show_support_block = False
        st.session_state.logged_user = None
        
    #Form Clear
    def clear_form():
        st.session_state["email"] = ""
        st.session_state["mobile"] = ""
        st.session_state["query_head"] = ""
        st.session_state["moble_descrip"] = ""

    # Query Insert Form
    with st.form("client_query_form"):
        emailid = st.text_input("Email ID", key="email")
        mobilenumber = st.text_input("Mobile No", key="mobile")
        queryheading = st.text_area("Query Heading", key="query_head")
        querydescription = st.text_area("Query Description", key="moble_descrip")

        col1, col2,col3 = st.columns(3)
        with col1:
            submitted = st.form_submit_button("Submit")
        with col2:
            st.form_submit_button("Clear",on_click=clear_form)
        with col3:
            st.form_submit_button("Logout",on_click=client_log_out)

        # Submit button inside the form
        # submitted = st.form_submit_button("Submit")

    # Query Submission Logic
    if submitted:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, emailid):
            st.toast("Please nter a valid email before submitting", icon="⚠️")
        elif not mobilenumber.isdigit() or len(mobilenumber) != 10:
            st.toast("Please enter a valid 10-digit mobile number", icon="⚠️")
        else:
            client_query = {
                "mail_id": emailid,
                "mobile_number": mobilenumber,
                "query_heading": queryheading,
                "query_description": querydescription,
                "query_status": "open",
                "query_closed_time": None
            }
            print(client_query)
            cqms_con.query_insertion(client_query)
            st.toast("Query Created successfully", icon="✅")


    # Log-Out button (outside form)
    # st.button("Clear", on_click=clear_form)
    # st.button("Log-Out", on_click=client_log_out)



# Query Managemant Dashboard Page
if st.session_state.show_support_block:
    
    # Query Managemant Dashboard Page Style
    st.markdown("""
        <style>
                .stSelectbox{
                    display:inline-flex;

                }
                .st-emotion-cache-3qzj0x{
                    width: 7rem;
                }
                </style>
        """,unsafe_allow_html=True)

    # Query Management Dashboard Header
    st.title("Query Management Dashboard")

    # Query Management Dashboard Logout
    def query_management_dashboard_log_out():
        st.session_state.show_login_block = True
        st.session_state.show_client_block = False
        st.session_state.show_support_block = False
        st.session_state.logged_user = None

    # Close Query PopUp
    @st.dialog("Close Query")
    def colse_query_dialog():
        query_id = st.text_input("Query ID")
        if query_id:
            if not query_id.isdigit():
                st.error("Please enter only numbers.")
            
        #Close Query PopUp Submit Function   
        def submit_query(query_id):
            print(query_id,"qqqqqqqqqqqqqq")
            cqms_con.update_query(query_id)
        if st.button("Submit",on_click=submit_query,args=(query_id,)):
            st.rerun() 

    col1, col2,col3 = st.columns(3)
    
    with col1:
        # Query Status filter
        status_options = ["all","open","close"]
        selected_status  = st.selectbox("Query Status",status_options, index=0, placeholder="Choose Status")
    with col2:
        st.button("Close Query",on_click=colse_query_dialog)
    with col3:
        st.button("Log-Out",on_click=query_management_dashboard_log_out)

   
    #Fetch Query data
    query_data = cqms_con.fetch_query(True)
    df = pd.DataFrame(query_data)

    # Select Qurey Status
    if selected_status == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['query_status'] == selected_status]

    # Query Information Show In The Table
    st.dataframe(filtered_df, hide_index=True)

    # st.button("Close Query",on_click=colse_query_dialog)
    # st.button("Log-Out",on_click=query_management_dashboard_log_out)
