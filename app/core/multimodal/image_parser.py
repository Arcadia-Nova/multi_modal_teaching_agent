# app/core/multimodal/image_parser.py
import os
os.environ['FLAGS_use_mkldnn'] = '0'

from paddleocr import PaddleOCR
from PIL import Image

# 初始化OCR模型
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 尝试初始化BLIP模型
try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
    BLIP_AVAILABLE = True
except Exception as e:
    print(f"BLIP模型加载失败: {e}，将使用简化模式")
    BLIP_AVAILABLE = False


def parse_image(image_path: str) -> dict:
    try:
        # 1. OCR文字识别
        ocr_result = ocr.ocr(image_path)
        ocr_text = " ".join([line[1][0] for line in ocr_result[0]]) if ocr_result else ""

        # 2. BLIP图像描述（如果模型可用）
        description = ""
        if BLIP_AVAILABLE:
            try:
                image = Image.open(image_path).convert('RGB')
                inputs = blip_processor(image, return_tensors="pt").to(device)
                out = blip_model.generate(**inputs, max_new_tokens=200)
                description = blip_processor.decode(out[0], skip_special_tokens=True)
            except Exception as e:
                description = f"图像描述生成失败: {str(e)}"
        else:
            description = "BLIP模型不可用"

        return {
            "ocr_text": ocr_text,
            "blip_description": description,
            "summary": f"图像文字: {ocr_text}。图像内容: {description}"
        }
    except Exception as e:
        return {
            "ocr_text": "",
            "blip_description": "",
            "summary": f"图像解析失败: {str(e)}"
        }