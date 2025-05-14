from typing import List

from langchain_chroma import Chroma
from langchain.schema import BaseRetriever,Document
from api.util.util import *

from starlette.concurrency import run_in_threadpool

# Retriever
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
        parsed      = parse_user_input(query) # user defined function
        meta_filter = build_meta_filter(parsed)
        print(f"[Retrieval] meta_filter={meta_filter}, k_meta={self.k_meta}")
        docs: List[Document] = []
        
        # Metadata-first filtering if meta_filter exists
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

        # Fallback to embedding similarity if needed
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