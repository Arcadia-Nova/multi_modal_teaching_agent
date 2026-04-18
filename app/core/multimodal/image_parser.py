# app/core/multimodal/image_parser.py
import os
os.environ['FLAGS_use_mkldnn'] = '0'

from paddleocr import PaddleOCR
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# 初始化OCR和BLIP模型
oocr = PaddleOCR(use_angle_cls=True, lang='ch')
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def parse_image(image_path: str):
    """
    解析图像内容
    
    Args:
        image_path: 图像路径
        
    Returns:
        dict: 包含OCR文本和图像描述的字典
    """
    try:
        # 使用OCR识别文本
        ocr_results = oocr.ocr(image_path, cls=True)
        ocr_text = ""
        if ocr_results:
            for line in ocr_results[0]:
                ocr_text += line[1][0] + " "
        
        # 使用BLIP生成图像描述
        image = Image.open(image_path).convert('RGB')
        inputs = blip_processor(image, return_tensors="pt")
        out = blip_model.generate(**inputs)
        description = blip_processor.decode(out[0], skip_special_tokens=True)
        
        return {
            "ocr_text": ocr_text.strip(),
            "blip_description": description,
            "summary": f"图像文字: {ocr_text}。图像内容: {description}"
        }
    except Exception as e:
        return {
            "ocr_text": "",
            "blip_description": "",
            "summary": f"图像解析失败: {str(e)}"
        }