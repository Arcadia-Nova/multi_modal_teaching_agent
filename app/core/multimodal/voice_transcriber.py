# app/core/multimodal/voice_transcriber.py
import dashscope
from dashscope.audio.asr import Transcription
from app.config import settings

class VoiceTranscriber:
    def __init__(self):
        # 从配置中读取你的API Key
        dashscope.api_key = settings.DASHSCOPE_API_KEY
        self.model = "qwen3-asr-flash"  # 也可以使用 "qwen3-asr-realtime" 等模型

    async def transcribe(self, audio_file_path: str) -> str:
        """
        使用Qwen3-ASR-Flash模型将音频文件转为文字。
        注意：此API有3分钟/10MB的音频文件限制。
        """
        # 调用DashScope的语音识别API
        transcription = Transcription.call(
            model=self.model,
            file_urls=[audio_file_path],  # 支持本地文件路径或可访问的URL
        )

        # 检查调用是否成功
        if transcription.status_code == 200:
            # 提取识别结果
            text = transcription.output['text']
            return text
        else:
            # 处理错误情况
            error_msg = f"Qwen3-ASR API调用失败: {transcription.message}"
            print(error_msg)
            raise Exception(error_msg)