"""
输入处理服务
"""
from typing import Optional, Dict, Any
from pathlib import Path
from app.config import settings


class InputService:
    """
    输入处理服务类
    """
    
    def process_input_file(self, file_path: str) -> Dict[str, Any]:
        """
        处理输入文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        # 简单的文件处理逻辑
        file = Path(file_path)
        
        if not file.exists():
            return {
                'status': 'error',
                'message': '文件不存在'
            }
        
        # 检查文件类型
        file_extension = file.suffix.lower()
        
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            return {
                'status': 'error',
                'message': '不支持的文件类型'
            }
        
        return {
            'status': 'success',
            'file_path': str(file),
            'file_type': file_extension,
            'file_size': file.stat().st_size
        }
