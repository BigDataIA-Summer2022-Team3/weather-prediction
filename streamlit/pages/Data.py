import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as components
from pathlib import Path
import pickle


usernames = ["zhijie", "yijun", "team4", "parth", "srikanth"]

file_path = Path(__file__).parent.parent / "streamlitUserPW.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, "Login", "abcdef", cookie_expiry_days=0)

if st.session_state["authentication_status"]:
    token = st.session_state["token"] 
    username = st.session_state["name"]
    tab1, tab2, tab3 = st.tabs(["Generate_data", "Train Model", "Data Report"])

    with tab1:
        st.header("Generate Data")
        HtmlFile = open("./pages/DataClean.html", 'r')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 5000)

    with tab2:
        st.header("Train Model")
        HtmlFile2 = open("./pages/model.html", 'r')
        source_code2 = HtmlFile2.read() 
        components.html(source_code2, height = 14000)

    with tab3:
        st.header("Data report")
        

else:
    st.markdown('# Please login first')