# app/core/rag/retriever.py
from typing import List, Dict, Optional
from app.core.rag.vector_store import ChromaVectorStore
from app.config import settings


class Retriever:
    """知识库检索器"""

    def __init__(self, collection_name: str = "teaching_knowledge_base"):
        self.store = ChromaVectorStore(
            collection_name=collection_name,
            persist_directory=settings.VECTOR_STORE_PATH
        )
        self.top_k = settings.TOP_K_RETRIEVAL

    def retrieve(self, query: str, top_k: Optional[int] = None, filter_metadata: Optional[Dict] = None) -> List[Dict]:
        """
        检索相关文档片段。
        Args:
            query: 查询文本
            top_k: 返回数量，默认使用配置值
            filter_metadata: 元数据过滤条件（例如 {"source": "curriculum.pdf"}）
        Returns:
            包含 content, metadata, distance 的列表
        """
        k = top_k or self.top_k
        results = self.store.similarity_search(query, top_k=k)
        if filter_metadata:
            results = [r for r in results if all(r['metadata'].get(k) == v for k, v in filter_metadata.items())]
        return results

    def retrieve_context_str(self, query: str, top_k: Optional[int] = None) -> str:
        """检索并返回拼接的上下文字符串，便于直接放入 prompt"""
        docs = self.retrieve(query, top_k)
        if not docs:
            return ""
        context_parts = []
        for idx, doc in enumerate(docs):
            source = doc['metadata'].get('source', 'unknown')
            context_parts.append(f"【来源：{source}】\n{doc['content']}")
        return "\n\n".join(context_parts)