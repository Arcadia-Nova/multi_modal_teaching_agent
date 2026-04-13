from app.core.generator.ppt_generator import PPTGenerator
from app.core.generator.word_generator import WordGenerator
from app.core.generator.animation_generator import AnimationGenerator
from app.core.generator.game_generator import GameGenerator
from app.core.generator.llm_client import LLMClient
import json

class GenerationService:
    def __init__(self):
        """初始化生成服务"""
        self.ppt_generator = PPTGenerator()
        self.word_generator = WordGenerator()
        self.animation_generator = AnimationGenerator()
        self.game_generator = GameGenerator()
        self.llm_client = LLMClient()
    
    def generate_ppt(self, topic: str, content: list = None, outline: dict = None, output_filename: str = None):
        """
        生成PPT
        
        Args:
            topic: PPT主题
            content: PPT内容列表
            outline: PPT大纲
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 如果没有提供内容或大纲，使用LLM生成
            if not content and not outline:
                outline = self._generate_ppt_outline(topic)
            
            # 根据提供的参数生成PPT
            if outline:
                output_path = self.ppt_generator.generate_ppt_from_outline(outline, output_filename)
            elif content:
                output_path = self.ppt_generator.generate_ppt(topic, content, output_filename)
            else:
                raise ValueError("请提供内容或大纲")
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "PPT生成成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"PPT生成失败: {str(e)}",
                "data": None
            }
    
    def _generate_ppt_outline(self, topic: str):
        """
        使用LLM生成PPT大纲
        
        Args:
            topic: PPT主题
            
        Returns:
            dict: PPT大纲
        """
        prompt = f"请为'{topic}'主题生成一个PPT大纲，包含以下结构：\n"
        prompt += "{\n"
        prompt += "  \"topic\": \"主题名称\",\n"
        prompt += "  \"sections\": [\n"
        prompt += "    {\n"
        prompt += "      \"title\": \"章节标题\",\n"
        prompt += "      \"content\": [\"要点1\", \"要点2\", \"要点3\"]\n"
        prompt += "    }\n"
        prompt += "  ]\n"
        prompt += "}\n"
        prompt += "请确保大纲结构完整，内容合理，至少包含3个章节。"
        
        response = self.llm_client.generate(prompt)
        
        # 解析LLM返回的JSON
        try:
            outline = json.loads(response)
            return outline
        except json.JSONDecodeError:
            # 如果解析失败，返回默认大纲
            return {
                "topic": topic,
                "sections": [
                    {
                        "title": "介绍",
                        "content": [f"{topic}的基本概念", "为什么重要", "本PPT的内容概览"]
                    },
                    {
                        "title": "核心内容",
                        "content": ["主要知识点1", "主要知识点2", "主要知识点3"]
                    },
                    {
                        "title": "总结",
                        "content": ["关键要点回顾", "应用场景", "未来发展"]
                    }
                ]
            }
    
    def generate_word(self, topic: str, content: list = None, output_filename: str = None):
        """
        生成Word文档
        
        Args:
            topic: 文档主题
            content: 文档内容
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用Word生成器
            output_path = self.word_generator.generate_word(topic, content, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "Word生成成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Word生成失败: {str(e)}",
                "data": None
            }
    
    def generate_animation(self, topic: str, content: list = None, output_filename: str = None):
        """
        生成动画
        
        Args:
            topic: 动画主题
            content: 动画内容
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 这里可以添加动画生成逻辑
            return {
                "success": True,
                "message": "动画生成功能开发中",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"动画生成失败: {str(e)}",
                "data": None
            }
    
    def generate_game(self, topic: str, content: list = None, game_type: str = "quiz", output_filename: str = None):
        """
        生成游戏
        
        Args:
            topic: 游戏主题
            content: 游戏内容
            game_type: 游戏类型 (quiz, memory, matching)
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用游戏生成器
            output_path = self.game_generator.generate_game(topic, content, game_type, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "游戏生成成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"游戏生成失败: {str(e)}",
                "data": None
            }
    
    def generate_ppt_with_ai(self, topic: str, output_filename: str = None):
        """
        使用AI生成PPT
        
        Args:
            topic: PPT主题
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用AI增强的PPT生成器
            output_path = self.ppt_generator.generate_ppt_with_ai(topic, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "AI生成PPT成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"AI生成PPT失败: {str(e)}",
                "data": None
            }
    
    def enhance_ppt_with_ai(self, topic: str, content: list, output_filename: str = None):
        """
        使用AI增强PPT内容
        
        Args:
            topic: PPT主题
            content: PPT内容
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用AI增强的PPT生成器
            output_path = self.ppt_generator.enhance_ppt_content_with_ai(topic, content, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "AI增强PPT成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"AI增强PPT失败: {str(e)}",
                "data": None
            }
    
    def generate_lesson_plan_with_ai(self, topic: str, output_filename: str = None):
        """
        使用AI生成教案
        
        Args:
            topic: 教案主题
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用AI增强的Word生成器
            output_path = self.word_generator.generate_lesson_plan_with_ai(topic, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "AI生成教案成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"AI生成教案失败: {str(e)}",
                "data": None
            }
    
    def generate_lesson_plan_from_ppt_with_ai(self, topic: str, ppt_content: list, output_filename: str = None):
        """
        从PPT内容生成AI增强教案
        
        Args:
            topic: 教案主题
            ppt_content: PPT内容
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用AI增强的Word生成器
            output_path = self.word_generator.generate_lesson_plan_from_ppt(topic, ppt_content, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "AI生成教案成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"AI生成教案失败: {str(e)}",
                "data": None
            }
    
    def generate_game_with_ai(self, topic: str, game_type: str = "quiz", output_filename: str = None):
        """
        使用AI生成游戏
        
        Args:
            topic: 游戏主题
            game_type: 游戏类型 (quiz, memory, matching)
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用AI增强的游戏生成器
            output_path = self.game_generator.generate_game_with_ai(topic, game_type, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "AI生成游戏成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"AI生成游戏失败: {str(e)}",
                "data": None
            }
    
    def enhance_game_with_ai(self, topic: str, content: list, game_type: str = "quiz", output_filename: str = None):
        """
        使用AI增强游戏内容
        
        Args:
            topic: 游戏主题
            content: 游戏内容
            game_type: 游戏类型
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        try:
            # 调用AI增强的游戏生成器
            output_path = self.game_generator.enhance_game_content_with_ai(topic, content, game_type, output_filename)
            
            # 生成可访问的URL
            relative_path = output_path.replace('app\\static\\', '')
            access_url = f"/static/{relative_path}"
            
            return {
                "success": True,
                "message": "AI增强游戏成功",
                "data": {
                    "file_path": output_path,
                    "access_url": access_url
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"AI增强游戏失败: {str(e)}",
                "data": None
            }
    
    def generate_courseware(self, topic: str, type: str, content: list = None, outline: dict = None, output_filename: str = None):
        """
        生成课件
        
        Args:
            topic: 课件主题
            type: 课件类型 (ppt, word, animation, game)
            content: 课件内容
            outline: 课件大纲
            output_filename: 输出文件名
            
        Returns:
            dict: 包含生成结果的字典
        """
        if type == "ppt":
            return self.generate_ppt(topic, content, outline, output_filename)
        elif type == "word":
            return self.generate_word(topic, content, output_filename)
        elif type == "animation":
            return self.generate_animation(topic, content, output_filename)
        elif type == "game":
            return self.generate_game(topic, content, "quiz", output_filename)
        else:
            return {
                "success": False,
                "message": "不支持的课件类型",
                "data": None
            }

# 测试代码
if __name__ == "__main__":
    service = GenerationService()
    
    # 测试PPT生成
    test_topic = "人工智能简介"
    result = service.generate_ppt(test_topic)
    print("PPT生成结果:", result)
    
    # 测试带内容的PPT生成
    test_content = [
        {
            'title': '什么是人工智能',
            'content': ['人工智能是模拟人类智能的技术', '包括机器学习、深度学习等分支', '应用于多个领域']
        },
        {
            'title': '人工智能的历史',
            'content': ['1956年诞生', '经历两次寒冬', '近年来快速发展']
        }
    ]
    result2 = service.generate_ppt(test_topic, content=test_content)
    print("带内容的PPT生成结果:", result2)
