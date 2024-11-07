### GitHub README.md: Blog Agent ChatBot 💬

---

# Blog Agent ChatBot 💬

### 📖 Introduction
**Blog Agent ChatBot**은 Streamlit 기반의 웹 애플리케이션으로, 사용자가 업로드한 CSV 데이터를 분석하고 자연어 질문에 답변할 수 있도록 설계된 대화형 챗봇입니다. LangChain 및 OpenAI API를 활용하여 데이터 분석, 임베딩, 벡터 검색, 질의응답 기능을 제공합니다.

---

## 🛠️ Features
- **CSV 파일 업로드 및 데이터 분석**
- **OpenAI 모델을 활용한 질의응답**
- **Pandas 데이터프레임 에이전트를 통한 데이터 탐색**
- **벡터 데이터베이스 저장 및 검색 기능**
- **대화 상태 관리**

---

## 🔧 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/BS-KIM-97/AI_ChatBot.git
    cd blog-agent-chatbot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    Create a `.env` file and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

---

## 🚀 Usage

### 1. 파일 업로드 및 모델 선택
- **CSV 파일 업로드**: 사이드바에서 데이터를 업로드합니다.
- **모델 선택**: OpenAI 모델(gpt-4o, gpt-4o-mini)을 선택합니다.
- **데이터 분석 시작**: `데이터 분석 시작` 버튼을 클릭하여 에이전트를 설정합니다.

### 2. 질의응답
- **대화 입력**: 메인 화면에서 자연어 질문을 입력하여 데이터에 대한 질의응답을 수행합니다.
- **결과 확인**: ChatBot이 데이터 분석 및 질문에 대한 답변을 제공합니다.

### 3. 벡터 데이터 저장
- **벡터 데이터 저장**: 분석된 데이터를 벡터 데이터베이스(FAISS)로 저장합니다.
- **파일 저장**: 저장 버튼을 통해 벡터 데이터를 로컬 디스크에 저장합니다.

---

## 📂 Project Structure

```
.
├── main.py                   # Streamlit 메인 애플리케이션
├── Modules/
│   ├── agent.py             # 에이전트 생성 로직
│   ├── call.py              # 질문 및 메시지 처리 로직
│   ├── logging.py           # 로그 설정
│   ├── messages.py          # 메세지 함수
├── requirements.txt         # 의존성 패키지 목록
├── README.md                # 설명서 (현재 파일)
```

---

## 📜 Code Explanation

### 1. **`app.py`**: Main Application

#### 주요 기능
- **Streamlit 설정**:
  - `st.title`로 제목 설정.
  - `st.session_state`로 상태 관리 (대화 내용, 데이터프레임, 에이전트 등).
  
- **사이드바**:
  - CSV 파일 업로드 (`st.file_uploader`).
  - OpenAI 모델 선택 (`st.selectbox`).
  - 데이터 분석 시작 (`apply_btn`).
  
- **데이터 처리**:
  - CSV 파일을 `Pandas DataFrame`으로 로드.
  - LangChain의 `create_agent`를 사용해 데이터프레임 에이전트를 생성.

- **질문 응답**:
  - 사용자 입력을 받아 `ask` 함수 호출.
  - 에이전트가 응답을 스트리밍 형태로 출력.

---

### 2. **`agent.py`**: 에이전트 생성 로직

- **`create_agent`**:
  - LangChain의 `create_pandas_dataframe_agent`를 활용하여 데이터프레임 분석 에이전트를 생성.
  - `prefix`를 사용해 에이전트의 역할 및 제한사항 설정.

---

### 3. **`call.py`**: 질문 및 메시지 처리

#### 주요 함수
- **`ask(query)`**:
  - 사용자 질문을 받아 에이전트에게 전달.
  - 응답을 스트리밍으로 받아 출력.

- **`print_messages()`**:
  - 대화 기록을 반복 출력.
  - 메시지 유형(TEXT, FIGURE, CODE, DATAFRAME)에 따라 적절한 형식으로 출력.

---

### 4. **벡터 데이터 저장**

#### 벡터 데이터 처리 흐름
1. **문서 생성**:
    - `Pandas DataFrame`의 각 행을 LangChain의 `Document` 형식으로 변환.
2. **텍스트 분할**:
    - `RecursiveCharacterTextSplitter`를 사용해 문서를 청크 단위로 분할.
3. **벡터 데이터베이스 생성**:
    - `FAISS`를 사용하여 임베딩된 데이터를 벡터 스토어에 저장.
4. **저장/업데이트**:
    - `FAISS.save_local`로 로컬 저장.
    - 기존 폴더가 있으면 `add_documents`로 추가.

---

## 📌 주요 코드

### 메시지 상태 관리
```python
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # 대화 상태 초기화
```

### CSV 업로드 및 분석
```python
if apply_btn and uploaded_file:
    loaded_data = pd.read_csv(uploaded_file)
    st.session_state["agent"] = create_agent(loaded_data, selected_model)
    st.success("설정이 완료되었습니다.")
```

### 질문 및 응답 처리
```python
user_input = st.chat_input("궁금한 내용을 물어보세요!")
if user_input:
    ask(user_input)
```

### 벡터 데이터 저장
```python
if save_btn and uploaded_file:
    db = FAISS.from_documents(documents=splitted_data, embedding=embeddings)
    db.save_local(folder_path="faiss_db", index_name="faiss_index")
```

---

## 🔑 Environment Variables

다음과 같은 환경 변수를 설정해야 합니다:

- `OPENAI_API_KEY`: OpenAI API 키.

---

## 🛡️ License

This project is licensed under the MIT License.

---

## 📝 Authors

- **Your Name**  
  *AI Enthusiast and Developer*  

Feel free to reach out for collaboration or questions! 😊
