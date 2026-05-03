from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import json, tempfile, os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

POSITIONS = ["Няня", "Охоронець", "Менеджер", "Бухгалтер", "Продавець", "Водій", "Адміністратор", "Інше"]

MODES = {
    "fast": {"name": "Швидкий (5 хв)", "questions": 7, "desc": "5-6 ключових метапрограм"},
    "medium": {"name": "Середній (15 хв)", "questions": 17, "desc": "10-12 метапрограм"},
    "deep": {"name": "Глибокий (30 хв)", "questions": 34, "desc": "17 метапрограм як в літературі"}
}

QUESTIONS_FAST = [
    "Розкажіть про себе і чому ви обрали цю професію?",
    "Що для вас найважливіше в роботі?",
    "Як ви розумієте, що добре впорались зі своєю роботою?",
    "Розкажіть про найкращий досвід у вашій роботі.",
    "Як ви дієте коли щось пішло не за планом?",
    "Як ви ставитесь до критики від керівництва?",
    "Що мотивує вас у роботі?"
]

QUESTIONS_MEDIUM = [
    "Чого ви найбільше хочете від своєї роботи?",
    "Що найважливіше в роботі для вас?",
    "Що спонукало вас обрати саме цю професію?",
    "Що найбільше турбує вас або чого хочете уникнути в роботі?",
    "Як ви розумієте, що добре впорались зі своєю роботою?",
    "Хто або що є для вас головним орієнтиром в роботі?",
    "Розкажіть про найкращий досвід у роботі.",
    "Коли плануєте справи, починаєте з загальної картини чи з конкретних кроків?",
    "Коли перед вами стоїть нове завдання, як зазвичай дієте?",
    "Якщо щось пішло не за планом, що робите першим?",
    "Ви любите чіткі інструкції чи надаєте перевагу свободі дій?",
    "Як плануєте свій робочий день?",
    "Найважчий момент у роботі — що відбувалось?",
    "Що робите при сильному роздратуванні або втомі?",
    "Як оцінюєте себе як спеціаліста порівняно з іншими?",
    "Як ставитесь до змін у житті?",
    "На який термін плануєте своє життя?"
]

QUESTIONS_DEEP = QUESTIONS_MEDIUM + [
    "Якщо керівник незадоволений вашою роботою, а ви вважаєте, що зробили правильно, як реагуєте?",
    "Що найважливіше: загальний результат чи виконання конкретних щоденних завдань?",
    "Порівняйте нинішню роботу з попередньою, що помічаєте в першу чергу?",
    "Коли приходите на нове місце, що першим кидається в очі?",
    "Ви берете ініціативу самі чи чекаєте вказівок?",
    "Що більше приваблює — нові підходи чи перевірені методи?",
    "Якщо керівник не дав чітких інструкцій, як дієте?",
    "Чи легко вам дотримуватись розкладу та домовленостей?",
    "Ви зосереджені на тому, що відбувається зараз, чи думаєте про майбутнє?",
    "Після важкого дня ви думаєте про справи чи про себе?",
    "Що важливіше — щоб вам було комфортно чи щоб справа була зроблена?",
    "Що відрізняє вас від інших спеціалістів?",
    "До чого прагнете в професійному розвитку?",
    "Як справляєтесь, коли все йде не так і нічого не допомагає?",
    "Вам комфортніше працювати самостійно чи в команді?",
    "Як ставитесь до того, коли керівник часто перевіряє роботу?",
    "Опишіть ідеальні стосунки з колегами і керівництвом."
]

QUESTIONS = {
    "fast": QUESTIONS_FAST,
    "medium": QUESTIONS_MEDIUM,
    "deep": QUESTIONS_DEEP
}

SYSTEM_PROMPT_FAST = """Ти експерт з НЛП та метапрограмного аналізу. Зроби звіт у форматі ПРОТОКОЛУ.

ФОРМАТ для кожного блоку (6 блоків):
БЛОК N. НАЗВА МЕТАПРОГРАМИ
Питання: [питання з інтерв'ю]
Відповідь: "[цитата відповіді]"
Аналіз: [2-3 речення — який тип метапрограми, що це означає]

6 БЛОКІВ:
БЛОК 1. МОТИВАЦІЯ (До / Від)
БЛОК 2. РЕФЕРЕНЦІЯ (Внутрішня / Зовнішня)
БЛОК 3. ПРОАКТИВНІСТЬ / РЕАКТИВНІСТЬ
БЛОК 4. МОЖЛИВОСТІ / ПРОЦЕДУРИ
БЛОК 5. МАСШТАБ (Глобальний / Деталізований)
БЛОК 6. УПРАВЛІННЯ СТРЕСОМ

В КІНЦІ ЗВІТУ:

ВИСНОВОК
[3-4 речення про загальне враження]

СИЛЬНІ СТОРОНИ
1. [пункт]
2. [пункт]
3. [пункт]

НА ЩО ЗВЕРНУТИ УВАГУ
1. [пункт]
2. [пункт]
3. [пункт]

РЕКОМЕНДАЦІЯ
[1-2 речення: підходить/частково/не підходить + кому підходить]"""

SYSTEM_PROMPT_MEDIUM = """Ти експерт з НЛП та метапрограмного аналізу. Зроби детальний звіт у форматі ПРОТОКОЛУ як у класичній літературі.

ФОРМАТ для кожного блоку:
БЛОК N. НАЗВА МЕТАПРОГРАМИ
Питання: [питання]
Відповідь: "[цитата]"
[якщо в блоці кілька питань — додай їх]
Аналіз: [3-4 речення — детальний розбір метапрограми]

12 БЛОКІВ:
БЛОК 1. МОТИВАЦІЯ (До / Від)
БЛОК 2. РЕФЕРЕНЦІЯ (Внутрішня / Зовнішня)
БЛОК 3. МАСШТАБ МИСЛЕННЯ (Глобальний / Деталізований)
БЛОК 4. ПРОАКТИВНІСТЬ / РЕАКТИВНІСТЬ
БЛОК 5. МОЖЛИВОСТІ / ПРОЦЕДУРИ
БЛОК 6. ЧАСОВА ОРІЄНТАЦІЯ
БЛОК 7. ФОКУС УВАГИ (Я / Інші)
БЛОК 8. УПРАВЛІННЯ СТРЕСОМ
БЛОК 9. СТИЛЬ РОБОТИ
БЛОК 10. СТАВЛЕННЯ ДО ЗМІН
БЛОК 11. СТАВЛЕННЯ ДО ПРАВИЛ
БЛОК 12. СТИЛЬ ПОРІВНЯННЯ

В КІНЦІ ЗВІТУ:

ВИСНОВОК
Загальне враження (4-5 речень)

СИЛЬНІ СТОРОНИ
1-5 пунктів з поясненням

НА ЩО ЗВЕРНУТИ УВАГУ
1-5 пунктів з поясненням і рекомендаціями

РЕКОМЕНДАЦІЯ ЩОДО СУМІСНОСТІ
Кому підходить, кому ні, що врахувати при онбордингу."""

SYSTEM_PROMPT_DEEP = """Ти експерт з НЛП та метапрограмного аналізу. Зроби максимально глибокий професійний звіт у форматі ПРОТОКОЛУ як у класичній літературі (Шелле, Холл, Вудсмолл).

ФОРМАТ для кожного блоку:
БЛОК N. НАЗВА МЕТАПРОГРАМИ
Питання: [питання 1]
Відповідь: "[цитата]"
Питання: [питання 2 якщо є]
Відповідь: "[цитата]"
Аналіз: [4-6 речень — глибокий професійний розбір]

17 ОБОВ'ЯЗКОВИХ БЛОКІВ:
БЛОК 1. МОТИВАЦІЯ (До / Від)
БЛОК 2. РЕФЕРЕНЦІЯ (Внутрішня / Зовнішня)
БЛОК 3. МАСШТАБ МИСЛЕННЯ (Глобальний / Деталізований)
БЛОК 4. СХОЖІСТЬ / ВІДМІННІСТЬ
БЛОК 5. ПРОАКТИВНІСТЬ / РЕАКТИВНІСТЬ
БЛОК 6. МОЖЛИВОСТІ / ПРОЦЕДУРИ
БЛОК 7. ЧАСОВА ОРІЄНТАЦІЯ (В часі / Крізь час)
БЛОК 8. ФОКУС УВАГИ (На себе / На інших)
БЛОК 9. ПЕРЕКОНАННЯ (мова вибору / зобов'язання)
БЛОК 10. СТИЛЬ ПОРІВНЯННЯ
БЛОК 11. УПРАВЛІННЯ СТРЕСОМ
БЛОК 12. СТИЛЬ РОБОТИ
БЛОК 13. ОРГАНІЗАЦІЯ ІНФОРМАЦІЇ
БЛОК 14. СТАВЛЕННЯ ДО ЗМІН
БЛОК 15. СТАВЛЕННЯ ДО ПРАВИЛ
БЛОК 16. МОДАЛЬНОСТІ (Візуал/Аудіал/Кінестетик/Дигітал)
БЛОК 17. ЧАСОВИЙ ГОРИЗОНТ ПЛАНУВАННЯ

В КІНЦІ ЗВІТУ ОБОВ'ЯЗКОВО:

ВИСНОВОК
Загальне враження (5-7 речень — глибокий аналіз особистості)

СИЛЬНІ СТОРОНИ (5 пунктів з детальним поясненням)
1. [сильна сторона]: [розгорнуте пояснення 2-3 речення]
...

НА ЩО ЗВЕРНУТИ УВАГУ (5 пунктів)
1. [спостереження]: [пояснення + рекомендація]
...

РЕКОМЕНДАЦІЯ ЩОДО СУМІСНОСТІ
Кандидат підходить для:
- [тип компанії/керівника/команди]
- ...

Кандидат НЕ підходить для:
- ...

При онбордингу врахувати:
- ...

Звіт має бути на рівні професійного HR-психолога."""

PROMPTS = {
    "fast": SYSTEM_PROMPT_FAST,
    "medium": SYSTEM_PROMPT_MEDIUM,
    "deep": SYSTEM_PROMPT_DEEP
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Профайлер кандидатів</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh}
.header{background:#2c3e50;color:white;padding:20px;text-align:center}
.header h1{font-size:26px}
.container{max-width:850px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:12px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;transition:all 0.2s;text-align:center}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.question-block{display:none}
.question-block.active{display:block}
.question-num{font-size:13px;color:#888;margin-bottom:6px}
.question-text{font-size:18px;font-weight:bold;color:#2c3e50;margin-bottom:14px}
.answer-area{min-height:90px;background:#f8f9fa;margin-bottom:12px;resize:vertical}
.btn-row{display:flex;gap:10px;flex-wrap:wrap}
.record-btn{background:#e74c3c;color:white;border:none;padding:11px 18px;border-radius:8px;font-size:14px;cursor:pointer}
.record-btn.recording{background:#c0392b;animation:pulse 1s infinite}
.record-btn.done{background:#27ae60}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.6}}
.nav-btn{background:#3498db;color:white;border:none;padding:11px 22px;border-radius:8px;font-size:15px;cursor:pointer}
.nav-btn:disabled{background:#bdc3c7;cursor:not-allowed}
.analyze-btn{background:#27ae60;color:white;border:none;padding:16px;border-radius:10px;font-size:17px;cursor:pointer;width:100%;display:none;margin-top:8px}
.progress{background:#ecf0f1;border-radius:10px;height:8px;margin:10px 0}
.progress-bar{background:#3498db;height:8px;border-radius:10px;transition:width 0.3s}
#result{background:white;border-radius:12px;padding:25px;margin-top:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08);white-space:pre-wrap;display:none;line-height:1.65;font-size:14px}
#loading{text-align:center;padding:30px;display:none;font-size:17px;color:#666}
.start-btn{background:#2c3e50;color:white;border:none;padding:14px 28px;border-radius:10px;font-size:16px;cursor:pointer;width:100%;margin-top:8px}
#setup{display:block}
#quiz{display:none}
.hint{font-size:12px;color:#999;margin-top:5px}
.cost{font-size:11px;color:#999;text-align:center;margin-top:8px}
</style>
</head>
<body>
<div class="header"><h1>🔍 Профайлер кандидатів</h1></div>
<div class="container">
<div id="setup">
<div class="card">
<label>Імя кандидата:</label>
<input type="text" id="candidate_name" placeholder="Введіть імя...">
</div>
<div class="card">
<label>Посада:</label>
<select id="position_select">
<option value="">-- Оберіть посаду --</option>
{% for pos in positions %}<option value="{{ pos }}">{{ pos }}</option>{% endfor %}
</select>
</div>
<div class="card">
<label>Формат тестування:</label>
<div class="modes">
<div class="mode-card" data-mode="fast" onclick="selectMode('fast')">
<div class="mode-name">⚡ Швидкий</div>
<div class="mode-desc">7 питань<br>~5 хв<br>6 метапрограм</div>
</div>
<div class="mode-card selected" data-mode="medium" onclick="selectMode('medium')">
<div class="mode-name">📊 Середній</div>
<div class="mode-desc">17 питань<br>~15 хв<br>12 метапрограм</div>
</div>
<div class="mode-card" data-mode="deep" onclick="selectMode('deep')">
<div class="mode-name">🧠 Глибокий</div>
<div class="mode-desc">34 питання<br>~30 хв<br>17 метапрограм</div>
</div>
</div>
</div>
<button class="start-btn" onclick="startQuiz()">▶ Розпочати тестування</button>
</div>
<div id="quiz">
<div class="card" style="background:#fff8e1;border-left:4px solid #f39c12">
<div style="font-size:14px;color:#7d4f00;line-height:1.5"><strong>📢 Інструкція:</strong> говоріть <strong>голосно і повільно</strong>. Після запису перевірте текст і відредагуйте якщо бачите помилки розпізнавання.</div>
</div>
<div class="card">
<div style="display:flex;justify-content:space-between;align-items:center">
<span id="progress_text" style="color:#888"></span>
<span id="candidate_display" style="font-weight:bold"></span>
</div>
<div class="progress"><div class="progress-bar" id="progress_bar"></div></div>
</div>
<div class="card" id="questions_container"></div>
<div style="display:flex;gap:10px;margin-bottom:18px">
<button class="nav-btn" id="prev_btn" onclick="prevQuestion()" disabled>← Назад</button>
<button class="nav-btn" id="next_btn" onclick="nextQuestion()">Далі →</button>
</div>
<button class="analyze-btn" id="analyze_btn" onclick="doAnalyze()">🧠 Проаналізувати</button>
</div>
<div id="loading">⏳ Аналізую відповіді... зачекайте 20-40 секунд</div>
<div id="result"></div>
</div>
<script>
const QUESTIONS = {{ questions_json|safe }};
let current = 0;
let answers = [];
let mediaRecorder = null;
let audioChunks = [];
let currentMode = "medium";

function selectMode(mode){
  currentMode = mode;
  document.querySelectorAll('.mode-card').forEach(c=>c.classList.remove('selected'));
  document.querySelector('.mode-card[data-mode="'+mode+'"]').classList.add('selected');
}

function startQuiz(){
  const name = document.getElementById("candidate_name").value.trim();
  const pos = document.getElementById("position_select").value;
  if(!name){alert("Введіть імя кандидата");return}
  if(!pos){alert("Оберіть посаду");return}
  const qs = QUESTIONS[currentMode];
  answers = new Array(qs.length).fill("");
  document.getElementById("candidate_display").textContent = name+" — "+pos;
  document.getElementById("setup").style.display="none";
  document.getElementById("quiz").style.display="block";
  buildQuestions(qs);
  showQuestion(0);
}

function buildQuestions(qs){
  const c = document.getElementById("questions_container");
  c.innerHTML="";
  qs.forEach((q,i)=>{
    const d = document.createElement("div");
    d.className="question-block";d.id="q_"+i;
    d.innerHTML='<div class="question-num">Питання '+(i+1)+' з '+qs.length+'</div>'+
      '<div class="question-text">'+q+'</div>'+
      '<textarea class="answer-area" id="answer_'+i+'" placeholder="Натисніть кнопку запису або введіть вручну..."></textarea>'+
      '<p class="hint" style="color:#e67e22;font-size:13px;font-weight:bold;margin-bottom:8px">🎤 Говоріть голосно і повільно. Редагуйте відповіді якщо бачите помилки розпізнавання.</p>'+
      '<div class="btn-row">'+
        '<button class="record-btn" id="rec_'+i+'" onclick="toggleRecord('+i+')">🎤 Записати</button>'+
      '</div>';
    c.appendChild(d);
  });
}

function showQuestion(idx){
  const qs = QUESTIONS[currentMode];
  document.querySelectorAll(".question-block").forEach(b=>b.classList.remove("active"));
  document.getElementById("q_"+idx).classList.add("active");
  document.getElementById("progress_text").textContent="Питання "+(idx+1)+" з "+qs.length;
  document.getElementById("progress_bar").style.width=((idx+1)/qs.length*100)+"%";
  document.getElementById("prev_btn").disabled=idx===0;
  document.getElementById("next_btn").style.display=idx===qs.length-1?"none":"inline-block";
  document.getElementById("analyze_btn").style.display=idx===qs.length-1?"block":"none";
  current=idx;
}

function nextQuestion(){if(current<QUESTIONS[currentMode].length-1)showQuestion(current+1)}
function prevQuestion(){if(current>0)showQuestion(current-1)}

async function toggleRecord(idx){
  const btn = document.getElementById("rec_"+idx);
  if(mediaRecorder && mediaRecorder.state==="recording"){
    mediaRecorder.stop();
    btn.textContent="⏳ Обробка...";
    btn.className="record-btn done";
    return;
  }
  try{
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});
    audioChunks=[];
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e=>audioChunks.push(e.data);
    mediaRecorder.onstop = async ()=>{
      stream.getTracks().forEach(t=>t.stop());
      const blob = new Blob(audioChunks,{type:"audio/webm"});
      const fd = new FormData();
      fd.append("audio",blob,"r.webm");
      try{
        const r = await fetch("/transcribe",{method:"POST",body:fd});
        const d = await r.json();
        if(d.text && d.text.trim().length>0){
          document.getElementById("answer_"+idx).value = d.text;
          answers[idx]=d.text;
          btn.textContent="✓ Записано (натисніть для перезапису)";
          btn.className="record-btn done";
        }else{
          btn.textContent="🎤 Записати";
          btn.className="record-btn";
          alert("Не вдалось розпізнати: "+(d.error||"спробуйте ще")+". Або введіть вручну.");
        }
      }catch(e){
        btn.textContent="🎤 Записати";
        btn.className="record-btn";
        alert("Помилка: "+e.message);
      }
    };
    mediaRecorder.start();
    btn.textContent="⏹ Зупинити запис";
    btn.className="record-btn recording";
  }catch(e){
    alert("Помилка доступу до мікрофону: "+e.message);
  }
}

async function doAnalyze(){
  const name = document.getElementById("candidate_name").value;
  const pos = document.getElementById("position_select").value;
  QUESTIONS[currentMode].forEach((q,i)=>{
    const el = document.getElementById("answer_"+i);
    if(el)answers[i]=el.value||"";
  });
  document.getElementById("quiz").style.display="none";
  document.getElementById("loading").style.display="block";
  try{
    const r = await fetch("/run_analyze",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({name,position:pos,mode:currentMode,answers,questions:QUESTIONS[currentMode]})
    });
    const d = await r.json();
    document.getElementById("loading").style.display="none";
    document.getElementById("result").style.display="block";
    document.getElementById("result").textContent=d.result||"Помилка: "+d.error;
  }catch(e){
    document.getElementById("loading").style.display="none";
    document.getElementById("result").style.display="block";
    document.getElementById("result").textContent="Помилка: "+e.message;
  }
}
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE, positions=POSITIONS, questions_json=json.dumps(QUESTIONS, ensure_ascii=False))

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name
        try:
            with open(tmp_path, 'rb') as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language="uk"
                )
            return jsonify({"text": transcript.text})
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        return jsonify({"text": "", "error": str(e)})

@app.route('/run_analyze', methods=['POST'])
def run_analyze():
    try:
        data = request.json
        name = data.get('name', 'Кандидат')
        position = data.get('position', '')
        mode = data.get('mode', 'medium')
        answers = data.get('answers', [])
        questions = data.get('questions', [])
        conversation = "Кандидат: " + name + "\nПосада: " + position + "\n\n"
        for q, a in zip(questions, answers):
            if a.strip():
                conversation += "Питання: " + q + "\nВідповідь: " + a + "\n\n"
        prompt = PROMPTS.get(mode, SYSTEM_PROMPT_MEDIUM)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": conversation}
            ],
            temperature=0.3
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"result": "", "error": str(e)})

if __name__ == '__main__':
    print("Профайлер запущено!")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
