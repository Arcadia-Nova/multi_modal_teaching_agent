# app/services/parse_service.py
from sqlalchemy.orm import Session
from app.core.multimodal.video_parser import VideoParser
from app.models.reference import UploadedFile, ParsedReference, FileType
from app.db.session import SessionLocal


def parse_video_file(file_id: str, file_path: str):
    """后台解析视频文件（同步函数，适合 BackgroundTasks）"""
    db = SessionLocal()
    try:
        # 更新状态为 processing
        db.query(UploadedFile).filter(UploadedFile.file_id == file_id).update({"parsed_status": "processing"})
        db.commit()

        # 解析视频
        parser = VideoParser()
        result = parser.parse_video(file_path)

        # 存储解析结果（摘要）
        parsed = ParsedReference(
            file_id=file_id,
            content_type="video_summary",
            content=result["summary"],
            metadata_json={
                "frame_count": result["frame_count"],
                "detailed_descriptions": result["descriptions"]
            },
            is_summary=1
        )
        db.add(parsed)

        # 更新状态为 completed
        db.query(UploadedFile).filter(UploadedFile.file_id == file_id).update({"parsed_status": "completed"})
        db.commit()
    except Exception as e:
        db.query(UploadedFile).filter(UploadedFile.file_id == file_id).update({"parsed_status": "failed"})
        db.commit()
        raise e
    finally:
        db.close()