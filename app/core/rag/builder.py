"""
知识库构建模块
"""
from typing import List, Optional
from pathlib import Path
from app.config import settings


def build_knowledge_base(directory: Optional[str] = None):
    """
    构建知识库
    
    Args:
        directory: 知识库目录路径
        
    Returns:
        bool: 构建是否成功
    """
    # 简单的知识库构建逻辑
    if directory is None:
        directory = settings.KNOWLEDGE_BASE_DIR
    
    knowledge_dir = Path(directory)
    
    # 确保知识库目录存在
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    
    # 列出目录中的文件
    files = list(knowledge_dir.glob("*"))
    print(f"知识库目录包含 {len(files)} 个文件")
    
    # 这里可以添加实际的知识库构建逻辑
    # 例如：文本分割、嵌入生成、向量存储等
    
    return True
