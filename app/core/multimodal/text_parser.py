# app/core/multimodal/text_parser.py
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPowerPointLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from typing import Dict, Any
import os


def parse_document(file_path: str) -> Dict[str, Any]:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        loader = PyPDFLoader(file_path)
    elif ext == '.docx':
        loader = Docx2txtLoader(file_path)
    elif ext == '.pptx':
        loader = UnstructuredPowerPointLoader(file_path)
    else:
        return {"error": "Unsupported document type"}

    pages = loader.load()
    full_text = "\n".join([page.page_content for page in pages])


    return {
        "full_text": full_text,
        "page_count": len(pages),
        "summary": full_text[:3000] + "..."  # 简单截取作为摘要
    }