# app/core/rag/builder.py
import hashlib
import json
import os
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings,BASE_DIR,KNOWLEDGE_BASE_DIR
from app.core.rag.vector_store import ChromaVectorStore

# 状态文件路径（保存在向量库目录下）
STATE_FILE = os.path.join(settings.VECTOR_STORE_PATH, "build_state.json")

def chunk_documents(docs: List[Document], chunk_size: int = 512, chunk_overlap: int = 64) -> List[Document]:
    """递归字符文本分割，保留语义结构"""
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "；", "，", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_documents(docs)

def _get_file_hash(file_path: str) -> str:
    """生成文件路径的唯一标识（用于ID前缀）"""
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()[:8]

def _get_chunk_id(file_path: str, chunk_index: int) -> str:
    """生成单个块的唯一ID"""
    return f"{_get_file_hash(file_path)}_{chunk_index}"

def _get_all_chunk_ids_for_file(file_path: str, num_chunks: int) -> List[str]:
    """生成某个文件所有块的ID列表"""
    return [_get_chunk_id(file_path, i) for i in range(num_chunks)]

def _load_build_state() -> Dict:
    """加载上次构建的状态"""
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_build_state(state: Dict):
    """保存构建状态"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def _process_file(file_path: str, vector_store: ChromaVectorStore) -> int:
    """
    处理单个文件：加载、分块、添加到向量库
    返回添加的块数量
    """
    file_name = os.path.basename(file_path)
    if file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_name.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_name.endswith(".pptx"):
        loader = UnstructuredPowerPointLoader(file_path)
    else:
        print(f"跳过不支持的文件类型: {file_name}")
        return 0

    print(f"处理文件: {file_name}")
    docs = loader.load()
    chunks = chunk_documents(docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    if not chunks:
        return 0

    # 生成 ID、文本、元数据
    ids = []
    texts = []
    metadatas = []
    for idx, chunk in enumerate(chunks):
        ids.append(_get_chunk_id(file_path, idx))
        texts.append(chunk.page_content)
        meta = chunk.metadata.copy()
        meta['source_file'] = file_name
        metadatas.append(meta)

    # 使用 upsert 添加（若已有则覆盖，但通常我们会先删除旧块，确保干净）
    # 更安全的做法：先删除该文件的所有旧块，再添加新块
    vector_store.delete_by_metadata({"source_file": file_name})
    vector_store.upsert_documents(ids, texts, metadatas)
    print(f"  已添加 {len(ids)} 个块")
    return len(ids)

def build_knowledge_base_incremental(collection_name: str = "teaching_knowledge_base"):
    """增量构建知识库：仅处理新增或修改的文件"""
    docs_dir = settings.KNOWLEDGE_BASE_DIR
    print("当前工作目录:", os.getcwd())
    print("文档目录绝对路径:", os.path.abspath(docs_dir))
    print("目录是否存在:", os.path.exists(docs_dir))
    if not os.path.exists(docs_dir):
        print(f"知识库目录不存在: {docs_dir}")
        return

    # 初始化向量库
    vector_store = ChromaVectorStore(collection_name, settings.VECTOR_STORE_PATH)

    # 加载上次构建状态
    old_state = _load_build_state()  # 格式: {"file_path": mtime, ...}
    new_state = {}

    # 获取当前所有文件及其 mtime
    current_files = {}
    for file_name in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, file_name)
        if not os.path.isfile(file_path):
            continue
        # 只处理支持的扩展名
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in ['.pdf', '.docx', '.pptx']:
            continue
        mtime = os.path.getmtime(file_path)
        current_files[file_path] = mtime

    # 检测需要删除的文件（在旧状态中存在但当前目录已无）
    files_to_delete = set(old_state.keys()) - set(current_files.keys())
    for file_path in files_to_delete:
        file_name = os.path.basename(file_path)
        print(f"检测到已删除文件: {file_name}，从向量库中移除")
        vector_store.delete_by_metadata({"source_file": file_name})

    # 处理新增或修改的文件
    for file_path, mtime in current_files.items():
        file_name = os.path.basename(file_path)
        old_mtime = old_state.get(file_path)
        if old_mtime is None:
            print(f"新增文件: {file_name}")
            _process_file(file_path, vector_store)
        elif abs(mtime - old_mtime) > 0.1:  # 允许微小误差
            print(f"文件已修改: {file_name}")
            _process_file(file_path, vector_store)
        else:
            print(f"文件未变化: {file_name}，跳过")
        # 无论是否处理，都记录当前 mtime
        new_state[file_path] = mtime

    # 保存新状态
    _save_build_state(new_state)
    print("增量构建完成")

def build_knowledge_base_full(collection_name: str = "teaching_knowledge_base"):
    """全量构建（原逻辑，保留作为备用）"""
    docs_dir = settings.KNOWLEDGE_BASE_DIR
    print("主目录:",BASE_DIR,",",KNOWLEDGE_BASE_DIR)
    print("当前工作目录:", os.getcwd())
    print("文档目录绝对路径:", os.path.abspath(docs_dir))
    print("目录是否存在:", os.path.exists(docs_dir))
    if not os.path.exists(docs_dir):
        print(f"知识库目录不存在: {docs_dir}")
        return

    all_ids = []
    all_texts = []
    all_metadatas = []
    current_files = {}  # 新增：记录当前文件及其修改时间

    for file_name in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, file_name)
        if not os.path.isfile(file_path):
            continue
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in ['.pdf', '.docx', '.pptx']:
            continue

        # 记录文件修改时间
        current_files[file_path] = os.path.getmtime(file_path)

        print(f"加载文件: {file_name}")
        if file_name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_name.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file_name.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(file_path)
        else:
            continue

        docs = loader.load()
        chunks = chunk_documents(docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)

        for idx, chunk in enumerate(chunks):
            unique_id = _get_chunk_id(file_path, idx)
            all_ids.append(unique_id)
            all_texts.append(chunk.page_content)
            metadata = chunk.metadata.copy()
            metadata['source_file'] = file_name
            all_metadatas.append(metadata)

    if not all_texts:
        print("未找到任何可处理的文档。")
        return

    vector_store = ChromaVectorStore(collection_name, settings.VECTOR_STORE_PATH)
    # 全量构建前可清空集合（例如删除集合后重建）
    # 简单起见：删除集合再重新创建
    try:
        vector_store.delete_collection()
    except Exception:
        pass  # 集合不存在时忽略
    # 重新创建集合（在 ChromaVectorStore 初始化时会自动创建）
    vector_store = ChromaVectorStore(collection_name, settings.VECTOR_STORE_PATH)
    vector_store.upsert_documents(all_ids, all_texts, all_metadatas)
    print(f"全量构建完成，共 {len(all_texts)} 个文本块。")

    # 保存状态（记录当前所有文件的修改时间）
    new_state = {fp: mtime for fp, mtime in current_files.items()}
    _save_build_state(new_state)

if __name__ == "__main__":
    # 默认使用增量构建，也可改为全量构建
    build_knowledge_base_full()