"""
意图澄清器
"""
from typing import Dict, Any


class Clarifier:
    """
    意图澄清器类
    """
    
    def clarify_intent(self, intent: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """
        澄清用户意图
        
        Args:
            intent: 提取的意图
            user_input: 用户输入
            
        Returns:
            Dict[str, Any]: 澄清后的意图信息
        """
        # 简单的意图澄清逻辑
        if intent['intent'] == 'unknown':
            # 尝试进一步分析未知意图
            user_input_lower = user_input.lower()
            if any(keyword in user_input_lower for keyword in ['帮助', '指导', '使用']):
                return {
                    'intent': 'help',
                    'topic': user_input
                }
            elif any(keyword in user_input_lower for keyword in ['关于', '介绍', '说明']):
                return {
                    'intent': 'about',
                    'topic': user_input
                }
        
        return intent
