# app/core/intent/clarifier.py
from typing import List
from app.models.intent import TeachingIntent


class Clarifier:
    """生成追问问题"""

    @staticmethod
    def generate_questions(intent: TeachingIntent) -> List[str]:
        """根据缺失字段，返回问题列表（最多2个，避免轰炸）"""
        missing = intent.missing_fields
        questions = []

        if "subject" in missing:
            questions.append("请问您要讲授哪个学科？（例如：初中物理、高中化学）")
        if "topic" in missing:
            questions.append("本节课的核心主题是什么？")
        if "key_points" in missing:
            questions.append("请列出本节课需要讲解的主要知识点。")
        if "duration_minutes" in missing:
            questions.append("预计课堂时长是多少分钟？")

        # 如果知识点已提供但重难点缺失，可以追问
        if intent.key_points and not intent.difficult_points:
            questions.append("其中哪些是学生较难理解的重难点？")

        return questions[:2]  # 一次最多问2个

    @staticmethod
    def generate_summary(intent: TeachingIntent) -> str:
        """生成意图摘要，用于向教师确认"""
        lines = []
        if intent.subject:
            lines.append(f"学科：{intent.subject}")
        if intent.topic:
            lines.append(f"主题：{intent.topic}")
        if intent.key_points:
            lines.append(f"知识点：{', '.join(intent.key_points)}")
        if intent.difficult_points:
            lines.append(f"重难点：{', '.join(intent.difficult_points)}")
        if intent.duration_minutes:
            lines.append(f"时长：{intent.duration_minutes}分钟")
        if intent.teaching_style:
            lines.append(f"教学风格：{intent.teaching_style}")
        return "\n".join(lines) if lines else "尚未提取到完整信息"