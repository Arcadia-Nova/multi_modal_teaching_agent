import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile

def generate_unique_filename(original_filename: str) -> str:
    ext = Path(original_filename).suffix
    return f"{uuid.uuid4().hex}{ext}"

async def save_upload_file(upload_file: UploadFile, destination_dir: str) -> str:
    """保存上传文件，返回保存路径"""
    os.makedirs(destination_dir, exist_ok=True)
    new_name = generate_unique_filename(upload_file.filename)
    file_path = os.path.join(destination_dir, new_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return str(Path(file_path).as_posix())