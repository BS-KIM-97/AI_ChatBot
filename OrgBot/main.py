
# 모듈
from typing import List, Union
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_experimental.tools import PythonAstREPLTool
from langchain_openai import ChatOpenAI
from Modules import logging
from Modules.messages import AgentStreamParser, AgentCallbacks
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Modules import call
from Modules.call import ask
from Modules.call import print_messages
from Modules.agent import create_agent

# env
load_dotenv()
logging.langsmith("Blog Agent ChatBot")

# 실행
st.title("Blog Agent ChatBot 💬")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # 대화 내용을 저장할 리스트 초기화

# 사이드바 설정
with st.sidebar:
    clear_btn = st.button("대화 초기화")  # 대화 내용을 초기화하는 버튼
    uploaded_file = st.file_uploader(
        "CSV 파일을 업로드 해주세요.", type=["csv"], accept_multiple_files=True
    )  # CSV 파일 업로드 기능
    selected_model = st.selectbox(
        "OpenAI 모델을 선택해주세요.", ["gpt-4o", "gpt-4o-mini"], index=0
    )  # OpenAI 모델 선택 옵션
    apply_btn = st.button("데이터 분석 시작")  # 데이터 분석을 시작하는 버튼


# 메인 로직
if clear_btn:
    st.session_state["messa ges"] = []  # 대화 내용 초기화

if apply_btn and uploaded_file:
    loaded_data = pd.read_csv(uploaded_file)  # CSV 파일 로드
    st.session_state["df"] = loaded_data  # 데이터프레임 저장
    st.session_state["python_tool"] = PythonAstREPLTool()  # Python 실행 도구 생성
    st.session_state["python_tool"].locals[
        "df"
    ] = loaded_data  # 데이터프레임을 Python 실행 환경에 추가
    st.session_state["agent"] = create_agent(
        loaded_data, selected_model
    )  # 에이전트 생성
    st.success("설정이 완료되었습니다. 대화를 시작해 주세요!")
elif apply_btn:
    st.warning("파일을 업로드 해주세요.")

print_messages()  # 저장된 메시지 출력

user_input = st.chat_input("궁금한 내용을 물어보세요!")  # 사용자 입력 받기
if user_input:
    ask(user_input)  # 사용자 질문 처리