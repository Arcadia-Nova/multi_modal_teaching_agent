import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.generator.ppt_generator import PPTGenerator

# 测试PPT生成器
generator = PPTGenerator()

print("=== 开始PPT生成测试 ===")

# 测试1: 基本生成 - 人工智能主题
print("\n1. 测试基本生成 - 人工智能主题")
test_topic = "人工智能技术发展"
test_content = [
    {
        'title': '人工智能定义',
        'content': ['模拟人类智能的技术', '涵盖多个领域', '不断演进的概念']
    },
    {
        'title': '技术发展阶段',
        'content': ['规则系统', '机器学习', '深度学习', '大语言模型']
    },
    {
        'title': '应用场景',
        'content': ['智能助手', '计算机视觉', '自然语言处理', '自动驾驶']
    },
    {
        'title': '未来趋势',
        'content': ['多模态融合', '自主学习', '伦理与安全', '行业应用深化']
    }
]

print("开始生成PPT...")
output_path = generator.generate_ppt(test_topic, test_content)
print(f"PPT生成成功: {output_path}")

# 测试2: 从大纲生成 - 教育科技主题
print("\n2. 测试从大纲生成 - 教育科技主题")
test_outline = {
    'topic': '教育科技发展趋势',
    'sections': [
        {
            'title': '教育科技概述',
            'content': ['定义与范围', '发展历程', '核心技术']
        },
        {
            'title': '智能教学系统',
            'content': ['自适应学习', '智能评测', '个性化推荐']
        },
        {
            'title': 'VR/AR教育应用',
            'content': ['沉浸式学习', '虚拟实验室', '场景化教学']
        },
        {
            'title': '未来展望',
            'content': ['AI教师助手', '元宇宙教育', '终身学习生态']
        }
    ]
}

print("开始从大纲生成PPT...")
output_path2 = generator.generate_ppt_from_outline(test_outline)
print(f"从大纲生成PPT成功: {output_path2}")

# 测试3: 自定义输出文件名
print("\n3. 测试自定义输出文件名")
custom_topic = "自定义文件名测试"
custom_content = [
    {
        'title': '测试页面1',
        'content': ['测试内容1', '测试内容2']
    }
]

print("开始生成自定义文件名PPT...")
custom_output_path = generator.generate_ppt(custom_topic, custom_content, "custom_test_ppt.pptx")
print(f"自定义文件名PPT生成成功: {custom_output_path}")

# 测试4: 边界情况 - 空内容
print("\n4. 测试边界情况 - 空内容")
empty_topic = "空内容测试"
empty_content = []

print("开始生成空内容PPT...")
empty_output_path = generator.generate_ppt(empty_topic, empty_content)
print(f"空内容PPT生成成功: {empty_output_path}")

# 测试5: 边界情况 - 单页内容
print("\n5. 测试边界情况 - 单页内容")
single_topic = "单页内容测试"
single_content = [
    {
        'title': '唯一页面',
        'content': ['这是唯一的页面内容']
    }
]

print("开始生成单页内容PPT...")
single_output_path = generator.generate_ppt(single_topic, single_content)
print(f"单页内容PPT生成成功: {single_output_path}")

print("\n=== 所有测试完成 ===")
print("测试结果:")
print(f"1. 基本生成: {output_path}")
print(f"2. 大纲生成: {output_path2}")
print(f"3. 自定义文件名: {custom_output_path}")
print(f"4. 空内容: {empty_output_path}")
print(f"5. 单页内容: {single_output_path}")
print("\n所有测试均已通过！")
