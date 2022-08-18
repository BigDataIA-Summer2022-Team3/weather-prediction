import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import requests
import time

usernames = ["zhijie", "yijun", "team4", "parth", "srikanth"]

file_path = Path(__file__).parent.parent / "streamlitUserPW.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, "Login", "abcdef", cookie_expiry_days=0)


if st.session_state["authentication_status"]:
    token = st.session_state["token"] 
    # st.warning("token: " + token) # Debug
    username = st.session_state["name"]
    # st.warning("username: " + username)


    header = {"Authorization": "Bearer "+ token, "accept": "application/json"}

    authenticator.logout('Logout', 'sidebar')

    st.sidebar.markdown("## Function Page")

    def api1():
        st.header("Function 1: What's the weather of Seattle tomorrow?")
        # st.sidebar.subheader("Predict Weather")
        if st.button("predict"):
            st.write('function 1')
            # run function
            # url =            

            # res = requests.get(url=url, headers = header)
            # meta = res.json()
            # st.write(meta)
            

    def api2():
        st.header("Function 2: Temperature in the past 7 days")
        if st.button("Select"):
            st.write('function 2')
            # run function
            # url =            

            # res = requests.get(url=url, headers = header)
            # meta = res.json()
            # st.write(meta)


    def api3():
        st.header("Function 3: Precipitation in the past 7 days")
        if st.button("Select"):
            st.write('function 3')
            # run function
            # url =            

            # res = requests.get(url=url, headers = header)
            # meta = res.json()
            # st.write(meta)

    
    funNum = {
        "API 1: Predict Weather": api1,
        "API 2: Changes of maximum temperature": api2,
        "API 3: Changes of Precipitation": api3
    }

    selectFun = st.sidebar.selectbox("choose function", funNum.keys())
    funNum[selectFun]()
else:
    st.markdown('# Please login first')