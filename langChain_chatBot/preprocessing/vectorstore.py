#
# 모듈 불러오기
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from Modules import logging
from dotenv import load_dotenv

# 환경설정

# 데이터 패스
DATA_PATH = "data/"

# langsmith 함수 
logging.langsmith("Search for documents")

#데이터 로드 (CSV)
loader = CSVLoader(
    file_path = DATA_PATH + "qna_re.csv", 
    encoding="utf-8",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames":"combined"
    },
)
# docs 변수 정의
docs = loader.load()

# 스플릿
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# 임배딩 모델 정의
# text-embedding-3-small 모델 사용
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# DB저장
# Faiss DB 사용
db = FAISS.from_documents(documents = split_documents, embedding = embeddings)

# 로컬에 저장
db.save_local(folder_path="faiss_db", index_name="faiss_index")