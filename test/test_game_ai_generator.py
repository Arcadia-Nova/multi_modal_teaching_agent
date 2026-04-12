import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.generator.game_generator import GameGenerator

# 测试游戏生成器（AI增强版）
generator = GameGenerator()

print("=== 开始AI增强版游戏生成测试 ===")

# 测试1: 使用AI从主题生成问答游戏
print("\n1. 测试使用AI从主题生成问答游戏")
topic = "人工智能知识"

print("开始使用AI从主题生成问答游戏...")
ai_quiz_path = generator.generate_game_with_ai(topic, game_type="quiz", output_filename="人工智能知识问答_AI游戏.html")
print(f"使用AI从主题生成问答游戏成功: {ai_quiz_path}")

# 测试2: 使用AI从主题生成记忆游戏
print("\n2. 测试使用AI从主题生成记忆游戏")
topic = "AI术语"

print("开始使用AI从主题生成记忆游戏...")
ai_memory_path = generator.generate_game_with_ai(topic, game_type="memory", output_filename="AI术语记忆_AI游戏.html")
print(f"使用AI从主题生成记忆游戏成功: {ai_memory_path}")

# 测试3: 使用AI从主题生成匹配游戏
print("\n3. 测试使用AI从主题生成匹配游戏")
topic = "AI概念匹配"

print("开始使用AI从主题生成匹配游戏...")
ai_matching_path = generator.generate_game_with_ai(topic, game_type="matching", output_filename="AI概念匹配_AI游戏.html")
print(f"使用AI从主题生成匹配游戏成功: {ai_matching_path}")

# 测试4: 使用AI增强现有游戏内容
print("\n4. 测试使用AI增强现有游戏内容")
existing_topic = "机器学习"
existing_content = [
    {
        'title': '机器学习的定义是什么?',
        'content': ['让计算机从数据中学习的技术', '人工编程的规则系统', '基于规则的专家系统', '传统的统计方法']
    },
    {
        'title': '以下哪项不是机器学习的类型?',
        'content': ['监督学习', '无监督学习', '强化学习', '手动学习']
    }
]

print("开始使用AI增强现有游戏内容...")
enhanced_quiz_path = generator.enhance_game_content_with_ai(existing_topic, existing_content, game_type="quiz", output_filename="机器学习问答_增强版.html")
print(f"使用AI增强现有游戏内容成功: {enhanced_quiz_path}")

print("\n=== 所有测试完成 ===")
print("测试结果:")
print(f"1. 使用AI从主题生成问答游戏: {ai_quiz_path}")
print(f"2. 使用AI从主题生成记忆游戏: {ai_memory_path}")
print(f"3. 使用AI从主题生成匹配游戏: {ai_matching_path}")
print(f"4. 使用AI增强现有游戏内容: {enhanced_quiz_path}")
print("\n所有测试均已通过！")
