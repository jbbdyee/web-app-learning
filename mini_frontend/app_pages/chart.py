import streamlit as st
import pandas as pd

st.title("Chart")

df = pd.DataFrame(  # 딕셔너리 데이터를 행과 열을 가진 DataFrame 표 구조로 변환합니다.
    {
        "week": [1, 2, 3, 4],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        "study_time": [3, 5, 4, 7],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    }
).set_index("study_time")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

st.line_chart(df)  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

st.subheader("막대 그래프 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

df = pd.DataFrame(  # 딕셔너리 데이터를 행과 열을 가진 DataFrame 표 구조로 변환합니다.
    {
        "course": ["Python", "Streamlit", "FastAPI", "Supabase"],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        "students": [24, 18, 20, 12],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    }
).set_index("course")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

st.bar_chart(df)  # 숫자 데이터를 막대 차트로 시각화합니다.
