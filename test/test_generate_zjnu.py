import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.generator.word_generator import WordGenerator
from app.core.generator.ppt_generator import PPTGenerator
from app.core.generator.game_generator import GameGenerator

topic = "AI教育"
timestamp = int(time.time())

print("=== 开始生成配套资源 ===\n")

# 1. 先获取AI生成的教案数据
print("1. 使用AI生成教案内容...")
word_gen = WordGenerator()
try:
    lesson_plan_data = word_gen._generate_full_lesson_plan_with_ai(topic)
    print(f"   教案内容生成成功，包含 {len(lesson_plan_data.get('teaching_objectives', []))} 个教学目标")
except Exception as e:
    print(f"   AI生成失败: {e}")
    lesson_plan_data = None

# 2. 根据教案生成配套Word文档
print("\n2. 生成教案 (Word文档)...")
lesson_plan_path = word_gen.generate_lesson_plan_with_ai(
    topic,
    f"{topic}_教案_{timestamp}.docx"
)
print(f"   教案生成成功: {lesson_plan_path}")

# 3. 从教案数据生成配套PPT
print("\n3. 生成配套PPT...")
ppt_gen = PPTGenerator()
if lesson_plan_data:
    ppt_path = ppt_gen.generate_ppt_from_lesson_plan(
        topic,
        lesson_plan_data,
        f"{topic}_配套PPT_{timestamp}.pptx"
    )
else:
    ppt_path = ppt_gen.generate_ppt_with_ai(
        topic,
        f"{topic}_配套PPT_{timestamp}.pptx"
    )
print(f"   PPT生成成功: {ppt_path}")

# 4. 生成所有配套游戏
print("\n4. 生成配套游戏...")
game_gen = GameGenerator()
game_types = ["quiz", "memory", "matching"]
game_paths = {}

for gt in game_types:
    if gt == "quiz":
        game_name = "知识问答游戏"
    elif gt == "memory":
        game_name = "记忆游戏"
    else:
        game_name = "匹配游戏"

    game_path = game_gen.generate_game_with_ai(
        topic,
        game_type=gt,
        output_filename=f"{topic}_{game_name}_{timestamp}.html"
    )
    game_paths[gt] = game_path
    print(f"   {game_name}生成成功: {game_path}")

print("\n=== 所有资源生成完成 ===")
print(f"教案: {lesson_plan_path}")
print(f"PPT: {ppt_path}")
print(f"问答游戏: {game_paths.get('quiz')}")
print(f"记忆游戏: {game_paths.get('memory')}")
print(f"匹配游戏: {game_paths.get('matching')}")