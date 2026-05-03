# v2.1
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI
from datetime import datetime
import json, tempfile, os, secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ADMIN_EMAIL = "a.v.maryniak@gmail.com"

PRICES = {
    "fast": 99,
    "medium": 249,
    "deep": 499
}
SIGNUP_BONUS = 99

# ===== MODELS =====
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120))
    balance = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    candidate_name = db.Column(db.String(120))
    position = db.Column(db.String(120))
    mode = db.Column(db.String(20))
    questions = db.Column(db.Text)
    answers = db.Column(db.Text)
    result = db.Column(db.Text)
    cost = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer)  # positive = top-up, negative = spending
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

QUESTIONS_FALLBACK = {
    "fast": [
        "Розкажіть про себе і чому ви обрали цю професію?",
        "Що для вас найважливіше в роботі?",
        "Як ви розумієте, що добре впорались зі своєю роботою?",
        "Чого ви хочете досягти у цій професії?",
        "Розкажіть про найкращий досвід у вашій роботі.",
        "Чий підхід або людина є для вас орієнтиром у роботі?",
        "Як ви дієте коли щось пішло не за планом?",
        "Що ви робите, коли стикаєтесь з новим завданням?",
        "Як ви ставитесь до критики від керівництва?",
        "Що мотивує вас у роботі?",
        "Як ви планують свій робочий день?",
        "Як ви справляєтесь зі стресом на роботі?",
        "Любите чіткі інструкції чи свободу дій?",
        "Як ви ставитесь до змін у звичних процесах?",
        "На який термін зазвичай плануєте робочі цілі?",
        "Що відрізняє вас від інших фахівців у цій сфері?"
    ],
    "medium": [
        "Чого ви найбільше хочете від своєї роботи?",
        "Що найважливіше в роботі для вас?",
        "Що спонукало вас обрати саме цю професію?",
        "Чого хочете уникнути в роботі?",
        "Як розумієте, що добре впорались зі своєю роботою?",
        "Хто є для вас орієнтиром?",
        "Розкажіть про найкращий досвід у роботі.",
        "Плануєте з загальної картини чи з конкретних кроків?",
        "Як дієте при новому завданні?",
        "Якщо щось пішло не за планом, що робите?",
        "Любите чіткі інструкції чи свободу дій?",
        "Як плануєте робочий день?",
        "Найважчий момент у роботі?",
        "Що робите при стресі?",
        "Як оцінюєте себе як спеціаліста?",
        "Як ставитесь до змін?",
        "На який термін плануєте життя?",
        "Як ви приймаєте рішення у складних ситуаціях?",
        "Що для вас важливіше — результат чи процес?",
        "Як ви оцінюєте, чи добре виконали роботу?",
        "Що залежить від вас, а що від обставин?",
        "Як ви розставляєте пріоритети?",
        "Які цінності найважливіші для вас у роботі?",
        "Як ви реагуєте на несподівані зміни плану?",
        "Що робите, коли треба швидко прийняти рішення?",
        "Як ви будуєте стосунки з колегами?",
        "Чи легко вам дається співпраця в команді?",
        "Що найбільше дратує вас у роботі?"
    ],
    "deep": [
        "Чого ви хочете від роботи?",
        "Що найважливіше?",
        "Чому обрали професію?",
        "Чого хочете уникнути?",
        "Як розумієте успіх?",
        "Хто орієнтир?",
        "Найкращий досвід?",
        "Загальна картина чи кроки?",
        "Як дієте при новому?",
        "Що робите при збої?",
        "Інструкції чи свобода?",
        "Як плануєте день?",
        "Найважчий момент?",
        "Що робите при стресі?",
        "Як оцінюєте себе?",
        "Ставлення до змін?",
        "Термін планування?",
        "Що відрізняє вас?",
        "Прагнення в розвитку?",
        "Як справляєтесь коли все не так?",
        "Самостійно чи в команді?",
        "Як ставитесь до контролю?",
        "Ідеальні стосунки з командою?",
        "Що думаєте після важкого дня?",
        "Що важливіше — комфорт чи результат?",
        "Що робите коли керівник вимагає неприйнятне?",
        "Бувало що діяли інакше?",
        "Як організуєте інформацію?",
        "Як засвоюєте нове?",
        "Як зчитуєте стан інших?",
        "Що першим помічаєте на новому місці?",
        "Як змінювали роботи?",
        "Стабільність чи різноманіття?",
        "Бачите себе через 5 років?",
        "Що залежить від вас, а що від ситуації?",
        "Як приймаєте складні рішення?",
        "Які цінності керують вашими виборами?",
        "Які переконання допомагають у роботі?",
        "Як ви фільтруєте важливе від другорядного?",
        "Що ви робите, коли дві важливі речі суперечать одна одній?"
    ]
}

SYSTEM_PROMPT_FAST = """Ти досвідчений HR-психолог з 15+ років практики. Зроби звіт у форматі ПРОТОКОЛУ.

ФОРМАТ для кожного блоку (6 блоків):
БЛОК N. НАЗВА
Питання: [питання]
Відповідь: "[цитата]"
Аналіз: [абзац 3-4 речення живою мовою]

8 БЛОКІВ:
БЛОК 1. МОТИВАЦІЯ (До / Від)
БЛОК 2. РЕФЕРЕНЦІЯ (Внутрішня / Зовнішня)
БЛОК 3. ПРОАКТИВНІСТЬ / РЕАКТИВНІСТЬ
БЛОК 4. МОЖЛИВОСТІ / ПРОЦЕДУРИ
БЛОК 5. МАСШТАБ
БЛОК 6. УПРАВЛІННЯ СТРЕСОМ
БЛОК 7. ЧАСОВА ОРІЄНТАЦІЯ
БЛОК 8. СТИЛЬ РОБОТИ

В КІНЦІ:
ВИСНОВОК (3-4 речення)
СИЛЬНІ СТОРОНИ (3 пункти)
НА ЩО ЗВЕРНУТИ УВАГУ (3 пункти)
РЕКОМЕНДАЦІЯ (1-2 речення)

В КІНЦІ ЗВІТУ ОКРЕМИЙ РОЗДІЛ:
АЛЬТЕРНАТИВНІ ПОСАДИ
Назви 2-3 інші посади де ця людина може проявити себе сильно, з коротким поясненням чому.

ВАЖЛИВО — СТИЛЬ ПИСЬМА:
Пиши як досвідчений HR-психолог, не як ШІ.
- Жодних шаблонів типу "кандидат демонструє", "це свідчить про"
- Жодних емодзі, маркдауну
- Природна жива мова, людські формулювання
- Допускаються "помітно", "видно", "схоже", "враження таке"
- Уникай надмірної впевненості: "ймовірно", "схиляється до"
- Конкретні цитати — обов'язково
- Кожен блок аналізу — суцільний абзац без списків
- Висновок — як портрет людини, не таблиця"""

SYSTEM_PROMPT_MEDIUM = """Ти досвідчений HR-психолог з 15+ років практики. Зроби детальний звіт у форматі ПРОТОКОЛУ живою людською мовою.

ФОРМАТ для кожного блоку:
БЛОК N. НАЗВА
Питання: [питання]
Відповідь: "[цитата]"
Аналіз: [абзац 4-5 речень живою мовою]

14 БЛОКІВ:
БЛОК 1. МОТИВАЦІЯ
БЛОК 2. РЕФЕРЕНЦІЯ
БЛОК 3. МАСШТАБ МИСЛЕННЯ
БЛОК 4. ПРОАКТИВНІСТЬ / РЕАКТИВНІСТЬ
БЛОК 5. МОЖЛИВОСТІ / ПРОЦЕДУРИ
БЛОК 6. ЧАСОВА ОРІЄНТАЦІЯ
БЛОК 7. ФОКУС УВАГИ
БЛОК 8. УПРАВЛІННЯ СТРЕСОМ
БЛОК 9. СТИЛЬ РОБОТИ
БЛОК 10. СТАВЛЕННЯ ДО ЗМІН
БЛОК 11. СТАВЛЕННЯ ДО ПРАВИЛ
БЛОК 12. СТИЛЬ ПОРІВНЯННЯ
БЛОК 13. ЛОКУС КОНТРОЛЮ
БЛОК 14. СТИЛЬ УХВАЛЕННЯ РІШЕНЬ

В КІНЦІ:
ВИСНОВОК (5-6 речень живої характеристики)
СИЛЬНІ СТОРОНИ (5 пунктів з поясненням)
НА ЩО ЗВЕРНУТИ УВАГУ (5 пунктів з рекомендацією)
РЕКОМЕНДАЦІЯ ЩОДО СУМІСНОСТІ

В КІНЦІ ЗВІТУ ОКРЕМИЙ РОЗДІЛ:
АЛЬТЕРНАТИВНІ ПОСАДИ
Назви 2-3 інші посади де ця людина може проявити себе сильно, з коротким поясненням чому.

ВАЖЛИВО — СТИЛЬ ПИСЬМА:
Пиши як досвідчений HR-психолог, не як ШІ.
- Жодних шаблонів типу "кандидат демонструє", "це свідчить про"
- Жодних емодзі, маркдауну
- Природна жива мова, людські формулювання
- Допускаються "помітно", "видно", "схоже", "враження таке"
- Уникай надмірної впевненості: "ймовірно", "схиляється до"
- Конкретні цитати — обов'язково
- Кожен блок аналізу — суцільний абзац без списків
- Висновок — як портрет людини, не таблиця"""

SYSTEM_PROMPT_DEEP = """Ти провідний HR-психолог з 20+ років практики, експерт з НЛП за школою Шелле, Холла, Вудсмолла. Пишеш найбільш глибокий професійний звіт живою людською мовою.

ФОРМАТ для кожного блоку:
БЛОК N. НАЗВА
Питання: [питання]
Відповідь: "[цитата]"
Аналіз: [абзац 5-7 речень — глибокий розбір живою мовою]

20 БЛОКІВ:
БЛОК 1. МОТИВАЦІЯ
БЛОК 2. РЕФЕРЕНЦІЯ
БЛОК 3. МАСШТАБ МИСЛЕННЯ
БЛОК 4. СХОЖІСТЬ / ВІДМІННІСТЬ
БЛОК 5. ПРОАКТИВНІСТЬ / РЕАКТИВНІСТЬ
БЛОК 6. МОЖЛИВОСТІ / ПРОЦЕДУРИ
БЛОК 7. ЧАСОВА ОРІЄНТАЦІЯ
БЛОК 8. ФОКУС УВАГИ
БЛОК 9. ПЕРЕКОНАННЯ
БЛОК 10. СТИЛЬ ПОРІВНЯННЯ
БЛОК 11. УПРАВЛІННЯ СТРЕСОМ
БЛОК 12. СТИЛЬ РОБОТИ
БЛОК 13. ОРГАНІЗАЦІЯ ІНФОРМАЦІЇ
БЛОК 14. СТАВЛЕННЯ ДО ЗМІН
БЛОК 15. СТАВЛЕННЯ ДО ПРАВИЛ
БЛОК 16. МОДАЛЬНОСТІ
БЛОК 17. ЧАСОВИЙ ГОРИЗОНТ
БЛОК 18. ЛОКУС КОНТРОЛЮ
БЛОК 19. СТИЛЬ УХВАЛЕННЯ РІШЕНЬ
БЛОК 20. ЦІННІСНІ ФІЛЬТРИ

В КІНЦІ:
ВИСНОВОК (6-8 речень живого портрету)
СИЛЬНІ СТОРОНИ (5 пунктів з детальним поясненням)
НА ЩО ЗВЕРНУТИ УВАГУ (5 пунктів з рекомендацією)
РЕКОМЕНДАЦІЯ ЩОДО СУМІСНОСТІ (прозою, без списків)

В КІНЦІ ЗВІТУ ОКРЕМИЙ РОЗДІЛ:
АЛЬТЕРНАТИВНІ ПОСАДИ
Назви 2-3 інші посади де ця людина може проявити себе сильно, з коротким поясненням чому.

ВАЖЛИВО — СТИЛЬ ПИСЬМА:
Пиши як досвідчений HR-психолог, не як ШІ.
- Жодних шаблонів типу "кандидат демонструє", "це свідчить про"
- Жодних емодзі, маркдауну
- Природна жива мова, людські формулювання
- Допускаються "помітно", "видно", "схоже", "враження таке"
- Уникай надмірної впевненості: "ймовірно", "схиляється до"
- Конкретні цитати — обов'язково
- Кожен блок аналізу — суцільний абзац без списків
- Висновок — як портрет людини, не таблиця"""

PROMPTS = {
    "fast": SYSTEM_PROMPT_FAST,
    "medium": SYSTEM_PROMPT_MEDIUM,
    "deep": SYSTEM_PROMPT_DEEP
}

# ===== AUTH ROUTES =====
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        name = request.form.get('name','').strip()
        if not email or not password:
            flash('Заповніть всі поля', 'error')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('Пароль має бути не менше 6 символів', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Такий email вже зареєстрований', 'error')
            return redirect(url_for('register'))
        user = User(email=email, name=name, balance=SIGNUP_BONUS, is_admin=(email==ADMIN_EMAIL))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        t = Transaction(user_id=user.id, amount=SIGNUP_BONUS, description='Бонус за реєстрацію')
        db.session.add(t)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Невірний email або пароль', 'error')
        return redirect(url_for('login'))
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    tests = Test.query.filter_by(user_id=current_user.id).order_by(Test.created_at.desc()).limit(20).all()
    return render_template_string(DASHBOARD_HTML, user=current_user, tests=tests, prices=PRICES)

@app.route('/test')
@login_required
def test_page():
    min_price = min(PRICES.values())
    if current_user.balance < min_price:
        flash(f'Недостатньо коштів для проведення тесту. Мінімум {min_price} грн. Поповніть баланс.', 'error')
        return redirect(url_for('billing'))
    return render_template_string(TEST_HTML, questions_json=json.dumps(QUESTIONS_FALLBACK, ensure_ascii=False), prices=PRICES, balance=current_user.balance)

@app.route('/history')
@login_required
def history():
    tests = Test.query.filter_by(user_id=current_user.id).order_by(Test.created_at.desc()).all()
    return render_template_string(HISTORY_HTML, user=current_user, tests=tests)

@app.route('/test/<int:test_id>')
@login_required
def view_test(test_id):
    t = Test.query.get_or_404(test_id)
    if t.user_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('dashboard'))
    return render_template_string(VIEW_TEST_HTML, test=t)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template_string(ADMIN_HTML, users=users)

@app.route('/admin/topup', methods=['POST'])
@login_required
def admin_topup():
    if not current_user.is_admin:
        return jsonify({"error": "forbidden"}), 403
    data = request.json
    user_id = data.get('user_id')
    amount = int(data.get('amount', 0))
    note = data.get('note', 'Поповнення вручну')
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    user.balance += amount
    t = Transaction(user_id=user.id, amount=amount, description=note)
    db.session.add(t)
    db.session.commit()
    return jsonify({"success": True, "new_balance": user.balance})

@app.route('/billing')
@login_required
def billing():
    txs = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    return render_template_string(BILLING_HTML, user=current_user, txs=txs)

# ===== TEST API =====
@app.route('/generate_questions', methods=['POST'])
@login_required
def generate_questions():
    try:
        data = request.json
        position = data.get('position', '')
        mode = data.get('mode', 'medium')
        cost = PRICES.get(mode, 249)
        if current_user.balance < cost:
            return jsonify({"error": f"Недостатньо коштів. Потрібно {cost} грн, на балансі {current_user.balance} грн.", "insufficient_balance": True, "required": cost, "balance": current_user.balance}), 402
        count = {"fast": 16, "medium": 28, "deep": 40}.get(mode, 17)
        prompt = f"""Згенеруй рівно {count} питань для метапрограмного НЛП-інтерв'ю кандидата на посаду "{position}".

Вимоги:
- Питання адаптовані під професію
- Кожне виявляє кілька метапрограм
- Відкриті, природні
- Українською мовою
- Лише питання по одному на рядок, без нумерації"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        text = response.choices[0].message.content.strip()
        questions = [q.strip().lstrip('0123456789.-) ').strip() for q in text.split('\n') if q.strip()]
        questions = [q for q in questions if len(q) > 10][:count]
        if len(questions) < count - 2:
            questions = QUESTIONS_FALLBACK.get(mode, QUESTIONS_FALLBACK["medium"])
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"questions": QUESTIONS_FALLBACK.get('medium'), "error": str(e)})

@app.route('/transcribe', methods=['POST'])
@login_required
def transcribe():
    try:
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name
        try:
            with open(tmp_path, 'rb') as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", file=f, language="uk"
                )
            return jsonify({"text": transcript.text})
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        return jsonify({"text": "", "error": str(e)})

@app.route('/run_analyze', methods=['POST'])
@login_required
def run_analyze():
    try:
        data = request.json
        name = data.get('name', 'Кандидат')
        position = data.get('position', '')
        mode = data.get('mode', 'medium')
        answers = data.get('answers', [])
        questions = data.get('questions', [])
        
        cost = PRICES.get(mode, 249)
        if current_user.balance < cost:
            return jsonify({"error": f"Недостатньо коштів. Потрібно {cost} грн, на балансі {current_user.balance} грн. Поповніть баланс."}), 402
        
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
            temperature=0.7
        )
        result = response.choices[0].message.content
        
        # Save test, deduct balance
        current_user.balance -= cost
        t = Test(
            user_id=current_user.id,
            candidate_name=name,
            position=position,
            mode=mode,
            questions=json.dumps(questions, ensure_ascii=False),
            answers=json.dumps(answers, ensure_ascii=False),
            result=result,
            cost=cost
        )
        db.session.add(t)
        tx = Transaction(user_id=current_user.id, amount=-cost, description=f'Тест: {name} - {position} ({mode})')
        db.session.add(tx)
        db.session.commit()
        
        return jsonify({"result": result, "test_id": t.id, "new_balance": current_user.balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


REGISTER_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Реєстрація — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}
</style></head>
<body>
<div style="max-width:450px;margin:60px auto;padding:0 20px">
<div class="card">
<h1 style="text-align:center;margin-bottom:25px;color:#2c3e50">🔍 MetaProfile</h1>
<h2 style="text-align:center;margin-bottom:20px;font-size:18px">Реєстрація</h2>
{% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for cat,msg in messages %}<div class="flash">{{msg}}</div>{% endfor %}{% endif %}{% endwith %}
<form method="POST">
<div style="margin-bottom:15px"><label>Імя:</label><input type="text" name="name" placeholder="Ваше ім'я"></div>
<div style="margin-bottom:15px"><label>Email:</label><input type="email" name="email" required></div>
<div style="margin-bottom:15px"><label>Пароль (мін. 6 символів):</label><input type="password" name="password" required minlength="6"></div>
<button type="submit" class="btn btn-green" style="width:100%">Зареєструватись</button>
</form>
<p style="text-align:center;margin-top:15px;font-size:13px">Бонус 99 грн на перший тест!</p>
<p style="text-align:center;margin-top:15px"><a href="/login">Вже маєте акаунт? Увійти</a></p>
</div>
</div>
</body></html>"""

LOGIN_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Вхід — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}
</style></head>
<body>
<div style="max-width:450px;margin:60px auto;padding:0 20px">
<div class="card">
<h1 style="text-align:center;margin-bottom:25px;color:#2c3e50">🔍 MetaProfile</h1>
<h2 style="text-align:center;margin-bottom:20px;font-size:18px">Вхід</h2>
{% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}{% for cat,msg in messages %}<div class="flash">{{msg}}</div>{% endfor %}{% endif %}{% endwith %}
<form method="POST">
<div style="margin-bottom:15px"><label>Email:</label><input type="email" name="email" required></div>
<div style="margin-bottom:15px"><label>Пароль:</label><input type="password" name="password" required></div>
<button type="submit" class="btn" style="width:100%">Увійти</button>
</form>
<p style="text-align:center;margin-top:15px"><a href="/register">Немає акаунта? Зареєструватись</a></p>
</div>
</div>
</body></html>"""

DASHBOARD_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Кабінет — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}
</style></head>
<body>
<div class="header">
<h1>🔍 MetaProfile</h1>
<div>
<a href="/dashboard">Кабінет</a>
<a href="/test">Новий тест</a>
<a href="/history">Історія</a>
<a href="/billing">Баланс</a>
{% if current_user.is_admin %}<a href="/admin">Адмінка</a>{% endif %}
<a href="/logout">Вийти ({{ current_user.email }})</a>
</div>
</div>
<div class="container">
<div class="balance-card">
<h2>Поточний баланс</h2>
<div class="amount">{{ user.balance }} грн</div>
<div style="margin-top:10px;font-size:13px">Ціни: Швидкий — {{ prices.fast }} грн · Середній — {{ prices.medium }} грн · Глибокий — {{ prices.deep }} грн</div>
</div>

<div class="card">
<h2 style="margin-bottom:15px">Швидкі дії</h2>
<a href="/test" class="btn btn-green">▶ Провести тест</a>
<a href="/history" class="btn btn-blue" style="margin-left:10px">📋 Історія тестів</a>
<a href="/billing" class="btn" style="margin-left:10px">💳 Поповнити баланс</a>
</div>

<div class="card">
<h2 style="margin-bottom:15px">Останні тести</h2>
{% if tests %}
<table>
<tr><th>Дата</th><th>Кандидат</th><th>Посада</th><th>Тип</th><th>Сума</th><th></th></tr>
{% for t in tests %}
<tr>
<td>{{ t.created_at.strftime('%d.%m.%Y %H:%M') }}</td>
<td>{{ t.candidate_name }}</td>
<td>{{ t.position }}</td>
<td><span class="tag tag-{{t.mode}}">{{ {'fast':'Швидкий','medium':'Середній','deep':'Глибокий'}[t.mode] }}</span></td>
<td>{{ t.cost }} грн</td>
<td><a href="/test/{{ t.id }}" class="btn btn-blue" style="padding:5px 12px;font-size:12px">Звіт</a></td>
</tr>
{% endfor %}
</table>
{% else %}
<p style="color:#888">Поки немає тестів. <a href="/test">Провести перший</a> — у вас є бонус!</p>
{% endif %}
</div>

<div class="card">
<h2 style="margin-bottom:10px">Як поповнити баланс</h2>
<p style="line-height:1.6">Поки що поповнення працює вручну. Перекажіть кошти на реквізити нижче і напишіть нам в Telegram або Viber із вашим email — ми зарахуємо баланс протягом 1-2 годин.</p>
<div style="background:#f8f9fa;padding:15px;border-radius:8px;margin-top:12px;font-family:monospace;font-size:13px">
ФОП Мариняк Андрій Володимирович<br>
ІПН: 3261605297<br>
Тел: +380969611196<br>
р/р UA 553052990000026008021021364<br>
АТ КБ "ПриватБанк", МФО 305299
</div>
</div>
</div>
</body></html>"""

HISTORY_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Історія — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}
</style></head>
<body><div class="header">
<h1>🔍 MetaProfile</h1>
<div>
<a href="/dashboard">Кабінет</a>
<a href="/test">Новий тест</a>
<a href="/history">Історія</a>
<a href="/billing">Баланс</a>
{% if current_user.is_admin %}<a href="/admin">Адмінка</a>{% endif %}
<a href="/logout">Вийти ({{ current_user.email }})</a>
</div>
</div>
<div class="container">
<div class="card">
<h2 style="margin-bottom:15px">Історія всіх тестів</h2>
{% if tests %}
<table>
<tr><th>Дата</th><th>Кандидат</th><th>Посада</th><th>Тип</th><th>Сума</th><th></th></tr>
{% for t in tests %}
<tr>
<td>{{ t.created_at.strftime('%d.%m.%Y %H:%M') }}</td>
<td>{{ t.candidate_name }}</td>
<td>{{ t.position }}</td>
<td><span class="tag tag-{{t.mode}}">{{ {'fast':'Швидкий','medium':'Середній','deep':'Глибокий'}[t.mode] }}</span></td>
<td>{{ t.cost }} грн</td>
<td><a href="/test/{{ t.id }}" class="btn btn-blue" style="padding:5px 12px;font-size:12px">Переглянути</a></td>
</tr>
{% endfor %}
</table>
{% else %}<p>Тестів поки немає.</p>{% endif %}
</div></div></body></html>"""

VIEW_TEST_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Звіт — {{ test.candidate_name }}</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}

.report-content{white-space:pre-wrap;line-height:1.7;font-size:14px;background:white;padding:25px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
</style></head>
<body><div class="header">
<h1>🔍 MetaProfile</h1>
<div>
<a href="/dashboard">Кабінет</a>
<a href="/test">Новий тест</a>
<a href="/history">Історія</a>
<a href="/billing">Баланс</a>
{% if current_user.is_admin %}<a href="/admin">Адмінка</a>{% endif %}
<a href="/logout">Вийти ({{ current_user.email }})</a>
</div>
</div>
<div class="container">
<div class="card">
<h1 style="margin-bottom:5px">Звіт: {{ test.candidate_name }}</h1>
<p style="color:#666">Посада: <strong>{{ test.position }}</strong> · Тип: <span class="tag tag-{{test.mode}}">{{ {'fast':'Швидкий','medium':'Середній','deep':'Глибокий'}[test.mode] }}</span> · Дата: {{ test.created_at.strftime('%d.%m.%Y %H:%M') }}</p>
<div style="margin-top:15px">
<button class="btn btn-red" onclick="downloadPdf()">📕 Завантажити PDF</button>
<button class="btn" onclick="copyResult()">📋 Копіювати</button>
<a href="/test" class="btn btn-green">🔄 Новий тест</a>
</div>
</div>
<div class="report-content" id="report">{{ test.result }}</div>
</div>
<script>
function downloadPdf(){
  const w = window.open("", "_blank");
  const html = "<html><head><meta charset='UTF-8'><title>Профайл {{ test.candidate_name }}</title>" +
    "<style>body{font-family:Georgia,serif;max-width:800px;margin:30px auto;padding:20px;line-height:1.7;color:#222}" +
    "h1{color:#2c3e50;border-bottom:3px solid #2c3e50;padding-bottom:10px}" +
    ".meta{background:#f8f9fa;padding:15px;border-radius:8px;margin-bottom:25px}" +
    ".content{white-space:pre-wrap;font-size:14px}@media print{body{margin:0}}</style></head><body>" +
    "<h1>Метапрограмний профіль кандидата</h1>" +
    "<div class='meta'><strong>Кандидат:</strong> {{ test.candidate_name }}<br>" +
    "<strong>Посада:</strong> {{ test.position }}<br>" +
    "<strong>Дата:</strong> {{ test.created_at.strftime('%d.%m.%Y') }}</div>" +
    "<div class='content'>" + document.getElementById("report").textContent.replace(/</g,"&lt;") + "</div>" +
    "<script>setTimeout(()=>window.print(),500)<\/script></body></html>";
  w.document.write(html); w.document.close();
}
function copyResult(){
  navigator.clipboard.writeText(document.getElementById("report").textContent).then(()=>alert("Скопійовано!"));
}
</script>
</body></html>"""

BILLING_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Баланс — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}
</style></head>
<body><div class="header">
<h1>🔍 MetaProfile</h1>
<div>
<a href="/dashboard">Кабінет</a>
<a href="/test">Новий тест</a>
<a href="/history">Історія</a>
<a href="/billing">Баланс</a>
{% if current_user.is_admin %}<a href="/admin">Адмінка</a>{% endif %}
<a href="/logout">Вийти ({{ current_user.email }})</a>
</div>
</div>
<div class="container">
<div class="balance-card">
<h2>Поточний баланс</h2>
<div class="amount">{{ user.balance }} грн</div>
</div>

<div class="card">
<h2 style="margin-bottom:15px">Як поповнити</h2>
<p style="line-height:1.7;margin-bottom:12px">Перекажіть кошти на реквізити нижче і напишіть нам в Telegram або Viber вказавши ваш email — ми зарахуємо баланс протягом 1-2 годин у робочий час.</p>
<div style="background:#f8f9fa;padding:18px;border-radius:8px;font-family:monospace;font-size:14px;line-height:1.8">
<strong>ФОП Мариняк Андрій Володимирович</strong><br>
ІПН: 3261605297<br>
Телефон: +380969611196<br>
р/р UA 553052990000026008021021364<br>
АТ КБ "ПриватБанк", МФО 305299
</div>
<p style="margin-top:15px;font-size:13px;color:#666">Ваш email для звірки: <strong>{{ user.email }}</strong></p>
</div>

<div class="card">
<h2 style="margin-bottom:15px">Історія операцій</h2>
{% if txs %}
<table>
<tr><th>Дата</th><th>Опис</th><th>Сума</th></tr>
{% for tx in txs %}
<tr>
<td>{{ tx.created_at.strftime('%d.%m.%Y %H:%M') }}</td>
<td>{{ tx.description }}</td>
<td style="font-weight:bold;color:{% if tx.amount >= 0 %}#27ae60{% else %}#e74c3c{% endif %}">{% if tx.amount >= 0 %}+{% endif %}{{ tx.amount }} грн</td>
</tr>
{% endfor %}
</table>
{% else %}<p>Операцій поки немає.</p>{% endif %}
</div>
</div></body></html>"""

ADMIN_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Адмінка — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}
</style></head>
<body><div class="header">
<h1>🔍 MetaProfile</h1>
<div>
<a href="/dashboard">Кабінет</a>
<a href="/test">Новий тест</a>
<a href="/history">Історія</a>
<a href="/billing">Баланс</a>
{% if current_user.is_admin %}<a href="/admin">Адмінка</a>{% endif %}
<a href="/logout">Вийти ({{ current_user.email }})</a>
</div>
</div>
<div class="container">
<div class="card">
<h1 style="margin-bottom:15px">⚙️ Адмінка</h1>
<table>
<tr><th>Email</th><th>Імя</th><th>Баланс</th><th>Дата</th><th>Поповнити</th></tr>
{% for u in users %}
<tr>
<td>{{ u.email }}{% if u.is_admin %} 👑{% endif %}</td>
<td>{{ u.name or '—' }}</td>
<td><strong>{{ u.balance }} грн</strong></td>
<td>{{ u.created_at.strftime('%d.%m.%Y') }}</td>
<td>
<input type="number" id="amt_{{u.id}}" placeholder="грн" style="width:90px;padding:5px">
<button class="btn btn-green" style="padding:5px 12px;font-size:12px" onclick="topup({{u.id}})">+</button>
</td>
</tr>
{% endfor %}
</table>
</div>
</div>
<script>
async function topup(uid){
  const amt = parseInt(document.getElementById('amt_'+uid).value);
  if(!amt) return;
  const note = prompt('Опис (наприклад: оплата 500 грн карткою)') || 'Поповнення';
  const r = await fetch('/admin/topup',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body:JSON.stringify({user_id:uid, amount:amt, note})
  });
  const d = await r.json();
  if(d.success){alert('Зараховано! Новий баланс: '+d.new_balance+' грн');location.reload();}
  else alert('Помилка: '+(d.error||'unknown'));
}
</script>
</body></html>"""

TEST_HTML = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Новий тест — MetaProfile</title><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#f0f2f5;min-height:100vh;color:#222}
.header{background:#2c3e50;color:white;padding:15px 25px;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:22px}
.header a{color:white;text-decoration:none;margin-left:20px;font-size:14px}
.header a:hover{text-decoration:underline}
.container{max-width:900px;margin:25px auto;padding:0 20px}
.card{background:white;border-radius:12px;padding:22px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
label{font-weight:bold;display:block;margin-bottom:8px;color:#333}
input,select,textarea{width:100%;padding:11px;border:2px solid #ddd;border-radius:8px;font-size:15px;font-family:inherit}
.btn{background:#2c3e50;color:white;border:none;padding:12px 28px;border-radius:8px;font-size:15px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#34495e}
.btn-green{background:#27ae60}
.btn-red{background:#e74c3c}
.btn-blue{background:#3498db}
.flash{padding:12px;border-radius:8px;margin-bottom:15px;background:#fee;color:#c00;border-left:4px solid #c00}
.balance-card{background:linear-gradient(135deg,#27ae60,#2ecc71);color:white;padding:25px;border-radius:12px;margin-bottom:20px}
.balance-card h2{font-size:14px;opacity:0.9;margin-bottom:5px}
.balance-card .amount{font-size:36px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #eee;font-size:14px}
th{background:#f8f9fa;font-weight:bold}
.tag{display:inline-block;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:bold}
.tag-fast{background:#3498db;color:white}
.tag-medium{background:#f39c12;color:white}
.tag-deep{background:#27ae60;color:white}
.modes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px}
.mode-card{border:2px solid #ddd;border-radius:10px;padding:15px;cursor:pointer;text-align:center;transition:all 0.2s}
.mode-card:hover{border-color:#3498db}
.mode-card.selected{border-color:#27ae60;background:#e8f8f0}
.mode-name{font-weight:bold;font-size:15px;color:#2c3e50;margin-bottom:5px}
.mode-desc{font-size:12px;color:#666}
.mode-price{color:#27ae60;font-weight:bold;font-size:18px;margin-top:5px}
.hint{font-size:12px;color:#999;margin-top:5px}

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
</style></head>
<body><div class="header">
<h1>🔍 MetaProfile</h1>
<div>
<a href="/dashboard">Кабінет</a>
<a href="/test">Новий тест</a>
<a href="/history">Історія</a>
<a href="/billing">Баланс</a>
{% if current_user.is_admin %}<a href="/admin">Адмінка</a>{% endif %}
<a href="/logout">Вийти ({{ current_user.email }})</a>
</div>
</div>
<div class="container">
<div id="setup">
<div class="balance-card" style="padding:18px"><div style="display:flex;justify-content:space-between;align-items:center"><div><div style="font-size:13px;opacity:0.9">Баланс</div><div style="font-size:24px;font-weight:bold">{{ balance }} грн</div></div><a href="/billing" style="color:white;font-size:13px;text-decoration:underline">Поповнити</a></div></div>

<div class="card"><label>Імя кандидата:</label><input type="text" id="candidate_name" placeholder="Введіть імя..."></div>
<div class="card"><label>Посада:</label><input type="text" id="position_select" placeholder="Введіть посаду (наприклад: Поліграфолог, Слідчий, Дизайнер...)"><p class="hint">💡 Введіть будь-яку посаду — питання адаптуються під неї автоматично</p></div>
<div class="card">
<label>Формат тестування:</label>
<div class="modes">
<div class="mode-card" data-mode="fast" onclick="selectMode('fast')"><div class="mode-name">⚡ Швидкий</div><div class="mode-desc">16 питань<br>8 метапрограм</div><div class="mode-price">{{ prices.fast }} грн</div></div>
<div class="mode-card selected" data-mode="medium" onclick="selectMode('medium')"><div class="mode-name">📊 Середній</div><div class="mode-desc">28 питань<br>14 метапрограм</div><div class="mode-price">{{ prices.medium }} грн</div></div>
<div class="mode-card" data-mode="deep" onclick="selectMode('deep')"><div class="mode-name">🧠 Глибокий</div><div class="mode-desc">40 питань<br>20 метапрограм</div><div class="mode-price">{{ prices.deep }} грн</div></div>
</div>
</div>
<button class="btn btn-green" onclick="startQuiz()" style="width:100%;font-size:17px;padding:15px">▶ Розпочати тестування</button>
</div>

<div id="quiz" style="display:none">
<div class="card" style="background:#fff8e1;border-left:4px solid #f39c12"><div style="font-size:14px;color:#7d4f00;line-height:1.5"><strong>📢 Інструкція:</strong> говоріть <strong>голосно і повільно</strong>. Перевірте текст і відредагуйте якщо є помилки.</div></div>
<div class="card"><div style="display:flex;justify-content:space-between"><span id="progress_text" style="color:#888"></span><span id="candidate_display" style="font-weight:bold"></span></div><div class="progress"><div class="progress-bar" id="progress_bar"></div></div></div>
<div class="card" id="questions_container"></div>
<div style="display:flex;gap:10px;margin-bottom:18px"><button class="nav-btn" id="prev_btn" onclick="prevQuestion()" disabled>← Назад</button><button class="nav-btn" id="next_btn" onclick="nextQuestion()">Далі →</button></div>
<button class="analyze-btn" id="analyze_btn" onclick="doAnalyze()">🧠 Проаналізувати</button>
</div>
<div id="loading">⏳ Готую...</div>
<div id="result"></div>
</div>
<script>
const QUESTIONS = {{ questions_json|safe }};
let DYNAMIC_QUESTIONS=null, current=0, answers=[], mediaRecorder=null, audioChunks=[], currentMode="medium";

function selectMode(mode){currentMode=mode;document.querySelectorAll('.mode-card').forEach(c=>c.classList.remove('selected'));document.querySelector('.mode-card[data-mode="'+mode+'"]').classList.add('selected');}

async function startQuiz(){
  const name=document.getElementById("candidate_name").value.trim();
  const pos=document.getElementById("position_select").value.trim();
  if(!name){alert("Введіть імя");return}
  if(!pos){alert("Введіть посаду");return}
  const PRICES_JS={fast: {{ prices.fast }}, medium: {{ prices.medium }}, deep: {{ prices.deep }}};
  const cost=PRICES_JS[currentMode];
  const bal={{ balance }};
  if(bal<cost){
    if(confirm("Недостатньо коштів. Потрібно "+cost+" грн, на балансі "+bal+" грн.\n\nПерейти на сторінку поповнення балансу?")){
      window.location.href="/billing";
    }
    return;
  }
  document.getElementById("setup").style.display="none";
  document.getElementById("loading").style.display="block";
  document.getElementById("loading").textContent="🤖 Готую питання адаптовані під «"+pos+"»...";
  try{
    const r=await fetch("/generate_questions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({position:pos,mode:currentMode})});
    const d=await r.json();
    DYNAMIC_QUESTIONS=d.questions;
  }catch(e){DYNAMIC_QUESTIONS=QUESTIONS[currentMode];}
  document.getElementById("loading").style.display="none";
  document.getElementById("loading").textContent="⏳ Аналізую відповіді... 20-40 секунд";
  const qs=DYNAMIC_QUESTIONS;
  answers=new Array(qs.length).fill("");
  document.getElementById("candidate_display").textContent=name+" — "+pos;
  document.getElementById("quiz").style.display="block";
  buildQuestions(qs);showQuestion(0);
}

function buildQuestions(qs){
  const c=document.getElementById("questions_container");c.innerHTML="";
  qs.forEach((q,i)=>{const d=document.createElement("div");d.className="question-block";d.id="q_"+i;
    d.innerHTML='<div class="question-num">Питання '+(i+1)+' з '+qs.length+'</div><div class="question-text">'+q+'</div><textarea class="answer-area" id="answer_'+i+'" placeholder="Натисніть запис або введіть вручну..."></textarea><p class="hint">🎤 Говоріть голосно і повільно. Редагуйте якщо потрібно.</p><div class="btn-row"><button class="record-btn" id="rec_'+i+'" onclick="toggleRecord('+i+')">🎤 Записати</button></div>';
    c.appendChild(d);});
}

function showQuestion(idx){const qs=DYNAMIC_QUESTIONS||QUESTIONS[currentMode];document.querySelectorAll(".question-block").forEach(b=>b.classList.remove("active"));document.getElementById("q_"+idx).classList.add("active");document.getElementById("progress_text").textContent="Питання "+(idx+1)+" з "+qs.length;document.getElementById("progress_bar").style.width=((idx+1)/qs.length*100)+"%";document.getElementById("prev_btn").disabled=idx===0;document.getElementById("next_btn").style.display=idx===qs.length-1?"none":"inline-block";document.getElementById("analyze_btn").style.display=idx===qs.length-1?"block":"none";current=idx;}
function nextQuestion(){const qs=DYNAMIC_QUESTIONS||QUESTIONS[currentMode];if(current<qs.length-1)showQuestion(current+1)}
function prevQuestion(){if(current>0)showQuestion(current-1)}

async function toggleRecord(idx){const btn=document.getElementById("rec_"+idx);
  if(mediaRecorder && mediaRecorder.state==="recording"){mediaRecorder.stop();btn.textContent="⏳ Обробка...";btn.className="record-btn done";return}
  try{const stream=await navigator.mediaDevices.getUserMedia({audio:true});audioChunks=[];mediaRecorder=new MediaRecorder(stream);
    mediaRecorder.ondataavailable=e=>audioChunks.push(e.data);
    mediaRecorder.onstop=async()=>{stream.getTracks().forEach(t=>t.stop());const blob=new Blob(audioChunks,{type:"audio/webm"});const fd=new FormData();fd.append("audio",blob,"r.webm");
      try{const r=await fetch("/transcribe",{method:"POST",body:fd});const d=await r.json();
        if(d.text&&d.text.trim().length>0){document.getElementById("answer_"+idx).value=d.text;answers[idx]=d.text;btn.textContent="✓ Записано (натисніть для перезапису)";btn.className="record-btn done";}
        else{btn.textContent="🎤 Записати";btn.className="record-btn";alert("Не вдалось розпізнати: "+(d.error||""))}
      }catch(e){btn.textContent="🎤 Записати";btn.className="record-btn";alert("Помилка: "+e.message)}};
    mediaRecorder.start();btn.textContent="⏹ Зупинити";btn.className="record-btn recording";
  }catch(e){alert("Помилка мікрофону: "+e.message)}}

async function doAnalyze(){
  const name=document.getElementById("candidate_name").value;
  const pos=document.getElementById("position_select").value;
  (DYNAMIC_QUESTIONS||QUESTIONS[currentMode]).forEach((q,i)=>{const el=document.getElementById("answer_"+i);if(el)answers[i]=el.value||"";});
  document.getElementById("quiz").style.display="none";
  document.getElementById("loading").style.display="block";
  try{
    const r=await fetch("/run_analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name,position:pos,mode:currentMode,answers,questions:(DYNAMIC_QUESTIONS||QUESTIONS[currentMode])})});
    const d=await r.json();
    document.getElementById("loading").style.display="none";
    if(d.error){document.getElementById("result").style.display="block";document.getElementById("result").innerHTML="<strong style='color:#e74c3c'>Помилка:</strong> "+d.error+(d.error.includes("Недостатньо")?'<br><br><a href=\"/billing\" class=\"btn btn-green\">Поповнити баланс</a>':'');return;}
    if(d.test_id){window.location.href="/test/"+d.test_id;}
  }catch(e){document.getElementById("loading").style.display="none";document.getElementById("result").style.display="block";document.getElementById("result").textContent="Помилка: "+e.message;}
}
</script>
</body></html>"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
