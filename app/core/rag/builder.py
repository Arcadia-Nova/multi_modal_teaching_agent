# app/core/rag/builder.py
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings
from app.core.rag.vector_store import ChromaVectorStore


def chunk_documents(docs: List[Document], chunk_size: int = 512, chunk_overlap: int = 64) -> List[Document]:
    """递归字符文本分割，保留语义结构"""
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "；", "，", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_documents(docs)


def build_knowledge_base(collection_name: str = "teaching_knowledge_base"):
    """扫描 knowledge_base/documents 并构建索引"""
    docs_dir = settings.KNOWLEDGE_BASE_DIR
    if not os.path.exists(docs_dir):
        print(f"知识库目录不存在: {docs_dir}")
        return

    all_chunks = []
    print(len(os.listdir(docs_dir)))
    for file_name in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, file_name)
        print(file_path,file_name)
        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file_name.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(file_path)
        else:
            continue
        print(f"加载文件: {file_name}")
        docs = loader.load()
        chunks = chunk_documents(docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("未找到任何可处理的文档。")
        return

    # 准备数据
    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    texts = [chunk.page_content for chunk in all_chunks]
    metadatas = [chunk.metadata for chunk in all_chunks]

    # 存入向量库
    vector_store = ChromaVectorStore(collection_name, settings.VECTOR_STORE_PATH)
    vector_store.add_documents(ids, texts, metadatas)
    print(f"知识库构建完成，共 {len(all_chunks)} 个文本块。")


if __name__ == "__main__":
    # 直接运行此脚本可离线构建
    build_knowledge_base()