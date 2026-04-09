# app/core/multimodal/image_parser.py
from paddleocr import PaddleOCR
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# 初始化OCR模型
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 初始化BLIP模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)


def parse_image(image_path: str) -> dict:
    # 1. OCR文字识别
    ocr_result = ocr.ocr(image_path, cls=True)
    ocr_text = " ".join([line[1][0] for line in ocr_result[0]])

    # 2. BLIP图像描述
    image = Image.open(image_path).convert('RGB')
    inputs = blip_processor(image, return_tensors="pt").to(device)
    out = blip_model.generate(**inputs)
    description = blip_processor.decode(out[0], skip_special_tokens=True)

    return {
        "ocr_text": ocr_text,
        "blip_description": description,
        "summary": f"图像文字: {ocr_text}。图像内容: {description}"
    }