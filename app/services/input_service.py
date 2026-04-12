import os
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from app.core.multimodal.image_parser import parse_image
from app.core.multimodal.text_parser import parse_document
from app.core.multimodal.voice_transcriber import VoiceTranscriber
from app.models.reference import UploadedFile, FileType, ParsedReference
from app.models.conversation import Message
from app.utils.file_utils import save_upload_file
from app.config import settings


class InputService:
    def __init__(self, db: Session):
        self.db = db
        self.transcriber = VoiceTranscriber()

    async def process_voice(self, session_id: str, audio_file) -> str:
        """处理语音：保存音频 -> 转文字 -> 保存消息 -> 返回文字"""
        # 1. 保存音频文件
        audio_dir = os.path.join(settings.UPLOAD_DIR, session_id, "audio")
        audio_path = await save_upload_file(audio_file, audio_dir)

        # 2. 转文字
        text = await self.transcriber.transcribe(audio_path)

        # 3. 保存消息到数据库
        message = Message(
            session_id=session_id,
            role="user",
            content=text,
            raw_audio_path=audio_path
        )
        self.db.add(message)
        self.db.commit()

        return text

    def process_text(self, session_id: str, text: str) -> str:
        """处理文字输入：保存消息，返回文本"""
        message = Message(
            session_id=session_id,
            role="user",
            content=text
        )
        self.db.add(message)
        self.db.commit()
        return text

    async def upload_reference(self, session_id: str, file, reference_note: str = None) -> str:
        """上传参考资料，保存记录，返回 file_id"""
        import uuid
        file_id = str(uuid.uuid4())
        file_dir = os.path.join(settings.UPLOAD_DIR, session_id, "refs")
        file_path = await save_upload_file(file, file_dir)

        # 判断文件类型
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in ['.pdf']:
            file_type = FileType.PDF
        elif ext in ['.docx']:
            file_type = FileType.DOCX
        elif ext in ['.pptx']:
            file_type = FileType.PPTX
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            file_type = FileType.IMAGE
        elif ext in ['.mp4', '.avi', '.mov']:
            file_type = FileType.VIDEO
        else:
            file_type = FileType.OTHER

        uploaded_file = UploadedFile(
            session_id=session_id,
            file_id=file_id,
            original_name=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=os.path.getsize(file_path),
            reference_note=reference_note,
            parsed_status="pending",
            uploaded_at=datetime.now()
        )
        self.db.add(uploaded_file)
        self.db.commit()

        # 触发异步解析（可使用 BackgroundTasks）
        # await trigger_parsing(file_id)

        return file_id

    def add_reference_note(self, file_id: str, note: str):
        """为已有文件添加参考说明"""
        file_record = self.db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
        if file_record:
            file_record.reference_note = note
            self.db.commit()


    # ---------- 异步解析任务 ----------
    def _parse_file_async(self, file_id: str, file_path: str, file_type: FileType):
        """后台解析文件（由 BackgroundTasks 调用）"""
        db = self.db  # 注意：BackgroundTasks 中的函数不能直接使用原 db，需新建会话
        from app.db.session import SessionLocal
        db_local = SessionLocal()
        try:
            # 更新状态为 processing
            db_local.query(UploadedFile).filter(UploadedFile.file_id == file_id).update({"parsed_status": "processing"})
            db_local.commit()

            if file_type in (FileType.PDF, FileType.DOCX, FileType.PPTX):
                result = parse_document(file_path)
                self._save_parsed_result(db_local, file_id, "text_summary", result.get("summary", ""), result)
            elif file_type == FileType.IMAGE:
                result = parse_image(file_path)
                self._save_parsed_result(db_local, file_id, "ocr_text", result.get("ocr_text", ""), result)
                self._save_parsed_result(db_local, file_id, "image_description", result.get("blip_description", ""), result)
                # 合并摘要
                summary = f"图像文字: {result.get('ocr_text')}。图像内容: {result.get('blip_description')}"
                self._save_parsed_result(db_local, file_id, "summary", summary, result)
            elif file_type == FileType.VIDEO:
                result = self.video_parser.parse_video(file_path)
                summary = result.get("summary", "")
                self._save_parsed_result(db_local, file_id, "video_summary", summary, result)
                # 也可以存储详细帧描述
                if result.get("descriptions"):
                    self._save_parsed_result(db_local, file_id, "frame_descriptions",
                                             str(result["descriptions"]), result)

            # 更新状态为 completed
            db_local.query(UploadedFile).filter(UploadedFile.file_id == file_id).update({"parsed_status": "completed"})
            db_local.commit()
        except Exception as e:
            db_local.query(UploadedFile).filter(UploadedFile.file_id == file_id).update({"parsed_status": "failed"})
            db_local.commit()
            raise e
        finally:
            db_local.close()

    def _save_parsed_result(self, db, file_id: str, content_type: str, content: str, metadata: dict):
        """保存解析结果到 ParsedReference 表"""
        parsed = ParsedReference(
            file_id=file_id,
            content_type=content_type,
            content=content[:2000],  # 限制长度
            metadata_json=metadata,
            is_summary=1 if content_type == "summary" else 0
        )
        db.add(parsed)
        db.commit()

    def get_parsed_result(self, file_id: str) -> Optional[Dict[str, Any]]:
        """获取文件的解析结果摘要"""
        file_record = self.db.query(UploadedFile).filter(UploadedFile.file_id == file_id).first()
        if not file_record:
            return None
        # 查询该文件的所有解析记录
        parsed_list = self.db.query(ParsedReference).filter(
            ParsedReference.file_id == file_id
        ).all()
        details = {}
        for parsed in parsed_list:
            details[parsed.content_type] = {
                "content": parsed.content,
                "metadata": parsed.metadata_json
            }
        return {
            "status": file_record.parsed_status,
            "summary": details.get("summary", {}).get("content") if details else None,
            "details": details
        }