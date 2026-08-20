#  customer_select.py

import streamlit as st
import pandas as pd
from core.api_client import BackendAPIError

from clients.customer_client import (
    customer_delete,
    customer_select,
    customer_select_all,
    customer_update
)



@st.dialog("삭제")
def show_del(p:dict) -> None:
    st.info("Delete")
    st.write(f"{p['name']}삭제 하시겠습니까")
    if st.button("삭제"):
        with st.spinner("삭제 진행"):
            result = customer_delete(p["id"])  
        if result is not None:
            st.rerun()

@st.dialog("수정")
def show_up(p:dict) -> None:
    st.info(f"{p['id']}를 수정 하겠습니다.")
    with st.form(f"form_{p['id']}"):
        customer_name = st.text_input("이름:", value=p["name"])
        customer_age = st.number_input("나이:", value=int(p["age"]))
        if st.form_submit_button("수정"):
            payload = {"name":customer_name, "age":customer_age}
            with st.spinner("데이터 요청"):
                result = customer_update(p["id"], payload)
            if result is not None:
                st.rerun()



"""데이터를 확인합니다."""

st.subheader("Customer 조회")
st.caption("customer 테이블을 선택하고 데이터를 확인합니다.")

try:
    with st.spinner("데이터 요청"):
        result = customer_select_all()

    if not result:
        st.info("Customer 가 없습니다.")
    for p in result:
        with st.container(border=True):
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                st.write(p["id"])
            with col2:    
                st.write(p["name"])
            with col3:
                st.write(f"{p['age']}원")
            with col4:
                if st.button("삭제", key=f"del_{p['id']}"):
                    show_del(p)
                if st.button("수정", key=f"up_{p['id']}"):
                    show_up(p)
except BackendAPIError as error:
    st.error(str(error))