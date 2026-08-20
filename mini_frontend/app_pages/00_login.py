import streamlit as st




st.title("LOGIN")

with st.form("login_form"):
    st.text_input("ID 입력")
    st.text_input("PWD 입력")
    st.form_submit_button("LOGIN")

