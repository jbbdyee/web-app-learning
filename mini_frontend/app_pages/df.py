import streamlit as st
import pandas as pd

st.title("Table")

data = {  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    "course": ["Python", "Streamlit", "FastAPI"],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    "hours": [24, 16, 32],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    "level": ["Basic", "Basic", "Intermediate"],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
}

df = pd.DataFrame(data)  # 딕셔너리 데이터를 행과 열을 가진 DataFrame 표 구조로 변환합니다.

st.subheader("dataframe")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
st.dataframe(df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.

st.subheader("table")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
st.table(df)  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.