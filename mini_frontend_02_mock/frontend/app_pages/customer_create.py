#  customer_create.py

import streamlit as st
from clients.customer_client import customer_insert
from core.api_client import BackendAPIError

"""로그인 후 mock 대화를 입력하고 누적 표시합니다."""

st.subheader("Customer")
st.caption("로그인 후 mock 대화를 입력하고 누적 표시합니다.")

with st.form("product_form", clear_on_submit=True):
    customer_id = st.number_input("ID")
    customer_name = st.text_input("NAME", placeholder="이름 입력")
    customer_age = st.number_input("AGE")
    customer_pwd = st.text_input("PASSWARD", type="password", placeholder="비밀번호 입력")

    submitted = st.form_submit_button("전송")

if submitted:

    if not customer_id or not customer_name or not customer_age or not customer_pwd:
        st.warning("모두 입력 하세요")
    else:
        customer_name = customer_name.strip()
        payload = {"id": customer_id, "pwd": customer_pwd, "name": customer_name, "age":customer_age}  # 백엔드 Pydantic 모델이 기대하는 JSON 구조로 데이터를 만듭니다.
        try:
            with st.spinner("전송후 기다립니다."):
                result = customer_insert(payload)

            if result is not None:
                st.info("입력 완료")
                st.info(f"{result["id"]} {result["name"]} {result["age"]}")
            else:
                st.warning("오류")
        except BackendAPIError as error:
            st.error(str(error))

    