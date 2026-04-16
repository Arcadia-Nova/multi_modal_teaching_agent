import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.generator.ppt_generator import PPTGenerator

# 测试PPT生成功能
def test_ppt_generator():
    generator = PPTGenerator()
    
    # 测试1: 直接使用AI生成PPT（包含知识点和详细解释）
    print("测试1: 使用AI生成包含知识点和详细解释的PPT")
    test_topic = "人工智能教育"
    output_path1 = generator.generate_ppt_with_ai(test_topic)
    print(f"AI生成PPT成功: {output_path1}")
    
    # 测试2: 从教案生成PPT（包含知识点和详细解释）
    print("\n测试2: 从教案生成包含知识点和详细解释的PPT")
    test_lesson_plan = {
        'teaching_objectives': [
            '了解人工智能的基本概念',
            '掌握人工智能的核心技术',
            '理解人工智能的应用场景'
        ],
        'teaching_process': [
            {
                'title': '导入环节',
                'content': ['人工智能的定义', '人工智能的发展历程', '人工智能的重要性'],
                'duration': '10分钟'
            },
            {
                'title': '讲解环节',
                'content': ['机器学习', '深度学习', '神经网络'],
                'duration': '30分钟'
            },
            {
                'title': '讨论环节',
                'content': ['人工智能的优势', '人工智能的挑战', '人工智能的未来'],
                'duration': '20分钟'
            }
        ],
        'classroom_activities': [
            {
                'title': '小组讨论',
                'description': '讨论人工智能在教育中的应用',
                'duration': '15分钟'
            },
            {
                'title': '案例分析',
                'description': '分析人工智能在医疗领域的应用案例',
                'duration': '15分钟'
            }
        ],
        'homework': [
            '完成人工智能概念的总结',
            '查找人工智能在生活中的应用实例',
            '思考人工智能对未来社会的影响'
        ]
    }
    
    output_path2 = generator.generate_ppt_from_lesson_plan(test_topic, test_lesson_plan)
    print(f"从教案生成PPT成功: {output_path2}")
    
    print("\nPPT生成测试完成！")

if __name__ == "__main__":
    test_ppt_generator()
