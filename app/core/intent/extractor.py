"""
意图提取器
"""
from typing import Dict, Any


class IntentExtractor:
    """
    意图提取器类
    """
    
    def extract_intent(self, user_input: str) -> Dict[str, Any]:
        """
        提取用户意图
        
        Args:
            user_input: 用户输入
            
        Returns:
            Dict[str, Any]: 包含意图信息的字典
        """
        # 简单的意图提取逻辑
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in ['生成', '创建', '制作', '做']):
            if any(keyword in user_input_lower for keyword in ['ppt', '幻灯片']):
                return {
                    'intent': 'generate_ppt',
                    'topic': user_input
                }
            elif any(keyword in user_input_lower for keyword in ['教案', '教学计划', '教学设计']):
                return {
                    'intent': 'generate_lesson_plan',
                    'topic': user_input
                }
            elif any(keyword in user_input_lower for keyword in ['游戏', 'quiz', '记忆', '匹配']):
                return {
                    'intent': 'generate_game',
                    'topic': user_input
                }
        
        # 默认意图
        return {
            'intent': 'unknown',
            'topic': user_input
        }
