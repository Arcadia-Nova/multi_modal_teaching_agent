import os
import json
from app.config import settings
from app.core.generator.llm_client import get_llm_client

class GameGenerator:
    def __init__(self):
        """初始化游戏生成器"""
        self.llm_client = get_llm_client()
    
    def generate_game(self, topic: str, content: list, game_type: str = "quiz", output_filename: str = None):
        """
        生成HTML5互动小游戏
        
        Args:
            topic: 游戏主题
            content: 游戏内容，根据游戏类型不同而不同
            game_type: 游戏类型，支持 quiz（ quiz 游戏）、memory（记忆游戏）、matching（匹配游戏）
            output_filename: 输出文件名
            
        Returns:
            str: 生成的游戏文件路径
        """
        # 生成文件名
        if not output_filename:
            output_filename = f"{topic.replace(' ', '_')}_game.html"
        
        # 确保输出目录存在
        os.makedirs(settings.EXPORT_DIR, exist_ok=True)
        
        # 生成游戏HTML
        if game_type == "quiz":
            game_html = self._generate_quiz_game(topic, content)
        elif game_type == "memory":
            game_html = self._generate_memory_game(topic, content)
        elif game_type == "matching":
            game_html = self._generate_matching_game(topic, content)
        else:
            game_html = self._generate_quiz_game(topic, content)  # 默认生成quiz游戏
        
        # 保存游戏文件
        output_path = os.path.join(settings.EXPORT_DIR, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(game_html)
        
        return output_path
    
    def _generate_quiz_game(self, topic: str, content: list):
        """生成问答游戏"""
        questions = []
        for item in content:
            if isinstance(item, dict) and 'title' in item and 'content' in item:
                question = {
                    'question': item['title'],
                    'options': item['content'][:4],  # 最多4个选项
                    'correct': item.get('correct', 0)  # 使用AI生成的正确答案索引，如果没有则默认为0
                }
                questions.append(question)
        
        # 生成HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 问答游戏</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }')
        html_parts.append('.container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }')
        html_parts.append('h1 { text-align: center; color: #333; }')
        html_parts.append('.question { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }')
        html_parts.append('.question h3 { margin-top: 0; color: #555; }')
        html_parts.append('.options { margin-top: 10px; }')
        html_parts.append('.option { margin: 5px 0; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; }')
        html_parts.append('.option:hover { background-color: #e9e9e9; }')
        html_parts.append('.option.correct { background-color: #d4edda; border-color: #c3e6cb; }')
        html_parts.append('.option.incorrect { background-color: #f8d7da; border-color: #f5c6cb; }')
        html_parts.append('.option.selected { background-color: #e3f2fd; border-color: #bbdefb; }')
        html_parts.append('#result { margin-top: 20px; padding: 15px; background-color: #e3f2fd; border-radius: 5px; text-align: center; font-size: 18px; font-weight: bold; }')
        html_parts.append('#submit-btn { display: block; width: 100%; padding: 10px; margin-top: 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }')
        html_parts.append('#submit-btn:hover { background-color: #45a049; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<div id="quiz">')
        
        for i, q in enumerate(questions):
            html_parts.append(f'<div class="question">')
            html_parts.append(f'<h3>问题 {i+1}: {q["question"]}</h3>')
            html_parts.append('<div class="options">')
            
            for j, option in enumerate(q['options']):
                html_parts.append(f'<div class="option" data-question="{i}" data-option="{j}">{option}</div>')
            
            html_parts.append('</div>')
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        html_parts.append('<button id="submit-btn">提交答案</button>')
        html_parts.append('<div id="result"></div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append(f'const questions = {json.dumps(questions)};')
        html_parts.append('const options = document.querySelectorAll(".option");')
        html_parts.append('const submitBtn = document.getElementById("submit-btn");')
        html_parts.append('const resultDiv = document.getElementById("result");')
        html_parts.append('let selectedAnswers = {};')
        html_parts.append('options.forEach(option => {')
        html_parts.append('option.addEventListener("click", function() {')
        html_parts.append('const question = this.getAttribute("data-question");')
        html_parts.append('const optionValue = this.getAttribute("data-option");')
        html_parts.append('document.querySelectorAll(".option").forEach(opt => {')
        html_parts.append('if (opt.getAttribute("data-question") === question) {')
        html_parts.append('opt.classList.remove("selected");')
        html_parts.append('}')
        html_parts.append('});')
        html_parts.append('this.classList.add("selected");')
        html_parts.append('selectedAnswers[question] = optionValue;')
        html_parts.append('});')
        html_parts.append('});')
        html_parts.append('submitBtn.addEventListener("click", function() {')
        html_parts.append('let score = 0;')
        html_parts.append('questions.forEach((q, index) => {')
        html_parts.append('const selected = selectedAnswers[index];')
        html_parts.append('if (selected && parseInt(selected) === q.correct) {')
        html_parts.append('score++;')
        html_parts.append('document.querySelectorAll(".option").forEach(opt => {')
        html_parts.append('if (opt.getAttribute("data-question") === index.toString() && opt.getAttribute("data-option") === q.correct.toString()) {')
        html_parts.append('opt.classList.add("correct");')
        html_parts.append('}')
        html_parts.append('});')
        html_parts.append('} else if (selected) {')
        html_parts.append('document.querySelectorAll(".option").forEach(opt => {')
        html_parts.append('if (opt.getAttribute("data-question") === index.toString() && opt.getAttribute("data-option") === selected.toString()) {')
        html_parts.append('opt.classList.add("incorrect");')
        html_parts.append('}')
        html_parts.append('});')
        html_parts.append('document.querySelectorAll(".option").forEach(opt => {')
        html_parts.append('if (opt.getAttribute("data-question") === index.toString() && opt.getAttribute("data-option") === q.correct.toString()) {')
        html_parts.append('opt.classList.add("correct");')
        html_parts.append('}')
        html_parts.append('});')
        html_parts.append('}')
        html_parts.append('});')
        html_parts.append('resultDiv.textContent = "得分: " + score + "/" + questions.length;')
        html_parts.append('submitBtn.disabled = true;')
        html_parts.append('});')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return ''.join(html_parts)
    
    def _generate_memory_game(self, topic: str, content: list):
        """生成记忆游戏"""
        # 提取内容作为记忆卡片
        cards = []
        for item in content:
            if isinstance(item, dict) and 'title' in item:
                cards.append(item['title'])
            elif isinstance(item, str):
                cards.append(item)
        
        # 确保卡片数量为偶数
        if len(cards) % 2 != 0 and len(cards) > 1:
            cards.append(cards[-1])
        
        # 生成HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 记忆游戏</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }')
        html_parts.append('.container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }')
        html_parts.append('h1 { text-align: center; color: #333; }')
        html_parts.append('.game-board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }')
        html_parts.append('.card { aspect-ratio: 1; background-color: #4CAF50; color: white; display: flex; align-items: center; justify-content: center; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: all 0.3s ease; }')
        html_parts.append('.card.flipped { background-color: #2196F3; }')
        html_parts.append('.card.matched { background-color: #ff9800; cursor: default; }')
        html_parts.append('#score { text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 20px; }')
        html_parts.append('#reset-btn { display: block; width: 100%; padding: 10px; margin-top: 20px; background-color: #f44336; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }')
        html_parts.append('#reset-btn:hover { background-color: #da190b; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<div id="score">尝试次数: 0</div>')
        html_parts.append('<div class="game-board" id="game-board"></div>')
        html_parts.append('<button id="reset-btn">重新开始</button>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append(f'const cards = {json.dumps(cards)};')
        html_parts.append('let gameBoard = document.getElementById("game-board");')
        html_parts.append('let scoreDisplay = document.getElementById("score");')
        html_parts.append('let resetBtn = document.getElementById("reset-btn");')
        html_parts.append('let flippedCards = [];')
        html_parts.append('let matchedPairs = 0;')
        html_parts.append('let attempts = 0;')
        html_parts.append('let gameActive = true;')
        html_parts.append('function initGame() {')
        html_parts.append('flippedCards = [];')
        html_parts.append('matchedPairs = 0;')
        html_parts.append('attempts = 0;')
        html_parts.append('gameActive = true;')
        html_parts.append('scoreDisplay.textContent = "尝试次数: " + attempts;')
        html_parts.append('gameBoard.innerHTML = "";')
        html_parts.append('let gameCards = [...cards, ...cards];')
        html_parts.append('gameCards.sort(() => Math.random() - 0.5);')
        html_parts.append('gameCards.forEach((card, index) => {')
        html_parts.append('const cardElement = document.createElement("div");')
        html_parts.append('cardElement.classList.add("card");')
        html_parts.append('cardElement.dataset.index = index;')
        html_parts.append('cardElement.dataset.value = card;')
        html_parts.append('cardElement.textContent = "?";')
        html_parts.append('cardElement.addEventListener("click", flipCard);')
        html_parts.append('gameBoard.appendChild(cardElement);')
        html_parts.append('});')
        html_parts.append('}')
        html_parts.append('function flipCard() {')
        html_parts.append('if (!gameActive || this.classList.contains("flipped") || this.classList.contains("matched")) {')
        html_parts.append('return;')
        html_parts.append('}')
        html_parts.append('this.classList.add("flipped");')
        html_parts.append('this.textContent = this.dataset.value;')
        html_parts.append('flippedCards.push(this);')
        html_parts.append('if (flippedCards.length === 2) {')
        html_parts.append('attempts++;')
        html_parts.append('scoreDisplay.textContent = "尝试次数: " + attempts;')
        html_parts.append('if (flippedCards[0].dataset.value === flippedCards[1].dataset.value) {')
        html_parts.append('flippedCards.forEach(card => {')
        html_parts.append('card.classList.add("matched");')
        html_parts.append('});')
        html_parts.append('matchedPairs++;')
        html_parts.append('if (matchedPairs === cards.length) {')
        html_parts.append('gameActive = false;')
        html_parts.append('scoreDisplay.textContent = "游戏完成! 尝试次数: " + attempts;')
        html_parts.append('}')
        html_parts.append('} else {')
        html_parts.append('gameActive = false;')
        html_parts.append('setTimeout(() => {')
        html_parts.append('flippedCards.forEach(card => {')
        html_parts.append('card.classList.remove("flipped");')
        html_parts.append('card.textContent = "?";')
        html_parts.append('});')
        html_parts.append('gameActive = true;')
        html_parts.append('}, 1000);')
        html_parts.append('}')
        html_parts.append('flippedCards = [];')
        html_parts.append('}')
        html_parts.append('}')
        html_parts.append('resetBtn.addEventListener("click", initGame);')
        html_parts.append('initGame();')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return ''.join(html_parts)
    
    def _generate_matching_game(self, topic: str, content: list):
        """生成匹配游戏"""
        # 提取匹配对
        pairs = []
        for item in content:
            if isinstance(item, dict) and 'title' in item and 'content' in item:
                for subitem in item['content']:
                    pairs.append({
                        'left': item['title'],
                        'right': subitem
                    })
        
        # 生成HTML
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 匹配游戏</title>')
        html_parts.append('<style>')
        html_parts.append('body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; }')
        html_parts.append('.container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }')
        html_parts.append('h1 { text-align: center; color: #333; }')
        html_parts.append('.game-area { display: flex; justify-content: space-around; margin: 20px 0; }')
        html_parts.append('.column { flex: 1; padding: 10px; }')
        html_parts.append('.item { padding: 10px; margin: 5px 0; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 4px; cursor: grab; text-align: center; }')
        html_parts.append('.item:active { cursor: grabbing; }')
        html_parts.append('.drop-zone { min-height: 50px; border: 2px dashed #ccc; border-radius: 4px; margin: 5px 0; padding: 10px; text-align: center; }')
        html_parts.append('.drop-zone.active { border-color: #4CAF50; background-color: #f0f8f0; }')
        html_parts.append('.drop-zone.correct { border-color: #4CAF50; background-color: #d4edda; }')
        html_parts.append('.drop-zone.incorrect { border-color: #f44336; background-color: #f8d7da; }')
        html_parts.append('#result { margin-top: 20px; padding: 15px; background-color: #e3f2fd; border-radius: 5px; text-align: center; font-size: 18px; font-weight: bold; }')
        html_parts.append('#reset-btn { display: block; width: 100%; padding: 10px; margin-top: 20px; background-color: #f44336; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }')
        html_parts.append('#reset-btn:hover { background-color: #da190b; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<div class="game-area">')
        html_parts.append('<div class="column">')
        html_parts.append('<h3>左侧项目</h3>')
        html_parts.append('<div id="left-items">')
        
        for i, pair in enumerate(pairs):
            html_parts.append(f'<div class="item" draggable="true" data-id="{i}">{pair["left"]}</div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="column">')
        html_parts.append('<h3>右侧匹配</h3>')
        html_parts.append('<div id="right-items">')
        
        for i, pair in enumerate(pairs):
            html_parts.append(f'<div class="drop-zone" data-id="{i}">{pair["right"]}</div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<div id="result"></div>')
        html_parts.append('<button id="reset-btn">重新开始</button>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append(f'const pairs = {json.dumps(pairs)};')
        html_parts.append('const leftItems = document.querySelectorAll(".item");')
        html_parts.append('const dropZones = document.querySelectorAll(".drop-zone");')
        html_parts.append('const resultDiv = document.getElementById("result");')
        html_parts.append('const resetBtn = document.getElementById("reset-btn");')
        html_parts.append('let draggedItem = null;')
        html_parts.append('leftItems.forEach(item => {')
        html_parts.append('item.addEventListener("dragstart", function(e) {')
        html_parts.append('draggedItem = this;')
        html_parts.append('setTimeout(() => this.style.opacity = "0.5", 0);')
        html_parts.append('});')
        html_parts.append('item.addEventListener("dragend", function() {')
        html_parts.append('this.style.opacity = "1";')
        html_parts.append('draggedItem = null;')
        html_parts.append('});')
        html_parts.append('});')
        html_parts.append('dropZones.forEach(zone => {')
        html_parts.append('zone.addEventListener("dragover", function(e) {')
        html_parts.append('e.preventDefault();')
        html_parts.append('this.classList.add("active");')
        html_parts.append('});')
        html_parts.append('zone.addEventListener("dragleave", function() {')
        html_parts.append('this.classList.remove("active");')
        html_parts.append('});')
        html_parts.append('zone.addEventListener("drop", function(e) {')
        html_parts.append('e.preventDefault();')
        html_parts.append('this.classList.remove("active");')
        html_parts.append('const draggedId = draggedItem.dataset.id;')
        html_parts.append('const dropId = this.dataset.id;')
        html_parts.append('if (draggedId === dropId) {')
        html_parts.append('this.classList.add("correct");')
        html_parts.append('draggedItem.style.opacity = "0.5";')
        html_parts.append('draggedItem.draggable = false;')
        html_parts.append('} else {')
        html_parts.append('this.classList.add("incorrect");')
        html_parts.append('setTimeout(() => this.classList.remove("incorrect"), 1000);')
        html_parts.append('}')
        html_parts.append('checkGameComplete();')
        html_parts.append('});')
        html_parts.append('});')
        html_parts.append('function checkGameComplete() {')
        html_parts.append('const correctZones = document.querySelectorAll(".drop-zone.correct");')
        html_parts.append('if (correctZones.length === pairs.length) {')
        html_parts.append('resultDiv.textContent = "游戏完成! 所有匹配都正确!";')
        html_parts.append('}')
        html_parts.append('}')
        html_parts.append('resetBtn.addEventListener("click", function() {')
        html_parts.append('dropZones.forEach(zone => {')
        html_parts.append('zone.classList.remove("correct", "incorrect");')
        html_parts.append('});')
        html_parts.append('leftItems.forEach(item => {')
        html_parts.append('item.style.opacity = "1";')
        html_parts.append('item.draggable = true;')
        html_parts.append('});')
        html_parts.append('resultDiv.textContent = "";')
        html_parts.append('});')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return ''.join(html_parts)

# 测试代码
if __name__ == "__main__":
    generator = GameGenerator()
    
    # 测试问答游戏
    test_topic = "人工智能知识问答"
    test_content = [
        {
            'title': '人工智能诞生于哪一年?',
            'content': ['1956年', '1960年', '1970年', '1980年']
        },
        {
            'title': '以下哪项不是机器学习的类型?',
            'content': ['监督学习', '无监督学习', '强化学习', '手动学习']
        },
        {
            'title': '深度学习属于哪种学习类型?',
            'content': ['监督学习', '无监督学习', '强化学习', '以上都对']
        }
    ]
    
    output_path = generator.generate_game(test_topic, test_content, game_type="quiz")
    print(f"问答游戏生成成功: {output_path}")
    
    # 测试记忆游戏
    test_topic = "AI术语记忆"
    test_content = ["机器学习", "深度学习", "神经网络", "自然语言处理", "计算机视觉", "语音识别"]
    
    output_path2 = generator.generate_game(test_topic, test_content, game_type="memory")
    print(f"记忆游戏生成成功: {output_path2}")
    
    # 测试匹配游戏
    test_topic = "AI概念匹配"
    test_content = [
        {
            'title': '监督学习',
            'content': ['分类', '回归']
        },
        {
            'title': '无监督学习',
            'content': ['聚类', '降维']
        }
    ]
    
    output_path3 = generator.generate_game(test_topic, test_content, game_type="matching")
    print(f"匹配游戏生成成功: {output_path3}")

    # 测试AI增强功能
    print("\n测试AI增强功能...")
    # 从主题生成游戏
    ai_quiz_path = generator.generate_game_with_ai("人工智能知识", game_type="quiz")
    print(f"AI生成问答游戏成功: {ai_quiz_path}")
    
    # 增强现有游戏内容
    enhanced_memory_path = generator.enhance_game_content_with_ai("AI术语", ["机器学习", "深度学习", "神经网络"], game_type="memory")
    print(f"AI增强记忆游戏成功: {enhanced_memory_path}")

# AI增强功能
def generate_game_with_ai(self, topic: str, game_type: str = "quiz", output_filename: str = None):
    """
    使用AI生成完整游戏
    
    Args:
        topic: 游戏主题
        game_type: 游戏类型，支持 quiz（问答游戏）、memory（记忆游戏）、matching（匹配游戏）
        output_filename: 输出文件名
        
    Returns:
        str: 生成的游戏文件路径
    """
    # 使用AI生成游戏内容
    content = self._generate_game_content_with_ai(topic, game_type)
    # 生成游戏
    return self.generate_game(topic, content, game_type, output_filename)

def enhance_game_content_with_ai(self, topic: str, content: list, game_type: str = "quiz", output_filename: str = None):
    """
    使用AI增强游戏内容
    
    Args:
        topic: 游戏主题
        content: 游戏内容
        game_type: 游戏类型
        output_filename: 输出文件名
        
    Returns:
        str: 生成的游戏文件路径
    """
    # 使用AI增强游戏内容
    enhanced_content = self._enhance_game_content_with_ai(topic, content, game_type)
    # 生成游戏
    return self.generate_game(topic, enhanced_content, game_type, output_filename)

def _generate_game_content_with_ai(self, topic: str, game_type: str):
    """
    使用AI生成游戏内容
    
    Args:
        topic: 游戏主题
        game_type: 游戏类型
        
    Returns:
        list: 游戏内容
    """
    if game_type == "quiz":
        prompt = f"请为'{topic}'主题生成5个问答游戏题目，每个题目包含一个问题、4个选项和1个正确答案的索引（从0开始）。\n"
        prompt += "请以以下格式输出：\n"
        prompt += "[\n"
        prompt += "  {\n"
        prompt += "    \"title\": \"问题内容\",\n"
        prompt += "    \"content\": [\"选项1\", \"选项2\", \"选项3\", \"选项4\"],\n"
        prompt += "    \"correct\": 正确答案的索引（0-3）\n"
        prompt += "  },\n"
        prompt += "  ...\n"
        prompt += "]\n"
        prompt += "请确保问题具有教育意义，选项合理，且正确答案明确。"
    elif game_type == "memory":
        prompt = f"请为'{topic}'主题生成10个适合记忆游戏的词汇或短语。\n"
        prompt += "请以列表形式输出，每个词汇或短语占一行。\n"
        prompt += "请确保这些词汇或短语与主题相关，且易于记忆。"
    elif game_type == "matching":
        prompt = f"请为'{topic}'主题生成5对匹配项，每对包含一个概念和对应的解释或相关内容。\n"
        prompt += "请以以下格式输出：\n"
        prompt += "[\n"
        prompt += "  {\n"
        prompt += "    \"title\": \"概念\",\n"
        prompt += "    \"content\": [\"相关内容1\", \"相关内容2\"]\n"
        prompt += "  },\n"
        prompt += "  ...\n"
        prompt += "]\n"
        prompt += "请确保概念与相关内容之间有明确的对应关系。"
    else:
        # 默认生成问答游戏内容
        prompt = f"请为'{topic}'主题生成5个问答游戏题目，每个题目包含一个问题、4个选项和1个正确答案的索引（从0开始）。\n"
        prompt += "请以以下格式输出：\n"
        prompt += "[\n"
        prompt += "  {\n"
        prompt += "    \"title\": \"问题内容\",\n"
        prompt += "    \"content\": [\"选项1\", \"选项2\", \"选项3\", \"选项4\"],\n"
        prompt += "    \"correct\": 正确答案的索引（0-3）\n"
        prompt += "  },\n"
        prompt += "  ...\n"
        prompt += "]\n"
        prompt += "请确保问题具有教育意义，选项合理，且正确答案明确。"

    try:
        response = self.llm_client.generate(prompt)
        # 尝试解析响应
        import json
        try:
            # 去除可能的markdown代码块标记
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            content = json.loads(response.strip())
            return content
        except json.JSONDecodeError:
            # 如果是记忆游戏，尝试解析为列表
            if game_type == "memory":
                content = [line.strip() for line in response.split('\n') if line.strip()]
                return content
            # 解析失败，返回默认内容
            print("解析AI生成的游戏内容失败，使用默认内容")
            return self._get_default_game_content(topic, game_type)
    except Exception as e:
        print(f"生成游戏内容失败: {str(e)}")
        # 失败时返回默认内容
        return self._get_default_game_content(topic, game_type)

def _enhance_game_content_with_ai(self, topic: str, content: list, game_type: str):
    """
    使用AI增强游戏内容
    
    Args:
        topic: 游戏主题
        content: 游戏内容
        game_type: 游戏类型
        
    Returns:
        list: 增强后的游戏内容
    """
    if game_type == "quiz":
        # 增强问答游戏内容
        enhanced_content = []
        for item in content:
            if isinstance(item, dict) and 'title' in item and 'content' in item:
                prompt = f"请增强以下问答游戏题目，使其更具教育意义和挑战性：\n"
                prompt += f"问题：{item['title']}\n"
                prompt += f"选项：{', '.join(item['content'])}\n"
                prompt += "请保持问题的核心内容，同时增加一些细节或背景信息，使问题更加丰富。\n"
                prompt += "请以以下格式输出：\n"
                prompt += "{\n"
                prompt += "  \"title\": \"增强后的问题\",\n"
                prompt += "  \"content\": [\"选项1\", \"选项2\", \"选项3\", \"选项4\"]\n"
                prompt += "}\n"
                
                try:
                    response = self.llm_client.generate(prompt)
                    import json
                    enhanced_item = json.loads(response.strip())
                    enhanced_content.append(enhanced_item)
                except Exception as e:
                    print(f"增强问答题目失败: {str(e)}")
                    enhanced_content.append(item)
            else:
                enhanced_content.append(item)
        return enhanced_content
    elif game_type == "memory":
        # 增强记忆游戏内容
        prompt = f"请为'{topic}'主题增强以下记忆游戏内容，使其更加丰富和有教育意义：\n"
        prompt += f"当前内容：{', '.join(content)}\n"
        prompt += "请生成更多与主题相关的词汇或短语，确保它们易于记忆且具有教育价值。\n"
        prompt += "请以列表形式输出，每个词汇或短语占一行。"
        
        try:
            response = self.llm_client.generate(prompt)
            enhanced_content = [line.strip() for line in response.split('\n') if line.strip()]
            return enhanced_content if enhanced_content else content
        except Exception as e:
            print(f"增强记忆游戏内容失败: {str(e)}")
            return content
    elif game_type == "matching":
        # 增强匹配游戏内容
        enhanced_content = []
        for item in content:
            if isinstance(item, dict) and 'title' in item and 'content' in item:
                prompt = f"请增强以下匹配游戏内容，使其更加丰富和有教育意义：\n"
                prompt += f"概念：{item['title']}\n"
                prompt += f"相关内容：{', '.join(item['content'])}\n"
                prompt += "请为该概念添加更多相关内容，确保它们与概念有明确的对应关系。\n"
                prompt += "请以以下格式输出：\n"
                prompt += "{\n"
                prompt += "  \"title\": \"概念\",\n"
                prompt += "  \"content\": [\"相关内容1\", \"相关内容2\", ...]\n"
                prompt += "}\n"
                
                try:
                    response = self.llm_client.generate(prompt)
                    import json
                    enhanced_item = json.loads(response.strip())
                    enhanced_content.append(enhanced_item)
                except Exception as e:
                    print(f"增强匹配游戏内容失败: {str(e)}")
                    enhanced_content.append(item)
            else:
                enhanced_content.append(item)
        return enhanced_content
    else:
        return content

def _get_default_game_content(self, topic: str, game_type: str):
    """
    获取默认游戏内容
    
    Args:
        topic: 游戏主题
        game_type: 游戏类型
        
    Returns:
        list: 默认游戏内容
    """
    if game_type == "quiz":
        return [
            {
                'title': f'{topic}的基本概念是什么?',
                'content': ['选项1', '选项2', '选项3', '选项4'],
                'correct': 0
            },
            {
                'title': f'{topic}的重要性体现在哪些方面?',
                'content': ['选项1', '选项2', '选项3', '选项4'],
                'correct': 0
            },
            {
                'title': f'{topic}的应用场景有哪些?',
                'content': ['选项1', '选项2', '选项3', '选项4'],
                'correct': 0
            },
            {
                'title': f'{topic}的发展历史是怎样的?',
                'content': ['选项1', '选项2', '选项3', '选项4'],
                'correct': 0
            },
            {
                'title': f'{topic}的未来趋势是什么?',
                'content': ['选项1', '选项2', '选项3', '选项4'],
                'correct': 0
            }
        ]
    elif game_type == "memory":
        return [f'{topic}概念1', f'{topic}概念2', f'{topic}概念3', f'{topic}概念4', f'{topic}概念5']
    elif game_type == "matching":
        return [
            {
                'title': f'{topic}概念1',
                'content': ['相关内容1', '相关内容2']
            },
            {
                'title': f'{topic}概念2',
                'content': ['相关内容1', '相关内容2']
            },
            {
                'title': f'{topic}概念3',
                'content': ['相关内容1', '相关内容2']
            }
        ]
    else:
        return []

# 将AI增强方法添加到GameGenerator类
GameGenerator.generate_game_with_ai = generate_game_with_ai
GameGenerator.enhance_game_content_with_ai = enhance_game_content_with_ai
GameGenerator._generate_game_content_with_ai = _generate_game_content_with_ai
GameGenerator._enhance_game_content_with_ai = _enhance_game_content_with_ai
GameGenerator._get_default_game_content = _get_default_game_content
