# app/core/rag/embedding.py
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingModel:
    """文本向量化模型封装（单例模式）"""
    _instance = None

    def __new__(cls, model_name: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name: str = None):
        if self._initialized:
            return
        from app.config import settings
        model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.model = SentenceTransformer(model_name)
        self._initialized = True
        print(f"Loaded embedding model: {model_name}")

    def encode(self, texts: List[str], normalize: bool = True) -> List[List[float]]:
        """将文本列表转换为向量列表"""
        embeddings = self.model.encode(texts, normalize_embeddings=normalize)
        return embeddings.tolist()

    def encode_query(self, query: str) -> List[float]:
        """查询向量化（与文档向量化保持一致）"""
        return self.encode([query])[0]