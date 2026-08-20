#  product_create.py

import httpx
import streamlit as st

API_BASE_URL = "https://zero2-mini-project-2-zjxj.onrender.com"

def product_create() -> None:
    """상품 조회."""

    st.subheader("Product 입력")
    st.caption("로그인 후 상품 조회를 합니다.")

    with st.form("product_form", clear_on_submit=True):
        product_id = st.number_input("ID")
        product_name = st.text_input("NAME", placeholder="품명 입력")
        product_price = st.number_input("PRICE")

        submitted = st.form_submit_button("전송")

    if submitted:

        if not product_id or not product_name or not product_price:
            st.warning("모두 입력 하세요")
        else:
            product_name = product_name.strip()
            payload = {"id": product_id, "name": product_name, "price":product_price}  # 백엔드 Pydantic 모델이 기대하는 JSON 구조로 데이터를 만듭니다.
            with st.spinner("전송후 기다립니다."):
                response = httpx.post(f"{API_BASE_URL}/product/create", json=payload, timeout=15.0)  # 메시지 API에 POST 요청을 보냅니다.
            if response.status_code == 200:
                result = response.json()
                st.info("입력 완료")
                st.info(f"{result["id"]} {result["name"]} {result["price"]}")
            else:
                st.warning("오류")
      

