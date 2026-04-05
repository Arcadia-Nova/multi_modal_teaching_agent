import cv2
from typing import List, Dict
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from app.config import settings


class VideoParser:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)

    def extract_frames(self, video_path: str) -> List[Image.Image]:
        """从视频中提取关键帧（PIL Image 列表）"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 计算抽帧间隔（帧数）
        frame_interval = max(1, int(fps * settings.VIDEO_FRAME_INTERVAL_SEC))

        frames = []
        frame_count = 0
        while len(frames) < settings.MAX_VIDEO_FRAMES:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                # OpenCV BGR -> RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                frames.append(pil_img)
            frame_count += 1
        cap.release()
        return frames

    def generate_description(self, image: Image.Image) -> str:
        """生成单帧图像的英文描述"""
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs)
        desc = self.processor.decode(out[0], skip_special_tokens=True)
        return desc

    def parse_video(self, video_path: str) -> Dict:
        """解析视频，返回结构化结果"""
        frames = self.extract_frames(video_path)
        if not frames:
            return {"frame_count": 0, "descriptions": [], "summary": "无法从视频中提取有效帧"}

        descriptions = []
        for idx, img in enumerate(frames):
            desc = self.generate_description(img)
            timestamp_sec = idx * settings.VIDEO_FRAME_INTERVAL_SEC
            descriptions.append({
                "timestamp": timestamp_sec,
                "description": desc
            })

        # 生成整体摘要：按时间顺序拼接
        summary_parts = [f"{d['timestamp']}秒: {d['description']}" for d in descriptions]
        summary = "；".join(summary_parts)

        return {
            "frame_count": len(frames),
            "descriptions": descriptions,
            "summary": summary
        }