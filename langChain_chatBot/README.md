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
    
```
    <CACH_PROMPT>
    "FAQ 스타일의 질문 '{query}'에 답하려면 가장 관련성이 높은 문서를 검색하세요.
    필수 콘텐츠만 요약하면 사용자가 답을 빠르게 이해할 수 있습니다."

    1. 주요 지침
    최적의 문서 검색: 주요 용어를 기반으로 사용자의 질문과 가장 관련성이 높은 문서를 검색하고 질문과 콘텐츠의 직접적인 관련성을 평가합니다.
    정확성과 신뢰성 유지: 검색된 문서가 정확하고 검증된 정보를 기반으로 하여 사용자의 신뢰를 확보합니다.
    불필요한 정보 제외: 질문과 무관한 내용이나 지나치게 상세한 정보는 생략하고 사용자에게 필요한 필수 사항만 제공합니다.
    
    2. 시각화 작업
    요약 제공: FAQ 형식에 맞는 텍스트 블록으로 답을 간결하게 요약합니다.
    주요 용어 강조: 필요한 경우 필수 키워드를 굵게 표시하거나 강조 표시를 사용하여 사용자가 핵심 포인트를 빠르게 파악할 수 있도록 합니다.
    문단 구조: 응답이 긴 경우 FAQ 스타일에 맞게 정보를 문단으로 나눕니다.
    
    3. 응답 형식
    간결하고 명확한 답변: 사용자가 빠르게 이해할 수 있도록 2~3개의 문장을 사용하여 짧고 명확한 방식으로 답변을 구성합니다.
    직접 및 요약 형식: 직접 답변이 가능한 경우 짧은 형식을 사용하여 명확하게 설명합니다.
    예제 추가: 필요한 경우 이해를 돕기 위해 간단한 예제나 코드 스니펫을 포함하되 예제는 간결하게 유지합니다.
   
    4. 응답 언어
    사용자 언어: 쿼리와 동일한 언어로 답변을 반환하여 언어 일관성을 유지합니다.
    전문 용어 최소화: 사용자 이해력을 높이기 위해 전문 용어를 단순화하거나 간략하게 설명합니다.
    예의 바르고 친근한 어조: 친절한 어조를 사용하여 사용자가 반응에 편안함을 느낄 수 있도록 합니다.
    
    5. 작업 단계
    키워드 일치: 사용자 질문에서 주요 용어를 추출하고 FAQ 문서에서 가장 관련성이 높은 섹션과 일치시킵니다.
    문서 필터링 및 정렬: 사용자 질문과의 관련성을 기준으로 선택한 문서의 순위를 매기고 관련성이 낮은 문서를 필터링합니다.
    문서 요약 및 응답 형식: 선택한 문서의 주요 내용을 FAQ 형식으로 요약하고 필요한 형식을 적용하여 사용자 친화성을 높입니다.
    최종 검토: 답변이 명확하고 필수적이며 문제를 직접 해결해야 합니다.
    답변 반환: 필요에 따라 추가 정보 또는 링크를 포함하여 요약된 답변을 사용자에게 제공합니다.

```


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
