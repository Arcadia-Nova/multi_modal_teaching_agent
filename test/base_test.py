import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader


def build_knowledge_base(collection_name: str = "teaching_knowledge_base", settings=None):
    """扫描 knowledge_base/documents 并构建索引"""

    # 假设settings对象的模拟实现
    class DefaultSettings:
        KNOWLEDGE_BASE_DIR = "../knowledge_base/documents"
        CHUNK_SIZE = 500
        CHUNK_OVERLAP = 50

    if settings is None:
        settings = DefaultSettings()

    docs_dir = settings.KNOWLEDGE_BASE_DIR
    print(f"正在检查知识库目录: {docs_dir}")

    if not os.path.exists(docs_dir):
        print(f"❌ 知识库目录不存在: {docs_dir}")
        return

    # 列出目录中的所有文件
    files_in_dir = os.listdir(docs_dir)
    print(f"📁 目录中的文件: {files_in_dir}")

    supported_extensions = ['.pdf', '.docx', '.pptx']
    supported_files = [f for f in files_in_dir if any(f.lower().endswith(ext) for ext in supported_extensions)]
    unsupported_files = [f for f in files_in_dir if not any(f.lower().endswith(ext) for ext in supported_extensions)]

    print(f"✅ 支持的文件: {supported_files}")
    print(f"❌ 不支持的文件: {unsupported_files}")

    all_chunks = []

    for file_name in files_in_dir:
        file_path = os.path.join(docs_dir, file_name)

        # 检查是否为文件（排除子目录）
        if not os.path.isfile(file_path):
            print(f"⚠️ 跳过非文件项: {file_name}")
            continue

        if file_name.lower().endswith(".pdf"):
            print(f"📄 检测到PDF文件: {file_name}")
            try:
                loader = PyPDFLoader(file_path)
            except Exception as e:
                print(f"❌ 加载PDF文件失败 {file_name}: {e}")
                continue
        elif file_name.lower().endswith(".docx"):
            print(f"📄 检测到DOCX文件: {file_name}")
            try:
                loader = Docx2txtLoader(file_path)
            except Exception as e:
                print(f"❌ 加载DOCX文件失败 {file_name}: {e}")
                continue
        elif file_name.lower().endswith(".pptx"):
            print(f"📊 检测到PPTX文件: {file_name}")
            try:
                loader = UnstructuredPowerPointLoader(file_path)
            except Exception as e:
                print(f"❌ 加载PPTX文件失败 {file_name}: {e}")
                continue
        else:
            print(f"⏭️ 跳过不支持的文件类型: {file_name}")
            continue

        print(f"🔄 加载文件: {file_name}")
        try:
            docs = loader.load()
            print(f"📝 文件 {file_name} 加载成功，共 {len(docs)} 个文档")

            # 这里需要模拟chunk_documents函数
            def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
                # 简化的分块逻辑示例
                chunks = []
                for doc in docs:
                    text = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                    # 简单按长度分块
                    for i in range(0, len(text), chunk_size - chunk_overlap):
                        chunk_text = text[i:i + chunk_size]
                        # 创建简单的文档对象
                        chunk_doc = type('Document', (), {'page_content': chunk_text, 'metadata': {}})()
                        chunks.append(chunk_doc)
                return chunks

            chunks = chunk_documents(docs, chunk_size=getattr(settings, 'CHUNK_SIZE', 500),
                                     chunk_overlap=getattr(settings, 'CHUNK_OVERLAP', 50))
            print(f"✂️ 文件 {file_name} 分块完成，共 {len(chunks)} 个块")
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"❌ 处理文件 {file_name} 时出错: {e}")
            continue

    print(f"📚 总共处理了 {len(all_chunks)} 个文档块")

    if not all_chunks:
        print("⚠️ 未找到任何可处理的文档。")
        print("💡 请检查以下几点:")
        print("   1. 文件是否确实存在于 knowledge_base/documents 目录中")
        print("   2. 文件扩展名是否正确 (.pdf, .docx, .pptx)")
        print("   3. 文件是否损坏或无法读取")
        print("   4. 是否有权限访问这些文件")
        return False
    else:
        print(f"✅ 成功构建知识库，共处理 {len(supported_files)} 个文件")
        return True


# 使用示例
if __name__ == "__main__":
    # 创建一个简单的settings对象
    class MySettings:
        KNOWLEDGE_BASE_DIR = "../knowledge_base/documents"
        CHUNK_SIZE = 500
        CHUNK_OVERLAP = 50


    settings = MySettings()
    build_knowledge_base(settings=settings)