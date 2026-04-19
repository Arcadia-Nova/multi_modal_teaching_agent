# app/core/multimodal/voice_transcriber.py
import os

import dashscope
from dashscope.audio.asr import Transcription
from dashscope.utils.oss_utils import OssUtils

from app.config import settings

class VoiceTranscriber:
    def __init__(self):
        # 从配置中读取你的API Key
        dashscope.api_key = settings.DASHSCOPE_API_KEY
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
        self.model = "qwen3-asr-flash"  # 也可以使用 "qwen3-asr-realtime" 等模型

    async def transcribe(self, audio_file_path: str) -> str:
        """
        使用Qwen3-ASR-Flash模型将音频文件转为文字。
        使用官方SDK自动上传文件并获取临时URL。
        """
        try:
            print(audio_file_path)
            # 1. 使用官方SDK上传文件，获取临时URL（OSS格式）
            temp_url = OssUtils.upload(
                file_path=audio_file_path,
                model=self.model,
                api_key=settings.DASHSCOPE_API_KEY
            )
            print(temp_url)

            messages = [
                {"role": "user",
                 "content": [{"audio": temp_url}]},
            ]
            # 2. 调用语音识别API
            response = dashscope.MultiModalConversation.call(
                # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
                api_key=settings.DASHSCOPE_API_KEY,
                # 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
                model="qwen3-asr-flash",
                messages=messages,
                result_format="message",
                asr_options={
                    # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
                    "language": "zh",
                    "enable_itn": False
                },
                headers={'X-DashScope-OssResourceResolve': 'enable'}
            )
            # 3. 处理结果
            if response.status_code == 200:
                print(response)
                return response.output['choices'][0]['message']['content'][0]['text']
            else:
                error_msg = f"Qwen3-ASR API调用失败: {response.message}"
                print(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"语音识别失败: {str(e)}")