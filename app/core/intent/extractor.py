<<<<<<< Updated upstream
=======
# app/core/intent/extractor.py
import json
from typing import Dict, List, Optional

from app.core.generator import llm_client
from app.core.generator.llm_client import LLMClient  # 假设已封装
from app.models.intent import TeachingIntent


class IntentExtractor:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def extract(self, conversation_history: List[Dict[str, str]]) -> TeachingIntent:
        """
        从对话历史中提取教学意图。
        conversation_history: [{"role": "user/assistant", "content": "..."}]
        """
        # 构建 prompt
        system_prompt = """
你是一位专业的教学助手，擅长从对话中提取教师的教学意图。
请分析以下教师与助手的对话，提取结构化的教学信息，输出 JSON 格式。
如果某些信息未提及，对应字段设为 null 或空列表。

字段说明：
- subject: 学科（如“初中物理”、“高中化学”）
- topic: 教学主题（如“欧姆定律”、“光的折射”）
- key_points: 核心知识点列表（至少一个）
- difficult_points: 重难点列表
- duration_minutes: 课堂时长（整数，单位分钟）
- teaching_style: 教学风格（“讲授式”、“探究式”、“案例式”之一）
- target_audience: 目标学段（“初中”、“高中”、“大学”）
- special_requirements: 特殊要求列表（如“需要互动游戏”、“多举例”）

注意：
1. 只输出 JSON，不要有其他解释。
2. 如果对话中教师未明确说明，可以结合上下文合理推断，但不要编造。
3. 如果信息明显缺失，将对应字段设为 null。
"""
        user_prompt = f"对话历史：\n{self._format_history(conversation_history)}\n请提取教学意图："

        # self.llm = LLMClient()

        response = self.llm.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0.2)


        # 解析 JSON
        try:
            data = json.loads(response)
            intent = TeachingIntent(**data)
        except Exception as e:
            # 降级：返回空意图
            intent = TeachingIntent()

        # 计算缺失字段
        intent.missing_fields = self._get_missing_fields(intent)
        intent.is_complete = len(intent.missing_fields) == 0
        return intent

    def _format_history(self, history: List[Dict]) -> str:
        lines = []
        for msg in history:
            role = "教师" if msg["role"] == "user" else "助手"
            lines.append(f"{role}: {msg['content']}")
        return "\n".join(lines)

    def _get_missing_fields(self, intent: TeachingIntent) -> List[str]:
        missing = []
        if not intent.subject:
            missing.append("subject")
        if not intent.topic:
            missing.append("topic")
        if not intent.key_points:
            missing.append("key_points")
        if not intent.duration_minutes:
            missing.append("duration_minutes")
        # 可根据需要增加
        return missing
>>>>>>> Stashed changes
