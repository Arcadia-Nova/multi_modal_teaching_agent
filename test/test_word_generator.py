import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.generator.word_generator import WordGenerator

# 测试Word生成器
generator = WordGenerator()

print("=== 开始Word生成测试 ===")

# 测试1: 基本Word文档生成
print("\n1. 测试基本Word文档生成")
test_topic = "人工智能技术概述"
test_content = [
    {
        'title': '人工智能定义',
        'content': ['人工智能是模拟人类智能的技术', '包括机器学习、深度学习等分支', '应用于多个领域']
    },
    {
        'title': '人工智能的历史',
        'content': ['1956年诞生', '经历两次寒冬', '近年来快速发展']
    }
]

print("开始生成Word文档...")
output_path = generator.generate_word(test_topic, test_content)
print(f"Word文档生成成功: {output_path}")

# 测试2: 教案生成
print("\n2. 测试教案生成")
lesson_topic = "人工智能基础"
teaching_objectives = [
    "了解人工智能的基本概念和发展历程",
    "掌握人工智能的核心技术和应用场景",
    "培养学生对人工智能的兴趣和创新思维"
]

teaching_process = [
    {
        'title': '导入环节',
        'content': ['通过案例引入人工智能概念', '讨论生活中的人工智能应用'],
        'duration': '5分钟'
    },
    {
        'title': '理论讲解',
        'content': ['人工智能的定义和发展历史', '人工智能的核心技术', '人工智能的应用领域'],
        'duration': '20分钟'
    },
    {
        'title': '互动讨论',
        'content': ['分组讨论人工智能的利弊', '探讨人工智能的未来发展'],
        'duration': '15分钟'
    },
    {
        'title': '总结归纳',
        'content': ['回顾本节课的重点内容', '布置课后作业'],
        'duration': '5分钟'
    }
]

teaching_methods = [
    "讲授法",
    "讨论法",
    "案例分析法",
    "互动问答"
]

classroom_activities = [
    {
        'title': '小组讨论',
        'description': '分组讨论人工智能在日常生活中的应用案例',
        'materials': ['白板', '马克笔'],
        'duration': '15分钟'
    },
    {
        'title': '知识问答',
        'description': '基于PPT内容进行互动问答，巩固所学知识',
        'materials': ['PPT'],
        'duration': '10分钟'
    }
]

homework = [
    "完成课后习题，巩固所学知识",
    "查找人工智能的最新发展动态，撰写一篇小论文",
    "思考人工智能对未来社会的影响"
]

print("开始生成教案...")
lesson_plan_path = generator.generate_lesson_plan(
    lesson_topic, teaching_objectives, teaching_process, 
    teaching_methods, classroom_activities, homework
)
print(f"教案生成成功: {lesson_plan_path}")

# 测试3: 从PPT内容生成配套教案
print("\n3. 测试从PPT内容生成配套教案")
ppt_topic = "机器学习基础"
ppt_content = [
    {
        'title': '什么是机器学习',
        'content': ['机器学习的定义', '机器学习的类型', '机器学习的应用']
    },
    {
        'title': '监督学习',
        'content': ['分类问题', '回归问题', '常见算法']
    },
    {
        'title': '无监督学习',
        'content': ['聚类分析', '降维技术', '异常检测']
    }
]

print("开始从PPT内容生成教案...")
ppt_lesson_plan_path = generator.generate_lesson_plan_from_ppt(ppt_topic, ppt_content)
print(f"从PPT内容生成教案成功: {ppt_lesson_plan_path}")

print("\n=== 所有测试完成 ===")
print("测试结果:")
print(f"1. 基本Word文档生成: {output_path}")
print(f"2. 教案生成: {lesson_plan_path}")
print(f"3. 从PPT内容生成教案: {ppt_lesson_plan_path}")
print("\n所有测试均已通过！")
