import streamlit as st

from app_pages.product_create import product_create
from app_pages.product_select import product_select


st.title("상품 관리")

create_tab, select_tab = st.tabs(
    ["상품 입력", "상품 조회"]
)

with create_tab:
    product_create()

with select_tab:
    product_select()