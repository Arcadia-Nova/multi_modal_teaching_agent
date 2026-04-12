import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.generator.ppt_generator import PPTGenerator

# 测试PPT生成器（AI增强版）
generator = PPTGenerator()

print("=== 开始AI增强版PPT生成测试 ===")

# 测试1: 使用AI从主题生成完整PPT
print("\n1. 测试使用AI从主题生成完整PPT")
topic = "人工智能在教育中的应用"

print("开始使用AI从主题生成完整PPT...")
ai_ppt_path = generator.generate_ppt_with_ai(topic, "人工智能教育应用_AI_PPT.pptx")
print(f"使用AI从主题生成完整PPT成功: {ai_ppt_path}")

# 测试2: 使用AI增强现有PPT内容
print("\n2. 测试使用AI增强现有PPT内容")
existing_topic = "机器学习基础"
existing_content = [
    {
        'title': '机器学习概述',
        'content': ['定义', '类型', '应用场景']
    },
    {
        'title': '监督学习',
        'content': ['分类', '回归', '常见算法']
    },
    {
        'title': '无监督学习',
        'content': ['聚类', '降维', '异常检测']
    }
]

print("开始使用AI增强现有PPT内容...")
enhanced_ppt_path = generator.enhance_ppt_content_with_ai(existing_topic, existing_content, "机器学习基础_增强版.pptx")
print(f"使用AI增强现有PPT内容成功: {enhanced_ppt_path}")

print("\n=== 所有测试完成 ===")
print("测试结果:")
print(f"1. 使用AI从主题生成完整PPT: {ai_ppt_path}")
print(f"2. 使用AI增强现有PPT内容: {enhanced_ppt_path}")
print("\n所有测试均已通过！")
