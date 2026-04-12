import asyncio
import os
from typing import List, Dict

from app.core.generator import llm_client
# 假设上面的 LLMClient 代码保存在 llm_client.py 中
from app.core.generator.llm_client import LLMClient
print("LLMClient 文件的真实路径是：", llm_client.__file__) # 这会告诉你 Python 实际加载的是哪个文件

# 如果没有使用 settings 模块，可以直接传入环境变量
# os.environ["DASHSCOPE_API_KEY"] = "sk-你的key"

def test_sync():
    print("=== 同步调用测试 ===")
    client = LLMClient()
    messages = [
        {"role": "user", "content": "你好，请用一句话介绍你自己"}
    ]
    response = client.chat(messages)
    print(response)


async def test_async():
    print("\n=== 异步调用测试 ===")
    client = LLMClient()
    messages = [
        {"role": "user", "content": "你好，请用一句话介绍异步调用的优势"}
    ]
    response = await client.achat(messages)
    print(response)


async def test_stream():
    print("\n=== 流式输出测试 (像打字机一样) ===")
    client = LLMClient()
    messages = [
        {"role": "user", "content": "请列举三个中国著名的旅游景点"}
    ]
    # 流式输出需要逐块接收
    async for chunk in client.astream(messages):
        print(chunk, end="", flush=True)
    print()  # 换行


async def test_json():
    print("\n=== JSON 格式输出测试 ===")
    client = LLMClient()
    messages = [
        {"role": "user", "content": "请列出三个水果及其颜色，要求输出JSON格式"}
    ]
    try:
        data = await client.achat_with_json(messages)
        print(data)
    except Exception as e:
        print("JSON解析失败:", e)


if __name__ == "__main__":
    # 运行同步测试
    test_sync()

    # 运行异步测试
    asyncio.run(test_async())
    asyncio.run(test_stream())
    asyncio.run(test_json())