# app/core/rag/vector_store.py
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional
from app.core.rag.embedding import EmbeddingModel


class ChromaVectorStore:
    """Chroma 向量数据库封装"""

    def __init__(self, collection_name: str, persist_directory: str):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embed_model = EmbeddingModel()

        # 自定义 embedding 函数，使 Chroma 使用我们的模型
        class CustomEmbeddingFunction(embedding_functions.EmbeddingFunction):
            def __init__(self, embed_model):
                self.embed_model = embed_model

            def __call__(self, input: List[str]) -> List[List[float]]:
                return self.embed_model.encode(input)

        self.embed_fn = CustomEmbeddingFunction(self.embed_model)

        # 获取或创建集合
        existing_collections = [c.name for c in self.client.list_collections()]
        if collection_name in existing_collections:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embed_fn
            )
        else:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embed_fn
            )

    def add_documents(self, ids: List[str], documents: List[str], metadatas: Optional[List[Dict]] = None):
        """批量添加文档"""
        if metadatas is None:
            metadatas = [{}] * len(documents)
        # 分批添加避免内存问题
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                ids=ids[i:i + batch_size],
                documents=documents[i:i + batch_size],
                metadatas=metadatas[i:i + batch_size]
            )

    def similarity_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """向量相似度检索，返回文档内容和元数据"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        if not results['documents']:
            return []
        return [
            {
                "content": doc,
                "metadata": meta,
                "distance": dist
            }
            for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
        ]

    def delete_collection(self):
        """删除整个集合（慎用）"""
        self.client.delete_collection(self.collection.name)