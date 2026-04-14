from pptx import Presentation
from pptx.util import Inches
import os
from app.config import settings
from app.core.generator.llm_client import get_llm_client
from app.core.generator.ppt_template_manager import template_manager

class PPTGenerator:
    def __init__(self):
        """初始化PPT生成器"""
        self.llm_client = get_llm_client()
        self.template_manager = template_manager
    
    def generate_ppt(self, topic: str, content: list, output_filename: str = None, template_id: str = None):
        """
        生成PPT文件
        
        Args:
            topic: PPT主题
            content: PPT内容列表，每个元素包含标题和内容
            output_filename: 输出文件名
            template_id: 模板ID
            
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
        
        # 应用模板
        if template_id:
            prs = self.template_manager.apply_template(prs, template_id)
        
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
        slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(slide_layout)
        title_placeholder = slide.shapes.title
        title_placeholder.text = title
    
    def _add_content_slide(self, prs, title, content):
        """添加内容页"""
        slide_layout = prs.slide_layouts[1]
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
    
    def generate_ppt_from_outline(self, outline: dict, output_filename: str = None, template_id: str = None):
        """
        从大纲生成PPT
        
        Args:
            outline: PPT大纲，包含主题和章节
            output_filename: 输出文件名
            template_id: 模板ID
            
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
        
        return self.generate_ppt(topic, content, output_filename, template_id)
    
    def generate_ppt_with_ai(self, topic: str, output_filename: str = None, template_id: str = None):
        """
        使用AI生成完整PPT
        
        Args:
            topic: PPT主题
            output_filename: 输出文件名
            template_id: 模板ID
            
        Returns:
            str: 生成的PPT文件路径
        """
        # 使用AI生成PPT大纲
        outline = self._generate_ppt_outline_with_ai(topic, None)
        # 从大纲生成PPT
        return self.generate_ppt_from_outline(outline, output_filename, template_id)
    
    def enhance_ppt_content_with_ai(self, topic: str, content: list, output_filename: str = None, template_id: str = None):
        """
        使用AI增强PPT内容
        
        Args:
            topic: PPT主题
            content: PPT内容列表
            output_filename: 输出文件名
            template_id: 模板ID
            
        Returns:
            str: 生成的PPT文件路径
        """
        # 使用AI增强每个幻灯片的内容
        enhanced_content = []
        for slide in content:
            slide_title = slide.get('title', '无标题')
            slide_content = slide.get('content', [])
            
            # 使用AI增强内容
            enhanced_slide_content = self._enhance_slide_content_with_ai(topic, slide_title, slide_content)
            
            enhanced_content.append({
                'title': slide_title,
                'content': enhanced_slide_content
            })
        
        # 生成PPT
        return self.generate_ppt(topic, enhanced_content, output_filename, template_id)
    
    def generate_ppt_from_template(self, template_path: str, topic: str, content: list = None, output_filename: str = None):
        """
        从外部模板文件生成PPT
        严格沿用模板的版式、字体、配色、排版样式和母版格式
        只保留模板框架和美化，替换所有文字内容
        
        Args:
            template_path: 模板文件路径
            topic: PPT主题
            content: PPT内容列表（可选）
            output_filename: 输出文件名
            
        Returns:
            str: 生成的PPT文件路径
        """
        # 从模板创建PPT
        prs = Presentation(template_path)
        
        # 保留第一页作为标题页，删除其他所有幻灯片
        # 注意：需要从后往前删除，避免索引问题
        for i in range(len(prs.slides) - 1, 0, -1):
            rId = prs.slides._sldIdLst[i].rId
            prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[1:]
        
        # 更新标题页
        if prs.slides:
            title_slide = prs.slides[0]
            title_shape = title_slide.shapes.title
            if title_shape:
                title_shape.text = topic
        
        # 如果提供了内容，添加新的幻灯片
        if content:
            # 直接添加新的内容幻灯片，使用模板的布局
            for item in content:
                if isinstance(item, dict) and 'title' in item and 'content' in item:
                    # 确保使用模板的布局
                    if len(prs.slide_layouts) > 1:
                        slide_layout = prs.slide_layouts[1]  # 使用模板的内容布局
                        slide = prs.slides.add_slide(slide_layout)
                        
                        # 设置标题
                        title_placeholder = slide.shapes.title
                        if title_placeholder:
                            title_placeholder.text = item['title']
                        
                        # 设置内容
                        content_placeholder = None
                        for placeholder in slide.placeholders:
                            if placeholder.placeholder_format.idx == 1:  # 内容占位符
                                content_placeholder = placeholder
                                break
                        
                        if content_placeholder:
                            if isinstance(item['content'], list):
                                content_text = '\n'.join(item['content'])
                            else:
                                content_text = str(item['content'])
                            content_placeholder.text = content_text
        
        # 生成文件名
        if not output_filename:
            output_filename = f"{topic.replace(' ', '_')}_ppt.pptx"
        
        # 确保输出目录存在
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        # 保存PPT文件
        output_path = os.path.join(settings.EXPORT_DIR, output_filename)
        prs.save(output_path)
        
        return output_path
    
    def generate_ppt_with_ai_from_template(self, template_path: str, topic: str, content_requirement: str = None, output_filename: str = None):
        """
        使用AI生成内容并从模板文件生成PPT
        严格沿用模板的版式、字体、配色、排版样式和母版格式
        
        Args:
            template_path: 模板文件路径
            topic: PPT主题
            content_requirement: 用户的内容需求（可选）
            output_filename: 输出文件名
            
        Returns:
            str: 生成的PPT文件路径
        """
        # 使用AI生成内容
        outline = self._generate_ppt_outline_with_ai(topic, content_requirement)
        
        # 提取内容
        content = []
        for section in outline.get('sections', []):
            content.append({
                'title': section.get('title', '无标题'),
                'content': section.get('content', [])
            })
        
        # 使用模板生成PPT
        return self.generate_ppt_from_template(template_path, topic, content, output_filename)
    
    def generate_enhanced_ppt_with_ai_from_template(self, template_path: str, topic: str, content_requirement: str = None, output_filename: str = None):
        """
        使用AI生成并增强内容，从模板文件生成PPT
        严格沿用模板的版式、字体、配色、排版样式和母版格式
        只生成一个包含AI增强内容的PPT文件
        
        Args:
            template_path: 模板文件路径
            topic: PPT主题
            content_requirement: 用户的内容需求（可选）
            output_filename: 输出文件名
            
        Returns:
            str: 生成的PPT文件路径
        """
        # 使用AI生成内容
        outline = self._generate_ppt_outline_with_ai(topic, content_requirement)
        
        # 提取内容
        content = []
        for section in outline.get('sections', []):
            content.append({
                'title': section.get('title', '无标题'),
                'content': section.get('content', [])
            })
        
        # 使用AI增强内容
        enhanced_content = []
        for slide in content:
            slide_title = slide.get('title', '无标题')
            slide_content = slide.get('content', [])
            
            # 使用AI增强内容
            enhanced_slide_content = self._enhance_slide_content_with_ai(topic, slide_title, slide_content)
            
            enhanced_content.append({
                'title': slide_title,
                'content': enhanced_slide_content
            })
        
        # 使用模板生成PPT
        return self.generate_ppt_from_template(template_path, topic, enhanced_content, output_filename)
    
    def _generate_ppt_outline_with_ai(self, topic: str, content_requirement: str = None):
        """
        使用AI生成PPT大纲
        
        Args:
            topic: PPT主题
            content_requirement: 用户的内容需求（可选）
            
        Returns:
            dict: PPT大纲
        """
        prompt = f"请为'{topic}'主题生成一个完整的PPT大纲，包含以下结构：\n"
        prompt += "{\n"
        prompt += "  \"topic\": \"主题名称\",\n"
        prompt += "  \"sections\": [\n"
        prompt += "    {\n"
        prompt += "      \"title\": \"章节标题\",\n"
        prompt += "      \"content\": [\"要点1\", \"要点2\", \"要点3\"]\n"
        prompt += "    }\n"
        prompt += "  ]\n"
        prompt += "}\n"
        
        if content_requirement:
            prompt += f"\n用户内容需求：{content_requirement}\n"
        
        prompt += "请确保大纲结构完整，内容合理，至少包含3个章节，每个章节至少包含3个要点。"
        
        try:
            response = self.llm_client.generate(prompt)
            # 尝试解析响应为JSON
            import json
            try:
                # 去除可能的markdown代码块标记
                if response.startswith("```json"):
                    response = response[7:]
                if response.endswith("```"):
                    response = response[:-3]
                outline = json.loads(response.strip())
                return outline
            except json.JSONDecodeError:
                # 如果解析失败，返回默认大纲
                print("解析AI生成的大纲失败，使用默认大纲")
                return {
                    'topic': topic,
                    'sections': [
                        {
                            'title': f'{topic}概述',
                            'content': [f'{topic}的定义', f'{topic}的重要性', f'{topic}的应用场景']
                        },
                        {
                            'title': f'{topic}的核心内容',
                            'content': ['核心概念', '关键技术', '实现方法']
                        },
                        {
                            'title': f'{topic}的未来发展',
                            'content': ['发展趋势', '挑战与机遇', '总结与展望']
                        }
                    ]
                }
        except Exception as e:
            print(f"生成PPT大纲失败: {str(e)}")
            # 失败时返回默认大纲
            return {
                'topic': topic,
                'sections': [
                    {
                        'title': f'{topic}概述',
                        'content': [f'{topic}的定义', f'{topic}的重要性', f'{topic}的应用场景']
                    },
                    {
                        'title': f'{topic}的核心内容',
                        'content': ['核心概念', '关键技术', '实现方法']
                    },
                    {
                        'title': f'{topic}的未来发展',
                        'content': ['发展趋势', '挑战与机遇', '总结与展望']
                    }
                ]
            }
    
    def get_available_templates(self):
        """
        获取所有可用模板
        
        Returns:
            list: 模板列表
        """
        return self.template_manager.get_available_templates()
    
    def get_template_preview(self, template_id: str = None):
        """
        获取模板预览信息
        
        Args:
            template_id: 模板ID
            
        Returns:
            dict: 模板预览信息
        """
        return self.template_manager.get_template_preview(template_id)
    

    
    def _enhance_slide_content_with_ai(self, topic: str, slide_title: str, slide_content: list):
        """
        使用AI增强幻灯片内容
        
        Args:
            topic: PPT主题
            slide_title: 幻灯片标题
            slide_content: 幻灯片内容
            
        Returns:
            list: 增强后的内容
        """
        prompt = f"请增强'{topic}'主题下'{slide_title}'幻灯片的内容。\n"
        prompt += f"当前内容：{', '.join(slide_content)}\n"
        prompt += "请生成更详细、更有深度的内容，保持要点式结构，每个要点简洁明了。\n"
        prompt += "请以列表形式输出，每个要点一行。"
        
        try:
            response = self.llm_client.generate(prompt)
            # 解析响应，提取增强后的内容
            enhanced_content = [line.strip() for line in response.split('\n') if line.strip()]
            # 确保内容不为空
            return enhanced_content if enhanced_content else slide_content
        except Exception as e:
            print(f"增强幻灯片内容失败: {str(e)}")
            # 失败时返回原始内容
            return slide_content

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
    
    # 测试使用模板生成
    output_path = generator.generate_ppt(test_topic, test_content, template_id="education")
    print(f"使用教育模板生成PPT成功: {output_path}")
    
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
    
    output_path2 = generator.generate_ppt_from_outline(test_outline, template_id="technology")
    print(f"使用科技模板从大纲生成PPT成功: {output_path2}")
    
    # 测试获取可用模板
    templates = generator.get_available_templates()
    print(f"可用模板: {templates}")
    
    # 测试模板预览
    preview = generator.get_template_preview("business")
    print(f"商务模板预览: {preview}")