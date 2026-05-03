from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import json, tempfile, os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

POSITIONS = {
    "Няня": [
        "Розкажіть, чому ви хочете працювати нянею?",
        "Як ви зазвичай реагуєте, коли дитина не слухається?",
        "Розкажіть про ситуацію, коли щось пішло не так у вашій роботі. Як ви діяли?",
        "Що для вас найважливіше в роботі з дітьми?",
        "Як ви плануєте свій день з дитиною?",
        "Що робите якщо батьки дають вам інструкції які вам не подобаються?",
        "Розкажіть про свій найкращий досвід роботи з дитиною.",
        "Як ви реагуєте на критику від роботодавця?",
        "Що мотивує вас у цій роботі?",
        "Як ви діяте в стресових ситуаціях?"
    ],
    "Охоронець": [
        "Чому ви хочете працювати охоронцем?",
        "Як ви реагуєте коли хтось порушує правила?",
        "Розкажіть про конфліктну ситуацію яку вам довелось вирішувати.",
        "Що для вас важливіше — суворо дотримуватись інструкцій чи діяти за ситуацією?",
        "Як ви поводитесь у стресових або небезпечних ситуаціях?",
        "Як ставитесь до нічних змін і монотонної роботи?",
        "Що робите якщо начальник дає наказ з яким ви не згодні?",
        "Розкажіть про свій досвід роботи з людьми.",
        "Що для вас означає відповідальність?",
        "Як ви ставитесь до правил і регламентів?"
    ],
    "Менеджер": [
        "Чому ви хочете займати керівну посаду?",
        "Як ви приймаєте складні рішення?",
        "Розкажіть про ситуацію коли ваша команда не виконала план. Що ви зробили?",
        "Як ви мотивуєте підлеглих?",
        "Як ви розставляєте пріоритети коли задач багато?",
        "Як реагуєте на критику зверху?",
        "Що для вас важливіше — результат чи процес?",
        "Як ви справляєтесь з конфліктами в команді?",
        "Що вас мотивує в роботі?",
        "Як ви ставитесь до змін і нових підходів?"
    ],
    "Бухгалтер": [
        "Чому ви обрали професію бухгалтера?",
        "Як ви реагуєте коли знаходите помилку в документах?",
        "Розкажіть про складну ситуацію в роботі з цифрами чи звітністю.",
        "Як ви організовуєте свою роботу в період звітності?",
        "Що для вас важливіше — швидкість чи точність?",
        "Як ставитесь до змін у законодавстві?",
        "Як реагуєте коли керівник просить зробити щось що вам здається неправильним?",
        "Що вас мотивує в цій роботі?",
        "Як ви справляєтесь зі стресом в напружені періоди?",
        "Як ви ставитесь до монотонної рутинної роботи?"
    ]
}

SYSTEM_PROMPT = """Ти експерт з НЛП та метапрограм. Проаналізуй відповіді кандидата та визнач його метапрограми.

Проаналізуй такі метапрограми:
1. Мотивація: ДО (рухається до цілей) або ВІД (уникає проблем)
2. Референція: ВНУТРІШНЯ (сама вирішує) або ЗОВНІШНЯ (потребує схвалення)
3. Орієнтація: ЛЮДИ або ЗАВДАННЯ або ПРОЦЕС
4. Стиль роботи: ПРОАКТИВНИЙ або РЕАКТИВНИЙ
5. Підхід: ПРОЦЕДУРНИЙ (інструкції) або ВАРІАТИВНИЙ (творчість)
6. Масштаб: ГЛОБАЛЬНИЙ або ДЕТАЛЬНИЙ
7. Стрес: СТІЙКИЙ або ЧУТЛИВИЙ

Для кожної метапрограми:
- Вкажи визначений тип
- Наведи цитату з відповідей яка це підтверджує
- Дай оцінку впевненості: висока/середня/низька

В кінці дай:
ЗАГАЛЬНИЙ ВИСНОВОК: чи підходить кандидат на посаду (так/частково/ні) і чому
РИЗИКИ: що може бути проблемою
РЕКОМЕНДАЦІЇ: на що звернути увагу"""

HTML_PAGE = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Профайлер кандидатів</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; min-height: 100vh; }
        .header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
        .header h1 { font-size: 28px; }
        .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .card { background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        label { font-weight: bold; display: block; margin-bottom: 8px; color: #333; }
        input[type=text] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 15px; }
        select { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 15px; background: white; }
        .question-block { background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: none; }
        .question-block.active { display: block; }
        .question-num { font-size: 13px; color: #888; margin-bottom: 5px; }
        .question-text { font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 15px; }
        .answer-area { width: 100%; min-height: 80px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 8px; padding: 15px; background: #f8f9fa; margin-bottom: 15px; resize: vertical; font-family: Arial, sans-serif; }
        .btn-row { display: flex; gap: 10px; flex-wrap: wrap; }
        .record-btn { background: #e74c3c; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 14px; cursor: pointer; }
        .record-btn.recording { background: #c0392b; animation: pulse 1s infinite; }
        .record-btn.done { background: #27ae60; }
        .retry-btn { background: #f39c12; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 14px; cursor: pointer; display: none; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
        .nav-btn { background: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-size: 15px; cursor: pointer; }
        .nav-btn:disabled { background: #bdc3c7; cursor: not-allowed; }
        .analyze-btn { background: #27ae60; color: white; border: none; padding: 18px; border-radius: 10px; font-size: 18px; cursor: pointer; width: 100%; display: none; margin-top: 10px; }
        .progress { background: #ecf0f1; border-radius: 10px; height: 8px; margin: 10px 0; }
        .progress-bar { background: #3498db; height: 8px; border-radius: 10px; transition: width 0.3s; }
        #result { background: white; border-radius: 12px; padding: 25px; margin-top: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); white-space: pre-wrap; display: none; line-height: 1.6; }
        #loading { text-align: center; padding: 30px; display: none; font-size: 18px; color: #666; }
        .start-btn { background: #2c3e50; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 17px; cursor: pointer; width: 100%; margin-top: 10px; }
        #setup { display: block; }
        #quiz { display: none; }
        .hint { font-size: 12px; color: #999; margin-top: 5px; margin-bottom: 10px; }
    </style>
</head>
<body>
<div class="header"><h1>&#128269; Профайлер кандидатів</h1></div>
<div class="container">
<div id="setup">
    <div class="card">
        <label>Імя кандидата:</label>
        <input type="text" id="candidate_name" placeholder="Введіть імя...">
    </div>
    <div class="card">
        <label>Посада:</label>
        <select id="position_select" onchange="loadQuestions()">
            <option value="">-- Оберіть посаду --</option>
            {% for pos in positions %}
            <option value="{{ pos }}">{{ pos }}</option>
            {% endfor %}
        </select>
    </div>
    <button class="start-btn" onclick="startQuiz()">&#9654; Розпочати тестування</button>
</div>
<div id="quiz">
    <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span id="progress_text" style="color:#888;">Питання 1 з 10</span>
            <span id="candidate_display" style="font-weight:bold;"></span>
        </div>
        <div class="progress"><div class="progress-bar" id="progress_bar" style="width:10%"></div></div>
    </div>
    <div id="questions_container"></div>
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button class="nav-btn" id="prev_btn" onclick="prevQuestion()" disabled>&#8592; Назад</button>
        <button class="nav-btn" id="next_btn" onclick="nextQuestion()">Далі &#8594;</button>
    </div>
    <button class="analyze-btn" id="analyze_btn" onclick="doAnalyze()">&#129504; Проаналізувати</button>
</div>
<div id="loading">&#9203; Аналізую відповіді... зачекайте 15-20 секунд</div>
<div id="result"></div>
</div>
<script>
const QUESTIONS = {{ questions_json|safe }};
let current = 0;
let answers = [];
let mediaRecorder = null;
let audioChunks = [];
let currentPosition = "";

function loadQuestions() {
    currentPosition = document.getElementById("position_select").value;
}

function startQuiz() {
    const name = document.getElementById("candidate_name").value.trim();
    if (!name) { alert("Введіть імя кандидата"); return; }
    if (!currentPosition) { alert("Оберіть посаду"); return; }
    const qs = QUESTIONS[currentPosition];
    answers = new Array(qs.length).fill("");
    document.getElementById("candidate_display").textContent = name;
    document.getElementById("setup").style.display = "none";
    document.getElementById("quiz").style.display = "block";
    buildQuestions(qs);
    showQuestion(0);
}

function buildQuestions(qs) {
    const container = document.getElementById("questions_container");
    container.innerHTML = "";
    qs.forEach((q, i) => {
        const div = document.createElement("div");
        div.className = "question-block";
        div.id = "q_" + i;
        div.innerHTML =
            '<div class="question-num">Питання ' + (i+1) + ' з ' + qs.length + '</div>' +
            '<div class="question-text">' + q + '</div>' +
            '<textarea class="answer-area" id="answer_' + i + '" placeholder="Натисніть кнопку запису або введіть відповідь вручну..."></textarea>' +
            '<p class="hint">&#9998; Текст можна редагувати вручну після запису</p>' +
            '<div class="btn-row">' +
            '<button class="record-btn" id="rec_' + i + '" onclick="toggleRecord(' + i + ')">&#127908; Записати відповідь</button>' +
            '<button class="retry-btn" id="retry_' + i + '" onclick="retryRecord(' + i + ')">&#128260; Записати ще раз</button>' +
            '</div>';
        container.appendChild(div);
    });
}

function showQuestion(idx) {
    const qs = QUESTIONS[currentPosition];
    document.querySelectorAll(".question-block").forEach(b => b.classList.remove("active"));
    document.getElementById("q_" + idx).classList.add("active");
    document.getElementById("progress_text").textContent = "Питання " + (idx+1) + " з " + qs.length;
    document.getElementById("progress_bar").style.width = ((idx+1)/qs.length*100) + "%";
    document.getElementById("prev_btn").disabled = idx === 0;
    document.getElementById("next_btn").style.display = idx === qs.length-1 ? "none" : "inline-block";
    document.getElementById("analyze_btn").style.display = idx === qs.length-1 ? "block" : "none";
    current = idx;
}

function nextQuestion() { if (current < QUESTIONS[currentPosition].length-1) showQuestion(current+1); }
function prevQuestion() { if (current > 0) showQuestion(current-1); }

function retryRecord(idx) {
    document.getElementById("answer_" + idx).value = "";
    document.getElementById("rec_" + idx).textContent = "&#127908; Записати відповідь";
    document.getElementById("rec_" + idx).className = "record-btn";
    document.getElementById("retry_" + idx).style.display = "none";
    answers[idx] = "";
}

async function toggleRecord(idx) {
    const btn = document.getElementById("rec_" + idx);
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        btn.textContent = "Обробка...";
        btn.className = "record-btn done";
        return;
    }
    try {
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        audioChunks = [];
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = async () => {
            stream.getTracks().forEach(t => t.stop());
            const blob = new Blob(audioChunks, {type: "audio/webm"});
            const formData = new FormData();
            formData.append("audio", blob, "recording.webm");
            try {
                const resp = await fetch("/transcribe", {method: "POST", body: formData});
                const data = await resp.json();
                if (data.text && data.text.length > 0) {
                    document.getElementById("answer_" + idx).value = data.text;
                    answers[idx] = data.text;
                    btn.textContent = "Записано";
                    btn.className = "record-btn done";
                    document.getElementById("retry_" + idx).style.display = "inline-block";
                } else {
                    btn.textContent = "Записати відповідь";
                    btn.className = "record-btn";
                    alert("Не вдалось розпізнати. Спробуйте ще раз або введіть вручну.");
                }
            } catch(e) {
                btn.textContent = "Записати відповідь";
                btn.className = "record-btn";
            }
        };
        mediaRecorder.start();
        btn.textContent = "Зупинити запис";
        btn.className = "record-btn recording";
    } catch(e) {
        alert("Помилка доступу до мікрофону. Дозвольте доступ у браузері.");
    }
}

async function doAnalyze() {
    const name = document.getElementById("candidate_name").value;
    QUESTIONS[currentPosition].forEach((q, i) => {
        const el = document.getElementById("answer_" + i);
        if (el) answers[i] = el.value || "";
    });
    document.getElementById("quiz").style.display = "none";
    document.getElementById("loading").style.display = "block";
    try {
        const resp = await fetch("/run_analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name, position: currentPosition, answers, questions: QUESTIONS[currentPosition]})
        });
        const data = await resp.json();
        document.getElementById("loading").style.display = "none";
        document.getElementById("result").style.display = "block";
        document.getElementById("result").textContent = data.result;
    } catch(e) {
        document.getElementById("loading").style.display = "none";
        document.getElementById("result").style.display = "block";
        document.getElementById("result").textContent = "Помилка аналізу. Спробуйте ще раз.";
    }
}
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE,
        positions=list(POSITIONS.keys()),
        questions_json=json.dumps(POSITIONS, ensure_ascii=False))


@app.route('/transcribe', methods=['POST'])
def transcribe():
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
    except Exception as e:
        return jsonify({"text": "", "error": str(e)})
    finally:
        os.unlink(tmp_path)


@app.route('/run_analyze', methods=['POST'])
def run_analyze():
    data = request.json
    name = data.get('name', 'Кандидат')
    position = data.get('position', '')
    answers = data.get('answers', [])
    questions = data.get('questions', [])
    conversation = "Кандидат: " + name + "\nПосада: " + position + "\n\n"
    for q, a in zip(questions, answers):
        if a.strip():
            conversation += "Питання: " + q + "\nВідповідь: " + a + "\n\n"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": conversation}
        ],
        temperature=0.3
    )
    return jsonify({"result": response.choices[0].message.content})


if __name__ == '__main__':
    print("Профайлер запущено!")
    print("Відкрий браузер і перейди на: http://localhost:5000")
    port = int(os.environ.get('PORT', 5000))
app.run(debug=False, host='0.0.0.0', port=port)