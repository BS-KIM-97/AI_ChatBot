
# 모듈
import os
from typing import List, Union
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_experimental.tools import PythonAstREPLTool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader


# env
load_dotenv()
logging.langsmith("Blog Agent ChatBot")

# 실행
st.title("Blog Agent ChatBot 💬")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # 대화 내용을 저장할 리스트 초기화

# 임베딩
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# 임베딩 차원 크기를 계산
dimension_size = len(embeddings.embed_query("hello world"))


# 사이드바 설정
with st.sidebar:
    clear_btn = st.button("대화 초기화")  # 대화 내용을 초기화하는 버튼
    uploaded_file = st.file_uploader(
        "CSV 파일을 업로드 해주세요.", type=["csv"]
    )  # CSV 파일 업로드 기능
    selected_model = st.selectbox(
        "OpenAI 모델을 선택해주세요.", ["gpt-4o", "gpt-4o-mini"], index=0
    )  # OpenAI 모델 선택 옵션
    apply_btn = st.button("데이터 분석 시작")  # 데이터 분석을 시작하는 버튼
    save_btn = st.button("파일 저장 버튼") # 파일을 저장하는 버튼

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
    

#파일 확인 함수
def check_folder_exists(directory, folder_name):
    """
    특정 디렉토리에 폴더가 존재하는지 확인하는 함수.
    
    Args:
        directory (str): 확인할 디렉토리 경로.
        folder_name (str): 확인할 폴더 이름.
    
    Returns:
        bool: 폴더가 존재하면 True, 없으면 False.
    """
    folder_path = os.path.join(directory, folder_name)
    return os.path.isdir(folder_path)

#디렉토리 확인
directory = "C:\WorkSpace\AI_ChatBot\OrgBot"
folder_name = "faiss_db"



if save_btn and uploaded_file:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    
    loader = CSVLoader(file_path=uploaded_file, encoding='utf-8')
    
    documents = loader.load()
    
    splitted_data = text_splitter.split_documents(loaded_data)
    
    db = FAISS.from_documents(documents=splitted_data, embedding=embeddings)
    
    if check_folder_exists(directory, folder_name):
        print(f"폴더 '{folder_name}'가 존재합니다.")
        db.add_documents()
    else:
        db = FAISS(
            embedding_function=embeddings,
            index=faiss.IndexFlatL2(dimension_size),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        print(f"폴더 '{folder_name}'가 존재하지 않아 생성 후 저장합니다.")
        


