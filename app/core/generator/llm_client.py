from app.config import settings
import dashscope

class LLMClient:
    def __init__(self):
        """初始化LLM客户端"""
        # 设置API密钥
        if settings.LLM_PROVIDER == "dashscope":
            dashscope.api_key = settings.LLM_API_KEY
        
        self.provider = settings.LLM_PROVIDER
        self.model_name = settings.LLM_MODEL_NAME
    
    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7):
        """
        使用LLM生成内容
        
        Args:
            prompt: 提示词
            max_tokens: 最大生成token数
            temperature: 生成温度
            
        Returns:
            str: 生成的内容
        """
        try:
            if self.provider == "dashscope":
                return self._generate_dashscope(prompt, max_tokens, temperature)
            else:
                # 其他LLM提供商的实现
                return f"Hello, this is a placeholder response for {self.provider}"
        except Exception as e:
            print(f"LLM生成失败: {str(e)}")
            # 返回默认响应
            return f"生成失败: {str(e)}"
    
    def _generate_dashscope(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7):
        """
        使用DashScope生成内容
        
        Args:
            prompt: 提示词
            max_tokens: 最大生成token数
            temperature: 生成温度
            
        Returns:
            str: 生成的内容
        """
        from dashscope import Generation
        
        response = Generation.call(
            model=self.model_name,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if response.status_code == 200:
            return response.output.text
        else:
            raise Exception(f"DashScope API调用失败: {response.message}")
    
    def generate_ppt_outline(self, topic: str):
        """
        生成PPT大纲
        
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
        
        return self.generate(prompt)

# 测试代码
if __name__ == "__main__":
    client = LLMClient()
    test_prompt = "请简单介绍一下人工智能"
    result = client.generate(test_prompt)
    print("LLM生成结果:", result)
    
    # 测试生成PPT大纲
    test_topic = "人工智能简介"
    outline = client.generate_ppt_outline(test_topic)
    print("PPT大纲生成结果:", outline)
