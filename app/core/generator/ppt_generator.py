from pptx import Presentation
from pptx.util import Inches
import os
from app.config import settings

class PPTGenerator:
    def __init__(self):
        """初始化PPT生成器"""
        pass
    
    def generate_ppt(self, topic: str, content: list, output_filename: str = None):
        """
        生成PPT文件
        
        Args:
            topic: PPT主题
            content: PPT内容列表，每个元素包含标题和内容
            output_filename: 输出文件名
            
        Returns:
            str: 生成的PPT文件路径
        """
        # 创建PPT对象
        prs = Presentation()
        
        # 添加标题页
        self._add_title_slide(prs, topic)
        
        # 添加内容页
        for item in content:
            if isinstance(item, dict) and 'title' in item and 'content' in item:
                self._add_content_slide(prs, item['title'], item['content'])
        
        # 生成文件名
        if not output_filename:
            output_filename = f"{topic.replace(' ', '_')}_ppt.pptx"
        
        # 确保输出目录存在
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        # 保存PPT文件
        output_path = os.path.join(settings.EXPORT_DIR, output_filename)
        prs.save(output_path)
        
        return output_path
    
    def _add_title_slide(self, prs, title):
        """添加标题页"""
        slide_layout = prs.slide_layouts[0]  # 标题布局
        slide = prs.slides.add_slide(slide_layout)
        title_placeholder = slide.shapes.title
        title_placeholder.text = title
    
    def _add_content_slide(self, prs, title, content):
        """添加内容页"""
        slide_layout = prs.slide_layouts[1]  # 标题和内容布局
        slide = prs.slides.add_slide(slide_layout)
        
        # 设置标题
        title_placeholder = slide.shapes.title
        title_placeholder.text = title
        
        # 设置内容
        content_placeholder = slide.placeholders[1]
        if isinstance(content, list):
            content_text = '\n'.join(content)
        else:
            content_text = str(content)
        
        content_placeholder.text = content_text
    
    def generate_ppt_from_outline(self, outline: dict, output_filename: str = None):
        """
        从大纲生成PPT
        
        Args:
            outline: PPT大纲，包含主题和章节
            output_filename: 输出文件名
            
        Returns:
            str: 生成的PPT文件路径
        """
        topic = outline.get('topic', 'Untitled')
        sections = outline.get('sections', [])
        
        content = []
        for section in sections:
            section_title = section.get('title', 'Section')
            section_content = section.get('content', [])
            content.append({
                'title': section_title,
                'content': section_content
            })
        
        return self.generate_ppt(topic, content, output_filename)

# 测试代码
if __name__ == "__main__":
    generator = PPTGenerator()
    
    # 测试基本生成
    test_topic = "人工智能简介"
    test_content = [
        {
            'title': '什么是人工智能',
            'content': ['人工智能是模拟人类智能的技术', '包括机器学习、深度学习等分支', '应用于多个领域']
        },
        {
            'title': '人工智能的历史',
            'content': ['1956年诞生', '经历两次寒冬', '近年来快速发展']
        },
        {
            'title': '人工智能的应用',
            'content': ['自动驾驶', '语音识别', '图像识别', '自然语言处理']
        }
    ]
    
    output_path = generator.generate_ppt(test_topic, test_content)
    print(f"PPT生成成功: {output_path}")
    
    # 测试从大纲生成
    test_outline = {
        'topic': '机器学习基础',
        'sections': [
            {
                'title': '机器学习概述',
                'content': ['定义', '类型', '应用场景']
            },
            {
                'title': '监督学习',
                'content': ['分类', '回归', '常见算法']
            },
            {
                'title': '无监督学习',
                'content': ['聚类', '降维', '异常检测']
            }
        ]
    }
    
    output_path2 = generator.generate_ppt_from_outline(test_outline)
    print(f"从大纲生成PPT成功: {output_path2}")
