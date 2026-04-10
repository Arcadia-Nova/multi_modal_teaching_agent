from app.core.generator.ppt_generator import PPTGenerator

# 测试PPT生成器
generator = PPTGenerator()

# 测试基本生成
test_topic = "人工智能简介"
test_content = [
    {
        'title': '什么是人工智能',
        'content': ['人工智能是模拟人类智能的技术', '包括机器学习、深度学习等分支', '应用于多个领域']
    },
    {
        'title': '人工智能的历史',
        'content': ['1956年诞生', '经历两次寒冬', '近年来快速发展']
    },
    {
        'title': '人工智能的应用',
        'content': ['自动驾驶', '语音识别', '图像识别', '自然语言处理']
    }
]

print("开始生成PPT...")
output_path = generator.generate_ppt(test_topic, test_content)
print(f"PPT生成成功: {output_path}")

# 测试从大纲生成
test_outline = {
    'topic': '机器学习基础',
    'sections': [
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
}

print("\n开始从大纲生成PPT...")
output_path2 = generator.generate_ppt_from_outline(test_outline)
print(f"从大纲生成PPT成功: {output_path2}")
print("测试完成!")
