# app/core/fusion/instruction_builder.py
import json
from typing import List
from app.core.fusion.schema import FusionContext, ReferenceFragment, RetrievalFragment

class InstructionBuilder:
    def __init__(self, llm_client):
        self.llm = llm_client

    def _aggregate_references(self, references: List[ReferenceFragment]) -> str:
        """将参考资料片段聚合成文本块，突出教师标注的内容"""
        aggregated = []
        for ref in references:
            note_prefix = f"[教师要求：{ref.reference_note}] " if ref.reference_note else ""
            aggregated.append(f"文件《{ref.file_name}》{note_prefix}\n{ref.content}")
        return "\n\n".join(aggregated)

    def _aggregate_retrieval(self, retrieval: List[RetrievalFragment]) -> str:
        """将检索结果聚合成文本块"""
        if not retrieval:
            return "无"
        parts = [f"【来源：{r.source}】{r.content}" for r in retrieval]
        return "\n\n".join(parts)

    def build(self, context: FusionContext) -> dict:
        """
        融合所有信息，生成课件指令集
        """
        # 1. 准备各部分文本
        intent_text = self._intent_to_text(context.intent)
        references_text = self._aggregate_references(context.references)
        retrieval_text = self._aggregate_retrieval(context.retrieval)

        # 2. 构建系统提示词
        system_prompt = """
你是一位专业的教学设计师，负责将教师的教学意图和参考资料转化为详细的课件生成指令。
请根据以下输入，输出一个JSON对象，包含生成PPT、Word教案、互动游戏所需的所有信息。

输出JSON结构必须严格按照以下格式：
{
  "title": "课件标题",
  "slides": [
    {"type": "cover", "title": "...", "subtitle": "..."},
    {"type": "catalog", "items": ["章节1", "章节2"]},
    {"type": "content", "title": "知识点", "bullet_points": ["点1", "点2"], "image_hint": "建议配图描述"},
    {"type": "summary", "content": "总结内容"}
  ],
  "teaching_process": [
    {"step": "导入", "duration": 5, "activity": "活动描述"},
    {"step": "新授", "duration": 20, "activity": "..."},
    {"step": "巩固", "duration": 10, "activity": "..."},
    {"step": "小结", "duration": 5, "activity": "..."}
  ],
  "game_requirement": {
    "type": "quiz",   // 可选 "quiz", "drag_drop", "flip_card"
    "topic": "主题",
    "questions": 3,
    "style": "选择题/判断题"
  },
  "style_preferences": {
    "theme_color": "blue/green/orange",
    "font_size": "normal/large"
  }
}

要求：
- 幻灯片数量控制在5-8页。
- 教学过程总时长应与教师意图中的duration_minutes匹配（默认45分钟）。
- 如果教师要求互动游戏，则game_requirement必填；否则可为null。
- 内容必须参考提供的参考资料和检索知识库，优先使用教师标注的内容。
- 只输出JSON，不要有其他解释。
"""
        # 3. 构建用户提示词
        user_prompt = f"""
教师教学意图：
{intent_text}

参考资料解析结果（已按教师要求标注）：
{references_text}

知识库检索相关片段：
{retrieval_text}

请生成课件指令集（JSON）：
"""
        # 4. 调用大模型
        response = self.llm.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0.3)

        # 5. 解析JSON并校验
        try:
            instruction = json.loads(response)
        except json.JSONDecodeError:
            # 降级：使用规则生成简单指令
            instruction = self._fallback_instruction(context)

        # 6. 补充默认值
        instruction = self._validate_and_fill(instruction, context)
        return instruction

    def _intent_to_text(self, intent: dict) -> str:
        lines = []
        if intent.get("subject"):
            lines.append(f"学科：{intent['subject']}")
        if intent.get("topic"):
            lines.append(f"主题：{intent['topic']}")
        if intent.get("key_points"):
            lines.append(f"核心知识点：{', '.join(intent['key_points'])}")
        if intent.get("difficult_points"):
            lines.append(f"重难点：{', '.join(intent['difficult_points'])}")
        if intent.get("duration_minutes"):
            lines.append(f"时长：{intent['duration_minutes']}分钟")
        if intent.get("teaching_style"):
            lines.append(f"教学风格：{intent['teaching_style']}")
        if intent.get("special_requirements"):
            lines.append(f"特殊要求：{', '.join(intent['special_requirements'])}")
        return "\n".join(lines) if lines else "无"

    def _fallback_instruction(self, context: FusionContext) -> dict:
        """当大模型解析失败时，生成最简单的指令集"""
        topic = context.intent.get("topic", "课件")
        return {
            "title": topic,
            "slides": [
                {"type": "cover", "title": topic, "subtitle": "AI生成课件"},
                {"type": "content", "title": "主要内容", "bullet_points": ["待补充"], "image_hint": None}
            ],
            "teaching_process": [
                {"step": "导入", "duration": 5, "activity": "导入活动"},
                {"step": "新授", "duration": 30, "activity": "知识点讲解"},
                {"step": "小结", "duration": 10, "activity": "总结"}
            ],
            "game_requirement": None,
            "style_preferences": {"theme_color": "blue"}
        }

    def _validate_and_fill(self, instruction: dict, context: FusionContext) -> dict:
        """确保指令集包含必要字段"""
        if not instruction.get("title"):
            instruction["title"] = context.intent.get("topic", "未命名课件")
        if not instruction.get("slides") or len(instruction["slides"]) < 2:
            instruction["slides"] = self._fallback_instruction(context)["slides"]
        if not instruction.get("teaching_process"):
            instruction["teaching_process"] = self._fallback_instruction(context)["teaching_process"]
        # 确保每个slide有type
        for slide in instruction["slides"]:
            if "type" not in slide:
                slide["type"] = "content"
        return instruction

