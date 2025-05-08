import os
from datetime import date, datetime
import pandas as pd
from typing import List
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.IO import APIResponse , ChatRequest


from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from api.util.util import *

# LangChain imports
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate
)
from langchain.chains.summarize import load_summarize_chain

from langchain.schema import BaseRetriever, Document
from starlette.concurrency import run_in_threadpool

# --- 환경 설정 ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise RuntimeError("Environment variable OPENAI_API_KEY is required")

# FastAPI 앱 인스턴스 생성
app = FastAPI(title="FestivalBot API", version="1.0")

# production 에서는 제한할것 !!!!!!!!!!!!!!!!!!!!!!!!!!!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LangChain 설정 ---
# 1) 프롬프트 템플릿
SYSTEM_PROMPT = \
"""<ROLE>
You are FestivalBot, a smart assistant for recommending local festivals and events in Korea.

You have access to:
  - A ChromaDB vector store `event_data` with metadata fields.
  - A database tool to fetch event details by event_id.
  - A calendar tool to filter by date ranges.

Retrieval procedure:
  1. **Metadata-first filtering**
     • If the user mentions a station name, filter `event_data` where `station` equals that name.
     • If the user mentions a category, filter `events_data` where `category` equals that category.  
  2. **Fallback to vector search**  
     • If metadata filtering yields insufficient results, perform embedding similarity search.  
  3. **Date filtering**  
     • If the user specifies a date or timeframe (e.g. "this week", "in May"), apply the calendar tool.

Response guidelines:
  - Always reply in Korean, in a friendly and concise tone.
  - Summarize each event with its name, period, and location.
  - Add a brief recommendation note (e.g., “Great for families”).
  - If there are more than three events, mention 1–2 representative ones and group the rest as “etc.”
  - **Fallback recommendation**: If metadata filtering returns zero events:
      1. Acknowledge: “요청하신 지역/카테고리의 축제가 현재 없습니다. 하지만 이런 행사는 어떠세요?”
</ROLE>"""

HUMAN_PROMPT = """
=== Retrieved Documents (after metadata filter + similarity search) ===
{context}

=== User Query ===
{question}

=== Output Format ===
- Recommend events reflecting the user's preferences (date, location, category).
- Provide a concise summary for each event (name, dates, venue).
- If there are more than three events, mention 1–2 and group the rest as “etc.”
- **Fallback recommendation**: If no events match the metadata filters, acknowledge and then recommend 2–3 popular or nearby-area events instead.
"""


# 한국어 요약용 프롬프트
custom_summarize_prompt = PromptTemplate(
    input_variables=["text"], 
    template=
"""
다음 내용을 한국어로 간결하고 명확하게 요약해 주세요:

{text}
"""
)

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(HUMAN_PROMPT)
])

# Retriever 커스텀
# --- Custom Retriever: Metadata-first, then Embedding fallback ---
class MetadataFirstRetriever(BaseRetriever):
    vectordb: Chroma
    k_meta:   int = 10
    k_embed:  int = k_meta * 2

    def __init__(self, vectordb, k_meta=3, k_embed=5):
        # Pass fields to BaseRetriever for Pydantic validation
        super().__init__(vectordb=vectordb, k_meta=k_meta, k_embed=k_embed)
        self.vectordb = vectordb
        self.k_meta   = k_meta
        self.k_embed  = k_embed

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        # Async interface calls sync method in executor
        return await run_in_threadpool(self.get_relevant_documents, query)

    def get_relevant_documents(self, query: str) -> List[Document]:
        parsed      = parse_user_input(query)
        meta_filter = build_meta_filter(parsed)
        print(f"[Retrieval] meta_filter={meta_filter}, k_meta={self.k_meta}")
        docs: List[Document] = []
        
        # 1) Metadata-first filtering if meta_filter exists
        if meta_filter:
            # Apply meta_filter to search_kwargs to filter documents by metadata
            search_kwargs = {
                "filter": meta_filter,  # Apply the metadata filter
                "k": self.k_meta  # Number of results to return
            }
            retr_meta = self.vectordb.as_retriever(search_kwargs=search_kwargs)
            try:
                docs = retr_meta.get_relevant_documents(query)
                print(f"[Retrieval] metadata match count={len(docs)}")
            except Exception as e:
                print(f"[Error] Metadata filtering failed: {e}")
                # Proceed to fallback if metadata filtering fails
        else:
            print("[Retrieval] no metadata filter provided, skipping metadata filtering")

        # 2) Fallback to embedding similarity if needed
        if len(docs) < self.k_meta:
            retr_embed = self.vectordb.as_retriever(
                search_kwargs={"k": self.k_embed}
            )
            try:
                more = retr_embed.get_relevant_documents(query)
                print(f"[Retrieval] Embedding fallback retrieved={len(more)}")
            except Exception as e:
                print(f"[Error] Embedding fallback failed: {e}")
                more = []
            
            # Merge without duplicates
            seen = {d.metadata.get("event_id") for d in docs}
            for d in more:
                if d.metadata.get("event_id") not in seen:
                    docs.append(d)
                    if len(docs) >= self.k_meta:
                        break
                
        print(f"[Retrieval] final docs count={len(docs)}")
        return docs


# catch vector
embedding = OpenAIEmbeddings()

vectordb = Chroma(
    persist_directory="/app/chroma_data",
    embedding_function=embedding,
    collection_name="event_data"
)

# 임베딩 벡터 search 용 질의 체인
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def make_qa_chain(retriever):
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

# description 요약용 질의 체인

# end point
@app.post("/api/events", response_model=APIResponse)
async def get_events(req: ChatRequest):

    retriever = MetadataFirstRetriever(
        vectordb=vectordb,
        k_meta=req.limit,
        k_embed=req.limit * 2
    )
    print("사용자 입력 프롬프트:" ,req.prompt)
    # 체인생성
    qa_chain = make_qa_chain(retriever)

    # 질문시작
    try:
        response = await qa_chain.acall({"query": req.prompt})
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM 처리 중 오류: {e}")

    source_docs = response["source_documents"]

    events = []
    today = date.today().isoformat()
    for doc in source_docs:
        if isinstance(doc, str):
            doc = Document(page_content=doc)

        # doc.metadata에 event_id가 존재하는지 확인
        if "event_id" not in doc.metadata:
            print(f"[Warning] No event_id in metadata: {doc.metadata}")
            continue

        m = doc.metadata
        base ={
        "event_id": str(m.get("event_id")),
        "title": m.get("title", "제목없음"),
        "category": m.get("category", "기타"),
        "location": {
            "name": m.get("location", "알 수 없음"),
            "gu": m.get("gu","알 수 없음"),
            "station":m.get("station","알 수 없음")
        },
        "start_date": m.get("start_date", today),
        "end_date": m.get("end_date", today)
        }

        events.append(base)

    response_payload = {
    "success": True,
    "meta": {
        "queryDate": date.today(),
        "limit":req.limit,
        "timestamp": datetime.now(),
        "returned": len(events)
    },
    "data": events,
    "result": response["result"]
    }

    return response_payload