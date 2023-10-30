import streamlit as st
import streamlit_authenticator as stauth 
import pandas as pd

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# --- USER AUTHENTICATION ---
st.sidebar.markdown('''
---
Made by [Bensaid Mohamed](mohamed2018bensaid@gmail.com/).
''')
names = ['Adminstrator']
usernames = ['admin']
passwords = ['admin']

# load hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwords[0]
                }            
            }
        }

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
        authenticator.logout("Logout", "sidebar")
        def get_data_from_excel():
                df=pd.read_csv('usage_records.csv')
                return df
        df=get_data_from_excel()
        df_selection=df.copy()
        avg_sal = int((df['correct'] == 1).sum())
        avg_age = int((df['correct'] - df['predection']).abs().sum())
        persdata = int((df_selection.shape[0]/df.shape[0])*100)

        st.markdown('### Metrics')
        col1, col2, col3 = st.columns(3)
        col1.metric("Correct predections:", f"{avg_sal}","")
        col2.metric("Sum of erorrs:", f"{avg_age}","")
        col3.metric("Data Selected:", f"{persdata}%",f"{df_selection.shape[0]}")
        st.markdown('### Data Table')
        st.dataframe(df_selection)