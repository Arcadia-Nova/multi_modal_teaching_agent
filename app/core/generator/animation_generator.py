import os
from app.config import settings

class AnimationGenerator:
    def __init__(self):
        """初始化动画生成器"""
        pass
    
    def generate_animation(self, topic: str, content: list, animation_type: str = "slideshow", output_filename: str = None):
        """
        生成HTML5动画
        
        Args:
            topic: 动画主题
            content: 动画内容，根据动画类型不同而不同
            animation_type: 动画类型，支持 slideshow（幻灯片动画）、timeline（时间线动画）、interactive（交互式动画）
            output_filename: 输出文件名
            
        Returns:
            str: 生成的动画文件路径
        """
        # 生成文件名
        if not output_filename:
            output_filename = f"{topic.replace(' ', '_')}_animation.html"
        
        # 确保输出目录存在
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        # 生成动画HTML
        if animation_type == "slideshow":
            animation_html = self._generate_slideshow_animation(topic, content)
        elif animation_type == "timeline":
            animation_html = self._generate_timeline_animation(topic, content)
        elif animation_type == "interactive":
            animation_html = self._generate_interactive_animation(topic, content)
        else:
            animation_html = self._generate_slideshow_animation(topic, content)  # 默认生成幻灯片动画
        
        # 保存动画文件
        output_path = os.path.join(settings.EXPORT_DIR, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(animation_html)
        
        return output_path
    
    def _generate_slideshow_animation(self, topic: str, content: list):
        """生成幻灯片动画"""
        # 生成HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 幻灯片动画</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; margin: 0; padding: 0; overflow: hidden; }')
        html_parts.append('.slideshow-container { position: relative; width: 100vw; height: 100vh; }')
        html_parts.append('.slide { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; transition: opacity 1s ease-in-out; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f0f0f0; }')
        html_parts.append('.slide.active { opacity: 1; }')
        html_parts.append('.slide h2 { font-size: 2.5em; color: #333; margin-bottom: 20px; text-align: center; }')
        html_parts.append('.slide p { font-size: 1.2em; color: #666; max-width: 800px; text-align: center; padding: 0 20px; }')
        html_parts.append('.controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; z-index: 10; }')
        html_parts.append('.control-btn { width: 15px; height: 15px; border-radius: 50%; background-color: #ccc; cursor: pointer; }')
        html_parts.append('.control-btn.active { background-color: #4CAF50; }')
        html_parts.append('.nav-btn { position: absolute; top: 50%; transform: translateY(-50%); width: 50px; height: 50px; background-color: rgba(255, 255, 255, 0.8); border: none; border-radius: 50%; font-size: 24px; cursor: pointer; z-index: 10; }')
        html_parts.append('.prev-btn { left: 20px; }')
        html_parts.append('.next-btn { right: 20px; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="slideshow-container">')
        
        # 生成幻灯片内容
        for i, item in enumerate(content):
            html_parts.append(f'<div class="slide" id="slide-{i}">')
            if isinstance(item, dict) and 'title' in item:
                html_parts.append(f'<h2>{item["title"]}</h2>')
                if 'content' in item:
                    if isinstance(item['content'], list):
                        for subitem in item['content']:
                            html_parts.append(f'<p>{subitem}</p>')
                    else:
                        html_parts.append(f'<p>{item["content"]}</p>')
            elif isinstance(item, str):
                html_parts.append(f'<h2>{item}</h2>')
            html_parts.append('</div>')
        
        html_parts.append('<button class="nav-btn prev-btn" onclick="prevSlide()">←</button>')
        html_parts.append('<button class="nav-btn next-btn" onclick="nextSlide()">→</button>')
        html_parts.append('<div class="controls" id="controls">')
        
        for i in range(len(content)):
            html_parts.append(f'<div class="control-btn" id="control-{i}" onclick="goToSlide({i})"></div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append('let currentSlide = 0;')
        html_parts.append('const slides = document.querySelectorAll(".slide");')
        html_parts.append('const controls = document.querySelectorAll(".control-btn");')
        html_parts.append('const totalSlides = slides.length;')
        html_parts.append('function showSlide(index) {')
        html_parts.append('slides.forEach((slide, i) => {')
        html_parts.append('slide.classList.remove("active");')
        html_parts.append('controls[i].classList.remove("active");')
        html_parts.append('});')
        html_parts.append('slides[index].classList.add("active");')
        html_parts.append('controls[index].classList.add("active");')
        html_parts.append('currentSlide = index;')
        html_parts.append('}')
        html_parts.append('function nextSlide() {')
        html_parts.append('let nextIndex = currentSlide + 1;')
        html_parts.append('if (nextIndex >= totalSlides) nextIndex = 0;')
        html_parts.append('showSlide(nextIndex);')
        html_parts.append('}')
        html_parts.append('function prevSlide() {')
        html_parts.append('let prevIndex = currentSlide - 1;')
        html_parts.append('if (prevIndex < 0) prevIndex = totalSlides - 1;')
        html_parts.append('showSlide(prevIndex);')
        html_parts.append('}')
        html_parts.append('function goToSlide(index) {')
        html_parts.append('showSlide(index);')
        html_parts.append('}')
        html_parts.append('// 自动播放')
        html_parts.append('let autoplayInterval = setInterval(nextSlide, 5000);')
        html_parts.append('// 初始化显示第一张幻灯片')
        html_parts.append('showSlide(0);')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return ''.join(html_parts)
    
    def _generate_timeline_animation(self, topic: str, content: list):
        """生成时间线动画"""
        # 生成HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 时间线动画</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f0f0; }')
        html_parts.append('.container { max-width: 1000px; margin: 0 auto; }')
        html_parts.append('h1 { text-align: center; color: #333; margin-bottom: 50px; }')
        html_parts.append('.timeline { position: relative; margin: 0 auto; padding: 40px 0; }')
        html_parts.append('.timeline::after { content: ""; position: absolute; width: 6px; background-color: #4CAF50; top: 0; bottom: 0; left: 50%; margin-left: -3px; }')
        html_parts.append('.timeline-item { padding: 10px 40px; position: relative; width: 45%; box-sizing: border-box; }')
        html_parts.append('.timeline-item.left { left: 0; }')
        html_parts.append('.timeline-item.right { left: 55%; }')
        html_parts.append('.timeline-item::after { content: ""; position: absolute; width: 25px; height: 25px; right: -13px; top: 15px; border-radius: 50%; background-color: white; border: 4px solid #4CAF50; z-index: 1; }')
        html_parts.append('.timeline-item.right::after { left: -13px; }')
        html_parts.append('.timeline-content { padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); opacity: 0; transform: translateY(20px); transition: all 0.5s ease; }')
        html_parts.append('.timeline-content.visible { opacity: 1; transform: translateY(0); }')
        html_parts.append('.timeline-content h2 { margin-top: 0; color: #4CAF50; }')
        html_parts.append('.timeline-content p { margin-bottom: 0; color: #666; }')
        html_parts.append('@media screen and (max-width: 768px) {')
        html_parts.append('.timeline::after { left: 31px; }')
        html_parts.append('.timeline-item { width: 100%; padding-left: 70px; padding-right: 25px; }')
        html_parts.append('.timeline-item.right { left: 0%; }')
        html_parts.append('.timeline-item::after { left: 18px; }')
        html_parts.append('.timeline-item.right::after { left: 18px; }')
        html_parts.append('}')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<div class="timeline" id="timeline">')
        
        # 生成时间线内容
        for i, item in enumerate(content):
            side = "left" if i % 2 == 0 else "right"
            html_parts.append(f'<div class="timeline-item {side}">')
            html_parts.append('<div class="timeline-content">')
            if isinstance(item, dict) and 'title' in item:
                html_parts.append(f'<h2>{item["title"]}</h2>')
                if 'content' in item:
                    if isinstance(item['content'], list):
                        for subitem in item['content']:
                            html_parts.append(f'<p>{subitem}</p>')
                    else:
                        html_parts.append(f'<p>{item["content"]}</p>')
            elif isinstance(item, str):
                html_parts.append(f'<h2>{item}</h2>')
            html_parts.append('</div>')
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append('function checkVisibility() {')
        html_parts.append('const items = document.querySelectorAll(".timeline-content");')
        html_parts.append('items.forEach(item => {')
        html_parts.append('const rect = item.getBoundingClientRect();')
        html_parts.append('const windowHeight = window.innerHeight || document.documentElement.clientHeight;')
        html_parts.append('if (rect.top <= windowHeight * 0.8) {')
        html_parts.append('item.classList.add("visible");')
        html_parts.append('}')
        html_parts.append('});')
        html_parts.append('}')
        html_parts.append('// 初始检查')
        html_parts.append('checkVisibility();')
        html_parts.append('// 滚动时检查')
        html_parts.append('window.addEventListener("scroll", checkVisibility);')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return ''.join(html_parts)
    
    def _generate_interactive_animation(self, topic: str, content: list):
        """生成交互式动画"""
        # 生成HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 交互式动画</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f0f0; }')
        html_parts.append('.container { max-width: 1000px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }')
        html_parts.append('h1 { text-align: center; color: #333; }')
        html_parts.append('.interactive-area { margin: 40px 0; }')
        html_parts.append('.interactive-item { margin: 20px 0; padding: 20px; border: 2px solid #ddd; border-radius: 8px; transition: all 0.3s ease; cursor: pointer; }')
        html_parts.append('.interactive-item:hover { border-color: #4CAF50; box-shadow: 0 0 10px rgba(76, 175, 80, 0.2); }')
        html_parts.append('.interactive-item.active { border-color: #4CAF50; background-color: #f0f8f0; }')
        html_parts.append('.interactive-item h2 { margin-top: 0; color: #4CAF50; }')
        html_parts.append('.interactive-item p { margin-bottom: 0; color: #666; }')
        html_parts.append('.interactive-item .details { display: none; margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; }')
        html_parts.append('.interactive-item.active .details { display: block; }')
        html_parts.append('.progress-bar { width: 100%; height: 20px; background-color: #f0f0f0; border-radius: 10px; margin: 20px 0; overflow: hidden; }')
        html_parts.append('.progress-fill { height: 100%; background-color: #4CAF50; width: 0%; transition: width 0.5s ease; }')
        html_parts.append('#progress-text { text-align: center; color: #666; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<div class="progress-bar">')
        html_parts.append('<div class="progress-fill" id="progress-fill"></div>')
        html_parts.append('</div>')
        html_parts.append('<div id="progress-text">完成度: 0%</div>')
        html_parts.append('<div class="interactive-area" id="interactive-area">')
        
        # 生成交互式内容
        for i, item in enumerate(content):
            html_parts.append(f'<div class="interactive-item" id="item-{i}" onclick="toggleItem({i})">')
            if isinstance(item, dict) and 'title' in item:
                html_parts.append(f'<h2>{item["title"]}</h2>')
                if 'content' in item:
                    if isinstance(item['content'], list):
                        for subitem in item['content']:
                            html_parts.append(f'<p>{subitem}</p>')
                    else:
                        html_parts.append(f'<p>{item["content"]}</p>')
                if 'details' in item:
                    html_parts.append('<div class="details">')
                    if isinstance(item['details'], list):
                        for detail in item['details']:
                            html_parts.append(f'<p>{detail}</p>')
                    else:
                        html_parts.append(f'<p>{item["details"]}</p>')
                    html_parts.append('</div>')
            elif isinstance(item, str):
                html_parts.append(f'<h2>{item}</h2>')
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append('let activeItems = new Set();')
        html_parts.append('const totalItems = document.querySelectorAll(".interactive-item").length;')
        html_parts.append('function toggleItem(index) {')
        html_parts.append('const item = document.getElementById("item-" + index);')
        html_parts.append('if (item.classList.contains("active")) {')
        html_parts.append('item.classList.remove("active");')
        html_parts.append('activeItems.delete(index);')
        html_parts.append('} else {')
        html_parts.append('item.classList.add("active");')
        html_parts.append('activeItems.add(index);')
        html_parts.append('}')
        html_parts.append('updateProgress();')
        html_parts.append('}')
        html_parts.append('function updateProgress() {')
        html_parts.append('const progress = (activeItems.size / totalItems) * 100;')
        html_parts.append('document.getElementById("progress-fill").style.width = progress + "%";')
        html_parts.append('document.getElementById("progress-text").textContent = "完成度: " + Math.round(progress) + "%";')
        html_parts.append('}')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return ''.join(html_parts)

# 测试代码
if __name__ == "__main__":
    generator = AnimationGenerator()
    
    # 测试幻灯片动画
    test_topic = "人工智能发展历程"
    test_content = [
        {
            'title': '1956年',
            'content': '人工智能概念诞生'
        },
        {
            'title': '1960-1970年代',
            'content': '早期AI研究与发展'
        },
        {
            'title': '1980-1990年代',
            'content': '专家系统与机器学习兴起'
        },
        {
            'title': '2000年代',
            'content': '大数据与深度学习发展'
        },
        {
            'title': '2010年代至今',
            'content': 'AI技术突破与广泛应用'
        }
    ]
    
    output_path = generator.generate_animation(test_topic, test_content, animation_type="slideshow")
    print(f"幻灯片动画生成成功: {output_path}")
    
    # 测试时间线动画
    test_topic = "AI重要事件时间线"
    test_content = [
        {
            'title': '1956年',
            'content': '达特茅斯会议，AI概念正式提出'
        },
        {
            'title': '1969年',
            'content': '第一个专家系统DENDRAL开发成功'
        },
        {
            'title': '1997年',
            'content': 'IBM深蓝战胜国际象棋世界冠军卡斯帕罗夫'
        },
        {
            'title': '2011年',
            'content': 'IBM Watson在Jeopardy!节目中获胜'
        },
        {
            'title': '2016年',
            'content': 'AlphaGo战胜围棋世界冠军李世石'
        }
    ]
    
    output_path2 = generator.generate_animation(test_topic, test_content, animation_type="timeline")
    print(f"时间线动画生成成功: {output_path2}")
    
    # 测试交互式动画
    test_topic = "AI技术分类"
    test_content = [
        {
            'title': '机器学习',
            'content': '让计算机从数据中学习的技术',
            'details': ['监督学习', '无监督学习', '强化学习']
        },
        {
            'title': '深度学习',
            'content': '基于神经网络的机器学习方法',
            'details': ['卷积神经网络', '循环神经网络', '生成对抗网络']
        },
        {
            'title': '自然语言处理',
            'content': '让计算机理解和处理人类语言',
            'details': ['文本分类', '情感分析', '机器翻译']
        },
        {
            'title': '计算机视觉',
            'content': '让计算机理解和处理图像和视频',
            'details': ['目标检测', '图像分类', '人脸识别']
        }
    ]
    
    output_path3 = generator.generate_animation(test_topic, test_content, animation_type="interactive")
    print(f"交互式动画生成成功: {output_path3}")
