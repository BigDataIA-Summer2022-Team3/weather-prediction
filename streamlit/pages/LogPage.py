import streamlit as st
import pymysql
Host, User, Password = st.secrets["Host"] , st.secrets["User"] , st.secrets["Password"]
con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
c = con.cursor()
c.execute('select * from log_table')
datainfo = c.fetchall()

st.write(datainfo)