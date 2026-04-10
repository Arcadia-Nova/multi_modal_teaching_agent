from app.core.generator.llm_client import get_llm_client

client = get_llm_client()
messages = [
    {"role": "system", "content": "你是教学助手"},
    {"role": "user", "content": "欧姆定律是什么？"}
]
reply = client.chat(messages, temperature=0.5)
print(reply)