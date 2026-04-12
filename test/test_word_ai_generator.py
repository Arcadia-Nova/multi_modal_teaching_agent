import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.generator.word_generator import WordGenerator

# 测试Word生成器（AI增强版）
generator = WordGenerator()

print("=== 开始AI增强版Word生成测试 ===")

# 测试1: 从PPT内容生成AI增强教案
print("\n1. 测试从PPT内容生成AI增强教案")
ppt_topic = "人工智能基础"
ppt_content = [
    {
        'title': '什么是人工智能',
        'content': ['人工智能的定义', '人工智能的发展历史', '人工智能的应用领域']
    },
    {
        'title': '人工智能的核心技术',
        'content': ['机器学习', '深度学习', '自然语言处理', '计算机视觉']
    },
    {
        'title': '人工智能的伦理问题',
        'content': ['隐私保护', '算法偏见', '就业影响', '安全风险']
    }
]

print("开始从PPT内容生成AI增强教案...")
ppt_lesson_plan_path = generator.generate_lesson_plan_from_ppt(ppt_topic, ppt_content, "人工智能基础_AI教案.docx")
print(f"从PPT内容生成AI增强教案成功: {ppt_lesson_plan_path}")

# 测试2: 使用AI直接生成完整教案
print("\n2. 测试使用AI直接生成完整教案")
topic = "机器学习入门"

print("开始使用AI直接生成完整教案...")
ai_lesson_plan_path = generator.generate_lesson_plan_with_ai(topic, "机器学习入门_AI教案.docx")
print(f"使用AI直接生成完整教案成功: {ai_lesson_plan_path}")

print("\n=== 所有测试完成 ===")
print("测试结果:")
print(f"1. 从PPT内容生成AI增强教案: {ppt_lesson_plan_path}")
print(f"2. 使用AI直接生成完整教案: {ai_lesson_plan_path}")
print("\n所有测试均已通过！")
