#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试游戏和动画生成功能
"""

from app.core.generator.game_generator import GameGenerator
from app.core.generator.animation_generator import AnimationGenerator

def test_game_generation():
    """测试游戏生成功能"""
    print("=== 测试游戏生成功能 ===")
    
    generator = GameGenerator()
    
    # 测试问答游戏
    test_topic = "人工智能知识问答"
    test_content = [
        {
            'title': '人工智能诞生于哪一年?',
            'content': ['1956年', '1960年', '1970年', '1980年']
        },
        {
            'title': '以下哪项不是机器学习的类型?',
            'content': ['监督学习', '无监督学习', '强化学习', '手动学习']
        },
        {
            'title': '深度学习属于哪种学习类型?',
            'content': ['监督学习', '无监督学习', '强化学习', '以上都对']
        }
    ]
    
    print("测试问答游戏生成...")
    output_path = generator.generate_game(test_topic, test_content, game_type="quiz")
    print(f"问答游戏生成成功: {output_path}")
    
    # 测试记忆游戏
    test_topic = "AI术语记忆"
    test_content = ["机器学习", "深度学习", "神经网络", "自然语言处理", "计算机视觉", "语音识别"]
    
    print("\n测试记忆游戏生成...")
    output_path2 = generator.generate_game(test_topic, test_content, game_type="memory")
    print(f"记忆游戏生成成功: {output_path2}")
    
    # 测试匹配游戏
    test_topic = "AI概念匹配"
    test_content = [
        {
            'title': '监督学习',
            'content': ['分类', '回归']
        },
        {
            'title': '无监督学习',
            'content': ['聚类', '降维']
        }
    ]
    
    print("\n测试匹配游戏生成...")
    output_path3 = generator.generate_game(test_topic, test_content, game_type="matching")
    print(f"匹配游戏生成成功: {output_path3}")
    
    print("\n游戏生成测试完成！")

def test_animation_generation():
    """测试动画生成功能"""
    print("\n=== 测试动画生成功能 ===")
    
    generator = AnimationGenerator()
    
    # 测试幻灯片动画
    test_topic = "人工智能发展历程"
    test_content = [
        {
            'title': '1956年',
            'content': '人工智能概念诞生'
        },
        {
            'title': '1960-1970年代',
            'content': '早期AI研究与发展'
        },
        {
            'title': '1980-1990年代',
            'content': '专家系统与机器学习兴起'
        },
        {
            'title': '2000年代',
            'content': '大数据与深度学习发展'
        },
        {
            'title': '2010年代至今',
            'content': 'AI技术突破与广泛应用'
        }
    ]
    
    print("测试幻灯片动画生成...")
    output_path = generator.generate_animation(test_topic, test_content, animation_type="slideshow")
    print(f"幻灯片动画生成成功: {output_path}")
    
    # 测试时间线动画
    test_topic = "AI重要事件时间线"
    test_content = [
        {
            'title': '1956年',
            'content': '达特茅斯会议，AI概念正式提出'
        },
        {
            'title': '1969年',
            'content': '第一个专家系统DENDRAL开发成功'
        },
        {
            'title': '1997年',
            'content': 'IBM深蓝战胜国际象棋世界冠军卡斯帕罗夫'
        },
        {
            'title': '2011年',
            'content': 'IBM Watson在Jeopardy!节目中获胜'
        },
        {
            'title': '2016年',
            'content': 'AlphaGo战胜围棋世界冠军李世石'
        }
    ]
    
    print("\n测试时间线动画生成...")
    output_path2 = generator.generate_animation(test_topic, test_content, animation_type="timeline")
    print(f"时间线动画生成成功: {output_path2}")
    
    # 测试交互式动画
    test_topic = "AI技术分类"
    test_content = [
        {
            'title': '机器学习',
            'content': '让计算机从数据中学习的技术',
            'details': ['监督学习', '无监督学习', '强化学习']
        },
        {
            'title': '深度学习',
            'content': '基于神经网络的机器学习方法',
            'details': ['卷积神经网络', '循环神经网络', '生成对抗网络']
        },
        {
            'title': '自然语言处理',
            'content': '让计算机理解和处理人类语言',
            'details': ['文本分类', '情感分析', '机器翻译']
        },
        {
            'title': '计算机视觉',
            'content': '让计算机理解和处理图像和视频',
            'details': ['目标检测', '图像分类', '人脸识别']
        }
    ]
    
    print("\n测试交互式动画生成...")
    output_path3 = generator.generate_animation(test_topic, test_content, animation_type="interactive")
    print(f"交互式动画生成成功: {output_path3}")
    
    print("\n动画生成测试完成！")

if __name__ == "__main__":
    test_game_generation()
    test_animation_generation()
    print("\n所有测试完成！")
