from app.config import settings
import dashscope

# app/core/generator/llm_client.py
import json
import asyncio
from typing import List, Dict, Any, Optional, Union, AsyncGenerator
from functools import wraps
import time
import logging

import httpx
from dashscope import Generation
from dashscope.api_entities.dashscope_response import GenerationResponse
from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    大模型统一调用封装（支持阿里Qwen，可通过配置切换其他模型）
    提供同步、异步、流式接口，内置重试和超时控制
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: Optional[str] = None,
            timeout: int = 60,
            max_retries: int = 3,
            retry_delay: float = 1.0,
    ):
        self.api_key = api_key or settings.DASHSCOPE_API_KEY
        self.model = model or "qwen-max"  # 可选: qwen-plus, qwen-turbo, qwen-max
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # 设置dashscope API密钥
        if self.api_key:
            Generation.api_key = self.api_key

        if settings.LLM_PROVIDER == "dashscope":
            dashscope.api_key = settings.LLM_API_KEY

        self.provider = settings.LLM_PROVIDER
        self.model_name = settings.LLM_MODEL_NAME

    def _should_retry(self, response: GenerationResponse) -> bool:
        """判断是否应该重试（基于API返回状态）"""
        if response.status_code == 200:
            return False
        # 可重试的错误码：限流、服务端错误等
        retry_codes = [429, 500, 502, 503, 504]
        return response.status_code in retry_codes

    def _build_messages(self, messages: List[Dict[str, str]]) -> List[Dict]:
        """转换消息格式为DashScope格式"""
        # DashScope要求role为system/user/assistant
        return messages

    def _call_dashscope_sync(self, messages: List[Dict], **kwargs) -> str:
        """同步调用DashScope API，带重试"""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = Generation.call(
                    model=self.model,
                    messages=self._build_messages(messages),
                    result_format="message",
                    **kwargs
                )
                if response.status_code == 200:
                    return response.output.choices[0].message.content
                elif self._should_retry(response):
                    logger.warning(
                        f"API调用失败 (尝试 {attempt + 1}/{self.max_retries}): "
                        f"status={response.status_code}, msg={response.message}"
                    )
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise Exception(f"API错误: {response.status_code} - {response.message}")
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    logger.warning(f"请求异常，重试 {attempt + 1}: {e}")
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise Exception(f"最终失败: {e}") from e
        raise last_exception

    async def _call_dashscope_async(self, messages: List[Dict], **kwargs) -> str:
        """异步调用DashScope API（使用httpx调用HTTP接口）"""
        # DashScope SDK暂不支持原生异步，使用httpx调用其HTTP API
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "input": {
                "messages": self._build_messages(messages)
            },
            "parameters": {
                "result_format": "message",
                **kwargs
            }
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    resp = await client.post(url, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["output"]["choices"][0]["message"]["content"]
                    elif resp.status_code in [429, 500, 502, 503, 504]:
                        await asyncio.sleep(self.retry_delay * (attempt + 1))
                        continue
                    else:
                        raise Exception(f"HTTP {resp.status_code}: {resp.text}")
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
        raise Exception("请求失败")

    def chat(
            self,
            messages: List[Dict[str, str]],
            temperature: float = 0.7,
            max_tokens: Optional[int] = None,
            **kwargs
    ) -> str:
        """
        同步聊天接口

        Args:
            messages: [{"role": "user/system/assistant", "content": "..."}]
            temperature: 温度参数 0-1
            max_tokens: 最大输出token数
        Returns:
            str: 模型回复内容
        """
        params = {
            "temperature": temperature,
            **kwargs
        }
        if max_tokens:
            params["max_tokens"] = max_tokens
        return self._call_dashscope_sync(messages, **params)

    async def achat(
            self,
            messages: List[Dict[str, str]],
            temperature: float = 0.7,
            max_tokens: Optional[int] = None,
            **kwargs
    ) -> str:
        """异步聊天接口"""
        params = {
            "temperature": temperature,
            **kwargs
        }
        if max_tokens:
            params["max_tokens"] = max_tokens
        return await self._call_dashscope_async(messages, **params)

    async def astream(
            self,
            messages: List[Dict[str, str]],
            temperature: float = 0.7,
            max_tokens: Optional[int] = None,
            **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        异步流式生成（使用HTTP流式接口）
        """
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        params = {
            "temperature": temperature,
            "result_format": "message",
            "incremental_output": True,  # 流式输出
            **kwargs
        }
        if max_tokens:
            params["max_tokens"] = max_tokens
        payload = {
            "model": self.model,
            "input": {"messages": self._build_messages(messages)},
            "parameters": params,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise Exception(f"流式请求失败: {response.status_code} - {error_text}")
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["output"]["choices"][0]["message"]["content"]
                            yield delta
                        except Exception as e:
                            logger.error(f"解析流式数据失败: {e}")

    def chat_with_json(
            self,
            messages: List[Dict[str, str]],
            temperature: float = 0.2,
            **kwargs
    ) -> Dict[str, Any]:
        """
        要求模型返回JSON格式（通常temperature设低）
        """
        # 添加JSON输出指示
        messages = messages.copy()
        last_user_msg = messages[-1]["content"] if messages[-1]["role"] == "user" else ""
        messages[-1]["content"] = f"{last_user_msg}\n请直接输出JSON格式，不要有其他文字。"
        response = self.chat(messages, temperature=temperature, **kwargs)
        # 尝试解析JSON
        try:
            # 去除可能的markdown代码块标记
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            return json.loads(response.strip())
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {response[:200]}...")
            raise ValueError(f"模型输出不是有效JSON: {e}")

    async def achat_with_json(
            self,
            messages: List[Dict[str, str]],
            temperature: float = 0.2,
            **kwargs
    ) -> Dict[str, Any]:
        """异步JSON请求"""
        messages = messages.copy()
        last_user_msg = messages[-1]["content"] if messages[-1]["role"] == "user" else ""
        messages[-1]["content"] = f"{last_user_msg}\n请直接输出JSON格式，不要有其他文字。"
        response = await self.achat(messages, temperature=temperature, **kwargs)
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        return json.loads(response.strip())




    # def __init__(self):
    #     """初始化LLM客户端"""
    #     # 设置API密钥
    #     if settings.LLM_PROVIDER == "dashscope":
    #         dashscope.api_key = settings.LLM_API_KEY
    #
    #     self.provider = settings.LLM_PROVIDER
    #     self.model_name = settings.LLM_MODEL_NAME
    
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

# 单例模式，全局复用
_llm_client_instance = None


def get_llm_client() -> LLMClient:
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = LLMClient()
    return _llm_client_instance

# 测试代码
if __name__ == "__main__":
    client = LLMClient()
    test_prompt = "请简单介绍一下中国小学教育包含哪些内容"
    result = client.generate(test_prompt)
    print("LLM生成结果:", result)
    
    # 测试生成PPT大纲
    test_topic = "人工智能简介"
    outline = client.generate_ppt_outline(test_topic)
    print("PPT大纲生成结果:", outline)
