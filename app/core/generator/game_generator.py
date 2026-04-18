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
                    'options': item['content'][:4],
                    'correct': item.get('correct', 0)
                }
                questions.append(question)

        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 问答游戏</title>')
        html_parts.append('<style>')
        html_parts.append('* { box-sizing: border-box; margin: 0; padding: 0; }')
        html_parts.append('body { font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); min-height: 100vh; padding: 20px; }')
        html_parts.append('.container { max-width: 800px; margin: 0 auto; }')
        html_parts.append('.header { text-align: center; color: white; margin-bottom: 30px; }')
        html_parts.append('.header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }')
        html_parts.append('.progress-bar { background: rgba(255,255,255,0.3); height: 12px; border-radius: 6px; margin-bottom: 25px; overflow: hidden; }')
        html_parts.append('.progress-fill { background: white; height: 100%; border-radius: 6px; transition: width 0.4s ease; }')
        html_parts.append('.score-board { display: flex; justify-content: center; gap: 30px; margin-bottom: 25px; }')
        html_parts.append('.score-item { background: rgba(255,255,255,0.2); padding: 10px 25px; border-radius: 50px; color: white; font-size: 1.1em; backdrop-filter: blur(5px); }')
        html_parts.append('.question-card { background: white; border-radius: 16px; padding: 30px; margin-bottom: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }')
        html_parts.append('.question-number { display: inline-block; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; margin-bottom: 15px; }')
        html_parts.append('.question-text { font-size: 1.4em; color: #333; margin-bottom: 25px; line-height: 1.6; }')
        html_parts.append('.options { display: flex; flex-direction: column; gap: 12px; }')
        html_parts.append('.option { padding: 18px 25px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 3px solid #dee2e6; border-radius: 12px; cursor: pointer; font-size: 1.1em; transition: all 0.3s ease; text-align: left; }')
        html_parts.append('.option:hover:not(.disabled) { transform: translateX(5px); border-color: #11998e; background: linear-gradient(135deg, #e8f5f3 0%, #d4edda 100%); }')
        html_parts.append('.option.selected { border-color: #11998e; background: linear-gradient(135deg, #d1f2eb 0%, #c3e6cb 100%); }')
        html_parts.append('.option.correct { border-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); animation: pulse 0.5s ease; }')
        html_parts.append('.option.incorrect { border-color: #dc3545; background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); animation: shake 0.5s ease; }')
        html_parts.append('.option.disabled { cursor: default; opacity: 0.7; }')
        html_parts.append('@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }')
        html_parts.append('@keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-8px); } 75% { transform: translateX(8px); } }')
        html_parts.append('.nav-buttons { display: flex; gap: 15px; margin-top: 20px; }')
        html_parts.append('.btn { padding: 15px 35px; font-size: 1.1em; border: none; border-radius: 50px; cursor: pointer; transition: all 0.3s ease; }')
        html_parts.append('.btn-primary { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }')
        html_parts.append('.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 5px 20px rgba(17,153,142,0.4); }')
        html_parts.append('.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }')
        html_parts.append('.result-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); justify-content: center; align-items: center; z-index: 1000; }')
        html_parts.append('.result-modal.show { display: flex; }')
        html_parts.append('.result-content { background: white; padding: 50px 70px; border-radius: 20px; text-align: center; animation: popIn 0.5s ease; }')
        html_parts.append('@keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }')
        html_parts.append('.result-content h2 { font-size: 2.5em; margin-bottom: 15px; }')
        html_parts.append('.result-content .score { font-size: 3em; font-weight: bold; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 20px 0; }')
        html_parts.append('.result-content p { font-size: 1.2em; color: #666; margin-bottom: 30px; }')
        html_parts.append('.stars { font-size: 2em; margin-bottom: 20px; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append('<div class="header">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<p style="font-size:1.2em;opacity:0.9;">测试你的知识！</p>')
        html_parts.append('</div>')
        html_parts.append('<div class="progress-bar"><div class="progress-fill" id="progress"></div></div>')
        html_parts.append('<div class="score-board">')
        html_parts.append('<div class="score-item">⏱️ <span id="timer">0</span>秒</div>')
        html_parts.append('<div class="score-item">✅ <span id="current">1</span>/' + str(len(questions)) + '</div>')
        html_parts.append('<div class="score-item">⭐ <span id="score">0</span>分</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="question-card" id="question-card">')
        html_parts.append('<div class="question-number" id="question-number">第 1 题</div>')
        html_parts.append('<div class="question-text" id="question-text"></div>')
        html_parts.append('<div class="options" id="options"></div>')
        html_parts.append('<div class="nav-buttons">')
        html_parts.append('<button class="btn btn-primary" id="prev-btn" disabled>← 上一题</button>')
        html_parts.append('<button class="btn btn-primary" id="next-btn">下一题 →</button>')
        html_parts.append('<button class="btn btn-primary" id="submit-btn" style="display:none;">提交答案</button>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="result-modal" id="result-modal">')
        html_parts.append('<div class="result-content">')
        html_parts.append('<div class="stars" id="stars"></div>')
        html_parts.append('<h2 id="result-title">游戏结束!</h2>')
        html_parts.append('<div class="score" id="final-score"></div>')
        html_parts.append('<p id="result-text"></p>')
        html_parts.append('<button class="btn btn-primary" onclick="resetGame()">再玩一次</button>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append(f'const questions = {json.dumps(questions)};')
        html_parts.append('let currentQuestion = 0;')
        html_parts.append('let score = 0;')
        html_parts.append('let startTime = Date.now();')
        html_parts.append('let answered = [];')
        html_parts.append('let timerInterval;')
        html_parts.append('function updateTimer() { document.getElementById("timer").textContent = Math.floor((Date.now() - startTime) / 1000); }')
        html_parts.append('function updateProgress() { document.getElementById("progress").style.width = ((currentQuestion + 1) / questions.length * 100) + "%"; }')
        html_parts.append('function showQuestion() { const q = questions[currentQuestion]; document.getElementById("question-number").textContent = "第 " + (currentQuestion + 1) + " 题"; document.getElementById("question-text").textContent = q.question; document.getElementById("current").textContent = currentQuestion + 1; updateProgress(); const optionsDiv = document.getElementById("options"); optionsDiv.innerHTML = ""; q.options.forEach((opt, i) => { const btn = document.createElement("div"); btn.className = "option"; if (answered[currentQuestion] !== undefined) { btn.classList.add("disabled"); if (i === q.correct) btn.classList.add("correct"); if (i === answered[currentQuestion] && i !== q.correct) btn.classList.add("incorrect"); } btn.textContent = String.fromCharCode(65 + i) + ". " + opt; if (answered[currentQuestion] === undefined) btn.onclick = () => selectOption(i); optionsDiv.appendChild(btn); }); document.getElementById("prev-btn").disabled = currentQuestion === 0; const isLast = currentQuestion === questions.length - 1; document.getElementById("next-btn").style.display = isLast ? "none" : "inline-block"; document.getElementById("submit-btn").style.display = isLast && answered[currentQuestion] !== undefined ? "inline-block" : "none"; }')
        html_parts.append('function selectOption(optIndex) { const q = questions[currentQuestion]; answered[currentQuestion] = optIndex; document.querySelectorAll(".option").forEach((opt, i) => { opt.classList.add("disabled"); if (i === q.correct) opt.classList.add("correct"); if (i === optIndex && i !== q.correct) opt.classList.add("incorrect"); }); if (optIndex === q.correct) { score++; document.getElementById("score").textContent = score; } const isLast = currentQuestion === questions.length - 1; document.getElementById("submit-btn").style.display = isLast ? "inline-block" : "none"; }')
        html_parts.append('function nextQuestion() { if (currentQuestion < questions.length - 1) { currentQuestion++; showQuestion(); } }')
        html_parts.append('function prevQuestion() { if (currentQuestion > 0) { currentQuestion--; showQuestion(); } }')
        html_parts.append('function showResult() { clearInterval(timerInterval); const elapsed = Math.floor((Date.now() - startTime) / 1000); const pct = Math.round(score / questions.length * 100); let stars = ""; for (let i = 0; i < 3; i++) stars += pct >= (i + 1) * 30 ? "⭐" : "☆"; let title = pct >= 80 ? "🎉 太棒了!" : pct >= 60 ? "👍 不错!" : "💪 继续加油!"; document.getElementById("stars").textContent = stars; document.getElementById("result-title").textContent = title; document.getElementById("final-score").textContent = score + "/" + questions.length; document.getElementById("result-text").textContent = "用时" + elapsed + "秒，正确率" + pct + "%"; document.getElementById("result-modal").classList.add("show"); }')
        html_parts.append('function resetGame() { currentQuestion = 0; score = 0; answered = []; startTime = Date.now(); document.getElementById("score").textContent = "0"; document.getElementById("result-modal").classList.remove("show"); showQuestion(); timerInterval = setInterval(updateTimer, 1000); }')
        html_parts.append('document.getElementById("next-btn").onclick = nextQuestion;')
        html_parts.append('document.getElementById("prev-btn").onclick = prevQuestion;')
        html_parts.append('document.getElementById("submit-btn").onclick = showResult;')
        html_parts.append('timerInterval = setInterval(updateTimer, 1000);')
        html_parts.append('showQuestion();')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')

        return ''.join(html_parts)
    
    def _generate_memory_game(self, topic: str, content: list):
        """生成记忆游戏"""
        cards = []
        for item in content:
            if isinstance(item, dict) and 'title' in item:
                cards.append(item['title'])
            elif isinstance(item, str):
                cards.append(item)

        if len(cards) % 2 != 0 and len(cards) > 1:
            cards.append(cards[-1])

        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 记忆游戏</title>')
        html_parts.append('<style>')
        html_parts.append('* { box-sizing: border-box; margin: 0; padding: 0; }')
        html_parts.append('body { font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); min-height: 100vh; padding: 20px; }')
        html_parts.append('.container { max-width: 700px; margin: 0 auto; }')
        html_parts.append('.header { text-align: center; color: white; margin-bottom: 30px; }')
        html_parts.append('.header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }')
        html_parts.append('.score-board { display: flex; justify-content: center; gap: 30px; margin-bottom: 25px; }')
        html_parts.append('.score-item { background: rgba(255,255,255,0.2); padding: 12px 30px; border-radius: 50px; color: white; font-size: 1.2em; backdrop-filter: blur(5px); }')
        html_parts.append('.game-board { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }')
        html_parts.append('.card { aspect-ratio: 1; perspective: 1000px; cursor: pointer; }')
        html_parts.append('.card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; }')
        html_parts.append('.card.flipped .card-inner { transform: rotateY(180deg); }')
        html_parts.append('.card.matched .card-inner { transform: rotateY(180deg); }')
        html_parts.append('.card.matched { cursor: default; }')
        html_parts.append('.card-front, .card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 0.9em; text-align: center; padding: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); }')
        html_parts.append('.card-front { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 2em; }')
        html_parts.append('.card-back { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color: #333; transform: rotateY(180deg); font-weight: bold; line-height: 1.4; }')
        html_parts.append('.card.matched .card-front { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }')
        html_parts.append('.card.matched .card-back { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); }')
        html_parts.append('.result-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); justify-content: center; align-items: center; z-index: 1000; }')
        html_parts.append('.result-modal.show { display: flex; }')
        html_parts.append('.result-content { background: white; padding: 50px 70px; border-radius: 20px; text-align: center; animation: popIn 0.5s ease; }')
        html_parts.append('@keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }')
        html_parts.append('.result-content h2 { font-size: 2.5em; color: #11998e; margin-bottom: 15px; }')
        html_parts.append('.result-content .score { font-size: 3em; font-weight: bold; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 20px 0; }')
        html_parts.append('.result-content p { font-size: 1.2em; color: #666; margin-bottom: 30px; }')
        html_parts.append('.btn { padding: 15px 40px; font-size: 1.2em; border: none; border-radius: 50px; cursor: pointer; transition: all 0.3s ease; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }')
        html_parts.append('.btn:hover { transform: translateY(-3px); box-shadow: 0 5px 20px rgba(245,87,108,0.4); }')
        html_parts.append('.stars { font-size: 2em; margin-bottom: 15px; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append('<div class="header">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<p style="font-size:1.2em;opacity:0.9;">找出所有配对卡牌！</p>')
        html_parts.append('</div>')
        html_parts.append('<div class="score-board">')
        html_parts.append('<div class="score-item">⏱️ <span id="timer">0</span>秒</div>')
        html_parts.append('<div class="score-item">🎯 <span id="pairs">0</span>/' + str(len(cards)) + '对</div>')
        html_parts.append('<div class="score-item">🔄 <span id="moves">0</span>次</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="game-board" id="game-board"></div>')
        html_parts.append('</div>')
        html_parts.append('<div class="result-modal" id="result-modal">')
        html_parts.append('<div class="result-content">')
        html_parts.append('<div class="stars" id="stars"></div>')
        html_parts.append('<h2 id="result-title">🎉 恭喜通关!</h2>')
        html_parts.append('<div class="score" id="final-score"></div>')
        html_parts.append('<p id="result-text"></p>')
        html_parts.append('<button class="btn" onclick="resetGame()">再玩一次</button>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append(f'const cards = {json.dumps(cards)};')
        html_parts.append('let gameBoard = document.getElementById("game-board");')
        html_parts.append('let flippedCards = [];')
        html_parts.append('let matchedPairs = 0;')
        html_parts.append('let moves = 0;')
        html_parts.append('let gameActive = true;')
        html_parts.append('let startTime = Date.now();')
        html_parts.append('let timerInterval;')
        html_parts.append('function updateTimer() { document.getElementById("timer").textContent = Math.floor((Date.now() - startTime) / 1000); }')
        html_parts.append('function initGame() {')
        html_parts.append('flippedCards = [];')
        html_parts.append('matchedPairs = 0;')
        html_parts.append('moves = 0;')
        html_parts.append('gameActive = true;')
        html_parts.append('startTime = Date.now();')
        html_parts.append('document.getElementById("pairs").textContent = "0";')
        html_parts.append('document.getElementById("moves").textContent = "0";')
        html_parts.append('gameBoard.innerHTML = "";')
        html_parts.append('let gameCards = [...cards, ...cards];')
        html_parts.append('gameCards.sort(() => Math.random() - 0.5);')
        html_parts.append('gameCards.forEach((card, index) => {')
        html_parts.append('const cardEl = document.createElement("div");')
        html_parts.append('cardEl.className = "card";')
        html_parts.append('cardEl.innerHTML = `<div class="card-inner"><div class="card-front">🎴</div><div class="card-back">${card}</div></div>`;')
        html_parts.append('cardEl.dataset.index = index;')
        html_parts.append('cardEl.dataset.value = card;')
        html_parts.append('cardEl.addEventListener("click", flipCard);')
        html_parts.append('gameBoard.appendChild(cardEl);')
        html_parts.append('}); }')
        html_parts.append('function flipCard() {')
        html_parts.append('if (!gameActive || this.classList.contains("flipped") || this.classList.contains("matched")) return;')
        html_parts.append('this.classList.add("flipped");')
        html_parts.append('flippedCards.push(this);')
        html_parts.append('if (flippedCards.length === 2) {')
        html_parts.append('moves++;')
        html_parts.append('document.getElementById("moves").textContent = moves;')
        html_parts.append('if (flippedCards[0].dataset.value === flippedCards[1].dataset.value) {')
        html_parts.append('flippedCards.forEach(card => card.classList.add("matched"));')
        html_parts.append('matchedPairs++;')
        html_parts.append('document.getElementById("pairs").textContent = matchedPairs;')
        html_parts.append('flippedCards = [];')
        html_parts.append('if (matchedPairs === cards.length) { gameActive = false; clearInterval(timerInterval); setTimeout(showResult, 500); }')
        html_parts.append('} else {')
        html_parts.append('gameActive = false;')
        html_parts.append('setTimeout(() => { flippedCards.forEach(card => card.classList.remove("flipped")); flippedCards = []; gameActive = true; }, 1000);')
        html_parts.append('} } }')
        html_parts.append('function showResult() { const elapsed = Math.floor((Date.now() - startTime) / 1000); const pct = Math.max(0, 100 - moves * 2); let stars = ""; for (let i = 0; i < 3; i++) stars += pct >= (i + 1) * 30 ? "⭐" : "☆"; document.getElementById("stars").textContent = stars; document.getElementById("final-score").textContent = moves + "步"; document.getElementById("result-text").textContent = "用时" + elapsed + "秒"; document.getElementById("result-modal").classList.add("show"); }')
        html_parts.append('function resetGame() { document.getElementById("result-modal").classList.remove("show"); initGame(); timerInterval = setInterval(updateTimer, 1000); }')
        html_parts.append('timerInterval = setInterval(updateTimer, 1000);')
        html_parts.append('initGame();')
        html_parts.append('</script>')
        html_parts.append('</body>')
        html_parts.append('</html>')

        return ''.join(html_parts)
    
    def _generate_matching_game(self, topic: str, content: list):
        """生成匹配游戏"""
        pairs = []
        for item in content:
            if isinstance(item, dict) and 'title' in item and 'content' in item:
                for subitem in item['content']:
                    pairs.append({
                        'left': item['title'],
                        'right': subitem
                    })

        import random
        shuffled_rights = [p['right'] for p in pairs]
        random.shuffle(shuffled_rights)

        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN">')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'<title>{topic} - 匹配游戏</title>')
        html_parts.append('<style>')
        html_parts.append('* { box-sizing: border-box; margin: 0; padding: 0; }')
        html_parts.append('body { font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }')
        html_parts.append('.container { max-width: 1000px; margin: 0 auto; }')
        html_parts.append('.header { text-align: center; color: white; margin-bottom: 30px; }')
        html_parts.append('.header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }')
        html_parts.append('.score-board { display: flex; justify-content: center; gap: 40px; margin-bottom: 20px; }')
        html_parts.append('.score-item { background: rgba(255,255,255,0.2); padding: 10px 25px; border-radius: 50px; color: white; font-size: 1.2em; backdrop-filter: blur(5px); }')
        html_parts.append('.game-area { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }')
        html_parts.append('.column { background: white; border-radius: 16px; padding: 25px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }')
        html_parts.append('.column-title { text-align: center; font-size: 1.4em; color: #333; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 3px solid #667eea; }')
        html_parts.append('.items-grid { display: flex; flex-direction: column; gap: 12px; }')
        html_parts.append('.item { padding: 15px 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; cursor: grab; text-align: center; font-size: 1.1em; color: #333; transition: all 0.3s ease; border: 2px solid transparent; user-select: none; }')
        html_parts.append('.item:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); border-color: #667eea; }')
        html_parts.append('.item:active { cursor: grabbing; }')
        html_parts.append('.item.dragging { opacity: 0.5; transform: scale(1.05); }')
        html_parts.append('.item.matched { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-color: #28a745; color: #155724; cursor: default; }')
        html_parts.append('.drop-zone { padding: 15px 20px; background: #f8f9fa; border: 3px dashed #dee2e6; border-radius: 10px; text-align: center; font-size: 1.1em; color: #666; transition: all 0.3s ease; min-height: 60px; display: flex; align-items: center; justify-content: center; }')
        html_parts.append('.drop-zone.dragover { border-color: #667eea; background: #e8eaf6; transform: scale(1.02); }')
        html_parts.append('.drop-zone.correct { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border: 3px solid #28a745; color: #155724; animation: pulse 0.5s ease; }')
        html_parts.append('.drop-zone.incorrect { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-color: #dc3545; animation: shake 0.5s ease; }')
        html_parts.append('@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }')
        html_parts.append('@keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-10px); } 75% { transform: translateX(10px); } }')
        html_parts.append('.result-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); justify-content: center; align-items: center; z-index: 1000; }')
        html_parts.append('.result-modal.show { display: flex; }')
        html_parts.append('.result-content { background: white; padding: 40px 60px; border-radius: 20px; text-align: center; animation: popIn 0.5s ease; }')
        html_parts.append('@keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }')
        html_parts.append('.result-content h2 { font-size: 2.5em; color: #28a745; margin-bottom: 20px; }')
        html_parts.append('.result-content p { font-size: 1.3em; color: #666; margin-bottom: 30px; }')
        html_parts.append('.btn { padding: 15px 40px; font-size: 1.2em; border: none; border-radius: 50px; cursor: pointer; transition: all 0.3s ease; }')
        html_parts.append('.btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }')
        html_parts.append('.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 5px 20px rgba(102,126,234,0.4); }')
        html_parts.append('.progress-bar { background: rgba(255,255,255,0.3); height: 8px; border-radius: 4px; margin-bottom: 30px; overflow: hidden; }')
        html_parts.append('.progress-fill { background: white; height: 100%; border-radius: 4px; transition: width 0.3s ease; }')
        html_parts.append('</style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('<div class="container">')
        html_parts.append('<div class="header">')
        html_parts.append(f'<h1>{topic}</h1>')
        html_parts.append('<p style="font-size:1.2em;opacity:0.9;">拖动左侧选项到右侧正确的位置</p>')
        html_parts.append('</div>')
        html_parts.append('<div class="progress-bar"><div class="progress-fill" id="progress"></div></div>')
        html_parts.append('<div class="score-board">')
        html_parts.append('<div class="score-item">用时: <span id="timer">0</span>秒</div>')
        html_parts.append('<div class="score-item">正确: <span id="correct-count">0</span>/<span id="total-count">' + str(len(pairs)) + '</span></div>')
        html_parts.append('<div class="score-item">错误: <span id="wrong-count">0</span></div>')
        html_parts.append('</div>')
        html_parts.append('<div class="game-area">')
        html_parts.append('<div class="column">')
        html_parts.append('<div class="column-title">🎯 请匹配</div>')
        html_parts.append('<div class="items-grid" id="left-items">')

        for i, pair in enumerate(pairs):
            html_parts.append(f'<div class="item" draggable="true" data-id="{i}" id="left-{i}">{pair["left"]}</div>')

        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="column">')
        html_parts.append('<div class="column-title">📝 拖到这里</div>')
        html_parts.append('<div class="items-grid" id="right-items">')

        for i, right_text in enumerate(shuffled_rights):
            original_index = pairs.index(next(p for p in pairs if p['right'] == right_text))
            html_parts.append(f'<div class="drop-zone" data-target="{original_index}" id="drop-{i}">{right_text}</div>')

        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<div class="result-modal" id="result-modal">')
        html_parts.append('<div class="result-content">')
        html_parts.append('<h2 id="result-title">🎉 恭喜通关!</h2>')
        html_parts.append('<p id="result-text">你完成了所有匹配!</p>')
        html_parts.append('<button class="btn btn-primary" onclick="resetGame()">再玩一次</button>')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('<script>')
        html_parts.append(f'const pairs = {json.dumps(pairs)};')
        html_parts.append('const leftItems = document.querySelectorAll(".item");')
        html_parts.append('const dropZones = document.querySelectorAll(".drop-zone");')
        html_parts.append('let correctCount = 0;')
        html_parts.append('let wrongCount = 0;')
        html_parts.append('let startTime = Date.now();')
        html_parts.append('let timerInterval;')
        html_parts.append('let draggedItem = null;')
        html_parts.append('let draggedId = null;')
        html_parts.append('function updateTimer() { document.getElementById("timer").textContent = Math.floor((Date.now() - startTime) / 1000); }')
        html_parts.append('function updateProgress() { const pct = (correctCount / pairs.length) * 100; document.getElementById("progress").style.width = pct + "%"; }')
        html_parts.append('timerInterval = setInterval(updateTimer, 1000);')
        html_parts.append('leftItems.forEach(item => {')
        html_parts.append('item.addEventListener("dragstart", function(e) { draggedItem = this; draggedId = this.dataset.id; this.classList.add("dragging"); e.dataTransfer.effectAllowed = "move"; });')
        html_parts.append('item.addEventListener("dragend", function() { this.classList.remove("dragging"); draggedItem = null; draggedId = null; });')
        html_parts.append('});')
        html_parts.append('dropZones.forEach(zone => {')
        html_parts.append('zone.addEventListener("dragover", function(e) { e.preventDefault(); this.classList.add("dragover"); });')
        html_parts.append('zone.addEventListener("dragleave", function() { this.classList.remove("dragover"); });')
        html_parts.append('zone.addEventListener("drop", function(e) {')
        html_parts.append('e.preventDefault();')
        html_parts.append('this.classList.remove("dragover");')
        html_parts.append('if (this.classList.contains("correct")) return;')
        html_parts.append('const targetId = this.dataset.target;')
        html_parts.append('if (draggedId === targetId) {')
        html_parts.append('this.classList.add("correct");')
        html_parts.append('document.getElementById("left-" + draggedId).classList.add("matched");')
        html_parts.append('document.getElementById("left-" + draggedId).draggable = false;')
        html_parts.append('correctCount++;')
        html_parts.append('document.getElementById("correct-count").textContent = correctCount;')
        html_parts.append('updateProgress();')
        html_parts.append('if (correctCount === pairs.length) { clearInterval(timerInterval); setTimeout(showResult, 500); }')
        html_parts.append('} else {')
        html_parts.append('this.classList.add("incorrect");')
        html_parts.append('wrongCount++;')
        html_parts.append('document.getElementById("wrong-count").textContent = wrongCount;')
        html_parts.append('setTimeout(() => this.classList.remove("incorrect"), 800);')
        html_parts.append('} }); });')
        html_parts.append('function showResult() { const elapsed = Math.floor((Date.now() - startTime) / 1000); document.getElementById("result-text").textContent = "用时" + elapsed + "秒，错误" + wrongCount + "次"; document.getElementById("result-modal").classList.add("show"); }')
        html_parts.append('function resetGame() { location.reload(); }')
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
def generate_game_with_ai(self, topic: str, game_type: str = "quiz", requirements: str = None, output_filename: str = None):
    """
    使用AI生成完整游戏
    
    Args:
        topic: 游戏主题
        game_type: 游戏类型，支持 quiz（问答游戏）、memory（记忆游戏）、matching（匹配游戏）
        requirements: 自定义要求
        output_filename: 输出文件名
        
    Returns:
        str: 生成的游戏文件路径
    """
    # 使用AI生成游戏内容
    content = self._generate_game_content_with_ai(topic, game_type, requirements)
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

def _generate_game_content_with_ai(self, topic: str, game_type: str, requirements: str = None):
    """
    使用AI生成游戏内容
    
    Args:
        topic: 游戏主题
        game_type: 游戏类型
        requirements: 自定义要求
        
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

    if requirements:
        prompt += f"\n用户特殊要求：{requirements}"

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
