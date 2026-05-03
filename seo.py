# -*- coding: utf-8 -*-
"""SEO landing, robots.txt and sitemap.xml for MetaProfile."""
from datetime import datetime
from flask import Response


LANDING_HTML = r"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MetaProfile — онлайн психологічне тестування кандидатів з AI-аналізом</title>
<meta name="description" content="MetaProfile — онлайн платформа для психологічного тестування кандидатів та оцінки персоналу. AI-аналіз профілю особистості, готовий звіт за 15 хвилин. Від 99 грн за тест.">
<meta name="keywords" content="онлайн тестування кандидатів, психологічний тест при прийомі на роботу, оцінка персоналу онлайн, AI оцінка кандидатів, скринінг персоналу, профайлінг кандидата, HR тести, тестування співробітників">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://www.metaprofile.online/">
<meta property="og:type" content="website">
<meta property="og:title" content="MetaProfile — AI-тестування кандидатів онлайн">
<meta property="og:description" content="Психологічний профіль кандидата за 15 хвилин. Від 99 грн.">
<meta property="og:url" content="https://www.metaprofile.online/">
<meta property="og:locale" content="uk_UA">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#1a1a1a;line-height:1.6;background:#fff}
.container{max-width:1100px;margin:0 auto;padding:0 20px}
header{padding:18px 0;border-bottom:1px solid #eee;position:sticky;top:0;background:#fff;z-index:10}
.nav{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
.logo{font-weight:700;font-size:20px;color:#111;text-decoration:none}
.nav a{color:#333;text-decoration:none;margin-left:18px;font-size:15px}
.nav a.cta{background:#111;color:#fff;padding:9px 18px;border-radius:8px}
.hero{padding:70px 0 60px;text-align:center;background:linear-gradient(180deg,#f7f8fa,#fff)}
.hero h1{font-size:42px;line-height:1.15;margin-bottom:18px}
.hero p.lead{font-size:19px;color:#444;max-width:720px;margin:0 auto 28px}
.btn{display:inline-block;padding:14px 28px;border-radius:10px;background:#111;color:#fff;text-decoration:none;font-weight:600;margin:6px}
.btn.secondary{background:#fff;color:#111;border:2px solid #111}
section{padding:64px 0;border-top:1px solid #f0f0f0}
section h2{font-size:30px;margin-bottom:32px;text-align:center}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px}
.card{background:#fafafa;border:1px solid #eee;border-radius:14px;padding:24px}
.card h3{font-size:18px;margin-bottom:10px}
.card p{color:#555;font-size:15px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}
.step{padding:24px 22px;background:#fff;border:1px solid #eee;border-radius:14px}
.step h3{font-size:18px;margin-bottom:8px}
.prices{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.price{background:#fff;border:2px solid #eee;border-radius:14px;padding:28px 22px;text-align:center}
.price.featured{border-color:#111}
.price h3{font-size:18px;margin-bottom:8px}
.price .amount{font-size:34px;font-weight:700;margin:10px 0}
.price ul{list-style:none;text-align:left;margin:18px 0}
.price li{padding:6px 0;color:#444;font-size:14px}
.price li:before{content:"✓ ";color:#0a8a3a;font-weight:700}
details{background:#fafafa;border:1px solid #eee;border-radius:10px;padding:14px 18px;margin-bottom:10px}
details summary{cursor:pointer;font-weight:600;font-size:16px}
details[open] summary{margin-bottom:10px}
details p{color:#444;font-size:15px}
footer{background:#111;color:#aaa;padding:36px 0;margin-top:40px;font-size:14px}
footer a{color:#fff;text-decoration:none}
.tagline{display:inline-block;background:#fff3cd;color:#664d03;padding:5px 12px;border-radius:20px;font-size:13px;margin-bottom:16px;font-weight:600}
@media(max-width:640px){.hero h1{font-size:30px}.hero p.lead{font-size:16px}section{padding:44px 0}section h2{font-size:24px}}
.hero-extra-link{margin-top:14px;font-size:14px;opacity:.85}
.hero-extra-link a{color:#9fb3ff;text-decoration:none;border-bottom:1px dashed #5a6dc4}
.hero-extra-link a:hover{color:#fff;border-color:#fff}
.article-promo{padding:50px 0;background:linear-gradient(135deg,#1a2540 0%,#0f1a30 100%)}
.article-promo .promo-card{max-width:760px;margin:0 auto;padding:36px 32px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;text-align:center}
.article-promo .promo-badge{display:inline-block;font-size:36px;margin-bottom:8px}
.article-promo h2{margin:8px 0 14px;font-size:24px;line-height:1.35}
.article-promo p{margin:0 0 22px;font-size:16px;opacity:.85;line-height:1.6}
.article-promo .btn{display:inline-block;padding:12px 28px;background:#4a6cf7;color:#fff;border-radius:8px;text-decoration:none;font-weight:600;transition:background .2s}
.article-promo .btn:hover{background:#5a7cff}
@media (max-width:640px){.article-promo{padding:32px 0}.article-promo .promo-card{padding:24px 18px}.article-promo h2{font-size:20px}}

</style>
</head>
<body>
<header><div class="container nav">
<a href="/" class="logo">MetaProfile</a>
<nav>
<a href="#why">Переваги</a>
<a href="#how">Як це працює</a>
<a href="#prices">Тарифи</a>
<a href="#faq">FAQ</a>
<a href="/login">Увійти</a>
<a href="/register">Реєстрація</a>
</nav>
</div></header>
<section class="hero"><div class="container">
<span class="tagline">AI-аналіз за 15 хвилин</span>
<h1>Психологічний профіль кандидата<br>онлайн за 15 хвилин</h1>
<p class="lead">MetaProfile — AI-платформа для психологічного тестування кандидатів та оцінки персоналу. Обʼєктивний звіт про сильні сторони, мотивацію та ризики — без багатогодинних співбесід.</p>
<a href="/register" class="btn">Створити акаунт безкоштовно</a>
<a href="#how" class="btn secondary">Як це працює</a>
<p class="hero-extra-link"><a href="/about-method">Не впевнені? Прочитайте за 5 хвилин чому це працює →</a></p>
<p class="free-badge" style="margin-top:18px;color:#666;font-size:0.95em">🎁 Перший тест — безкоштовно. Реєстрація — лише email.</p>
</div></section>
<section id="why"><div class="container">
<h2>Чому HR обирають MetaProfile</h2>
<div class="grid">
<div class="card"><h3>Економія часу</h3><p>Замість 2-годинної співбесіди з психологом — структурований AI-звіт за 15 хвилин. Працює 24/7 без черг.</p></div>
<div class="card"><h3>Обʼєктивність</h3><p>AI аналізує відповіді без упередженості, симпатій чи втоми. Результат однаковий для всіх кандидатів.</p></div>
<div class="card"><h3>Доступна ціна</h3><p>Перший тест — у подарунок. Далі від 99 грн за тест замість тисяч гривень за консультацію психолога.</p></div>
<div class="card"><h3>Готовий звіт</h3><p>Професійний звіт із сильними сторонами, ризиками та рекомендаціями. Можна додати до досьє кандидата.</p></div>
<div class="card"><h3>Зменшення помилок найму</h3><p>За дослідженнями, помилка найму коштує бізнесу значних сум. Обʼєктивний скринінг суттєво знижує цей ризик.</p></div>
<div class="card"><h3>Повністю онлайн</h3><p>Кандидат проходить тест із будь-якого пристрою. Ви отримуєте звіт у своєму кабінеті MetaProfile.</p></div>
</div>
</div></section>
<section id="how"><div class="container">
<h2>Як це працює</h2>
<div class="steps">
<div class="step"><h3>1. Реєстрація</h3><p>Створіть безкоштовний акаунт за хвилину — потрібен лише email.</p></div>
<div class="step"><h3>2. Поповнення</h3><p>Перший тест — безкоштовно. Далі поповніть баланс — від 99 грн за тест.</p></div>
<div class="step"><h3>3. Тестування</h3><p>Запустіть тест. Кандидат проходить його онлайн за 15 хвилин.</p></div>
<div class="step"><h3>4. Звіт</h3><p>Отримайте AI-звіт з профілем кандидата у своєму кабінеті.</p></div>
</div>
</div></section>
<section id="cases"><div class="container">
<h2>Сценарії використання</h2>
<p style="text-align:center;color:#666;max-width:720px;margin:0 auto 24px">Як HR-менеджери, власники бізнесу та психологи використовують MetaProfile у щоденній роботі.</p>
<div class="grid">
<div class="card"><h3>🛍️ Підбір менеджера з продажу</h3><p>Власник магазину перевіряє 5 кандидатів за вечір замість тижня співбесід. Отримує обʼєктивний профіль: стресостійкість, мотивація, схильність до маніпуляцій — і обирає того, хто реально витримає роботу з клієнтами.</p></div>
<div class="card"><h3>👥 Перевірка команди перед реструктуризацією</h3><p>HR-директор IT-компанії оцінює 30 співробітників перед обʼєднанням відділів. Бачить, хто здатний бути лідером, а хто краще працює виконавцем — рішення про ролі базуються на даних, а не на інтуїції.</p></div>
<div class="card"><h3>🧠 Скринінг ризику вигорання</h3><p>Психолог-консультант використовує MetaProfile для попередньої діагностики клієнтів. За 15 хвилин отримує гіпотези про сильні сторони та зони ризику — і готується до сесії якісніше, заощаджуючи перші 1-2 зустрічі.</p></div>
</div>
<h3 style="text-align:center;margin-top:48px;margin-bottom:8px">Що показує дослідження ринку</h3>
<p style="text-align:center;color:#666;max-width:720px;margin:0 auto 24px">Глобальні дані про ефективність AI-оцінки кандидатів у HR.</p>
<div class="grid">
<div class="card"><h3 style="font-size:2em;color:#2563eb">−40%</h3><p><strong>часу на найм</strong> при використанні онлайн-оцінки кандидатів замість класичних співбесід <span style="color:#999">(Aberdeen Group, дослідження HR-індустрії)</span>.</p></div>
<div class="card"><h3 style="font-size:2em;color:#2563eb">+24%</h3><p><strong>якість найму</strong> зростає, коли рішення базується на структурованій оцінці, а не на враженні рекрутера <span style="color:#999">(Harvard Business Review, мета-аналіз)</span>.</p></div>
<div class="card"><h3 style="font-size:2em;color:#2563eb">−30%</h3><p><strong>плинність кадрів</strong> у компаній, що використовують психометричну оцінку перед наймом <span style="color:#999">(SHRM, галузеві звіти)</span>.</p></div>
</div>
</div></section>
<section id="prices"><div class="container">
<h2>Тарифи</h2>
<p style="text-align:center;background:#fff7e6;border:1px solid #ffd591;border-radius:12px;padding:14px 20px;max-width:560px;margin:0 auto 28px;color:#874d00"><strong>🎁 Спробуйте безкоштовно:</strong> 1 тест у подарунок при реєстрації — без картки.</p>
<div class="prices">
<div class="price"><h3>Базовий</h3><div class="amount">99 грн</div><p>За один тест</p>
<ul><li>Основний особистісний профіль</li><li>AI-аналіз відповідей</li><li>Звіт онлайн</li></ul>
<a href="/register" class="btn">Почати</a></div>
<div class="price featured"><h3>Розширений</h3><div class="amount">249 грн</div><p>За один тест</p>
<ul><li>Все з Базового</li><li>Сильні сторони та ризики</li><li>Розширений звіт</li><li>Рекомендації для посади</li></ul>
<a href="/register" class="btn">Почати</a></div>
<div class="price"><h3>Повний</h3><div class="amount">499 грн</div><p>За один тест</p>
<ul><li>Все з Розширеного</li><li>Глибинний AI-аналіз</li><li>Поведінкові патерни</li><li>Повний звіт</li></ul>
<a href="/register" class="btn">Почати</a></div>
</div>
</div></section>

<section class="article-promo"><div class="container">
<div class="promo-card">
<span class="promo-badge">📚</span>
<h2>Чому з одними людьми легко, а з іншими важко?</h2>
<p>Один і той ж факт люди сприймають по-різному. Це не характер — це метапрограми мислення. В статті за 5 хвилин розберемось, чому так.</p>
<a href="/about-method" class="btn">Читати статтю →</a>
</div>
</div></section>
<section id="faq"><div class="container" style="max-width:820px">
<h2>Поширені запитання</h2>
<details><summary>Що таке MetaProfile і кому це підходить?</summary><p>MetaProfile — онлайн-сервіс психологічного тестування кандидатів з AI-аналізом. Підходить HR-фахівцям, рекрутерам, психологам, керівникам команд і власникам бізнесу.</p></details>
<details><summary>Скільки часу займає тестування?</summary><p>Кандидат проходить тест приблизно за 15 хвилин. Звіт формується одразу після завершення.</p></details>
<details><summary>Скільки коштує один тест?</summary><p>Базовий — 99 грн, Розширений — 249 грн, Повний — 499 грн. Без щомісячних абонплат, ви платите тільки за проведені тести.</p></details>
<details><summary>Чим AI-аналіз кращий за традиційні тести?</summary><p>AI обробляє відповіді без субʼєктивного людського фактору й одразу формує структурований звіт з рекомендаціями.</p></details>
<details><summary>Чи безпечні дані кандидатів?</summary><p>Так. Дані зберігаються на захищених серверах. Доступ до результатів має лише власник акаунта.</p></details>
<details><summary>Як отримати звіт після тестування?</summary><p>Звіт доступний у вашому особистому кабінеті одразу після завершення тесту.</p></details>
<details><summary>Чи можна провести тест для кількох кандидатів?</summary><p>Так. Кількість тестів не обмежена — оплата за кожен тест окремо.</p></details>
<details><summary>Як поповнити баланс?</summary><p>У розділі «Поповнити баланс» вказані банківські реквізити. Після оплати баланс зараховується протягом 1–2 годин.</p></details>
</div></section>
<section><div class="container" style="text-align:center">
<h2>Готові спробувати?</h2>
<p style="color:#555;margin-bottom:24px">Реєстрація безкоштовна. Перший тест — у подарунок.</p>
<a href="/register" class="btn">Створити акаунт</a>
</div></section>
<footer><div class="container">
<p><strong>MetaProfile</strong> — онлайн психологічне тестування кандидатів з AI-аналізом.</p>
<p style="margin-top:8px">© 2026 MetaProfile · <a href="/login">Вхід</a> · <a href="/register">Реєстрація</a></p>
</div></footer>
</body>
</html>"""


ABOUT_METHOD_HTML = r"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>Чому з одними людьми легко, а з іншими важко? — MetaProfile</title>
<meta name="description" content="Як метапрограми мислення пояснюють поведінку людей">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="https://www.metaprofile.online/about-method">
<style>
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0a0f1f;color:#e6edf7;line-height:1.7}
a{color:#9fb3ff}a:hover{color:#fff}
.wrap{max-width:760px;margin:0 auto;padding:48px 22px}
header.top{padding:18px 22px;border-bottom:1px solid rgba(255,255,255,.06)}
header.top .row{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}
header.top .logo{font-weight:700;color:#fff;text-decoration:none;font-size:18px}
header.top a.back{color:#9fb3ff;text-decoration:none;font-size:14px}
h1{font-size:34px;line-height:1.25;margin:0 0 12px;color:#fff}
.lead{font-size:18px;opacity:.85;margin:0 0 32px}
h2{font-size:22px;line-height:1.35;margin:36px 0 12px;color:#fff}
p{margin:0 0 16px;font-size:16px}
ul{padding-left:22px;margin:0 0 18px}
li{margin-bottom:8px}
.cta-box{margin:40px 0 0;padding:28px 24px;background:linear-gradient(135deg,#1a2540 0%,#0f1a30 100%);border:1px solid rgba(255,255,255,.08);border-radius:14px;text-align:center}
.cta-box .btn{display:inline-block;padding:12px 26px;background:#4a6cf7;color:#fff;text-decoration:none;border-radius:8px;font-weight:600;margin-top:8px}
.cta-box .btn:hover{background:#5a7cff}
@media (max-width:640px){h1{font-size:26px}.lead{font-size:16px}h2{font-size:19px}.wrap{padding:32px 18px}}
</style>
</head>
<body>
<header class="top"><div class="row"><a class="logo" href="/">MetaProfile</a><a class="back" href="/">← На головну</a></div></header>
<article class="wrap">
<h1>Чому з одними людьми легко, а з іншими важко?</h1>
<p class="lead">Як метапрограми мислення пояснюють поведінку людей.</p>
<p>Ви помічали, що з одними людьми ви  розумієтесь з півслова, а з іншими — ніби говорите різними мовами? Справа не в характері. Справа в тому, як людина обробляє інформацію.</p>
<h2>Метапрограми — фільтри сприйняття</h2>
<p>Метапрограми — це стійкі патерни того, як людина фільтрує реальність. Вони визначають, на що людина звертає увагу, як приймає рішення, що ј мотивує.</p>
<h2>Чотири ключові типи</h2>
<p>У кожного людини є свої домінуючі фільтри. Ось чотири найважливіших и тих, що визначають, чи легко вам буде з людиною чи нітч :</p>
<ul>
<li>Мотивація: людина поглинає успіхом чи існує проблеми ? Якщо вона эхільний оптиміст — вам легко. Якщо вона негативно налаштована — вам важко.</li>
<li>Референтна інформація: хтось довіряє лише собі, хтось іншим. Це впливає на те, як людина сприймає рішення.</li>
<li>Стиль роботи: самостійно чи в команді. одним потрібе хоче чіткі інструкції, іншим — свободи дій.</li>
</ul>
<h2>Це не типизація. Це опис</h2>
<p>Метапрограми не оцінюють людину як хорошу чи погану. Вони показують, як особа опрацьовує інформацію. Це не гарне чи погане — це просто інше.</p>
<h2>Як це допомагає в житті</h2>
<p>Коли ви розумієте метапрограми людини — ви перестаєте очікувати, що вона буде такою ж, як ви. Ви починаєте говорити на її мові. Це знимає тісну і конфлікти.</p>
<h2>В бізнесі та підборі персоналу</h2>
<p>Коли компанія наймає людину на позицію — головний ризик не в навичках. Головний ризик — людина не вписується в команду. Це не прохідний. Це глибокий конфлікт.</p>
<h2>Як це працює на практиці</h2>
<p>MetaProfile визначає ключові метапрограми людини через тест. Ви отримуєте звіт — не жаргон і не характеристики, а конкретні підходи. Як говорити. Як мотивувати. Як давати зворотний звязок.</p>
<div class="cta-box">
<p style="margin:0 0 6px;font-size:17px">Спробувати на собі</p>
<a class="btn" href="/register">Створити акаунт безкоштовно</a>
</div>
</article>
</body>
</html>"""

ROBOTS_TXT = (
    "User-agent: *\n"
    "Allow: /\n"
    "Disallow: /dashboard\n"
    "Disallow: /test\n"
    "Disallow: /history\n"
    "Disallow: /admin\n"
    "Disallow: /billing\n"
    "Disallow: /generate_questions\n"
    "Disallow: /transcribe\n"
    "Disallow: /run_analyze\n"
    "\n"
    "Sitemap: https://www.metaprofile.online/sitemap.xml\n"
)


def build_sitemap_xml():
    base = "https://www.metaprofile.online"
    today = datetime.utcnow().strftime("%Y-%m-%d")
    urls = [
        (base + "/", "1.0", "weekly"),
        (base + "/login", "0.5", "monthly"),
        (base + "/register", "0.7", "monthly"),
        (base + "/about-method", "0.8", "monthly"),
    ]
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio, freq in urls:
        parts.append(
            "<url><loc>" + loc + "</loc>"
            "<lastmod>" + today + "</lastmod>"
            "<changefreq>" + freq + "</changefreq>"
            "<priority>" + prio + "</priority></url>"
        )
    parts.append("</urlset>")
    return "\n".join(parts)


def register_seo_routes(app):
    """Register /robots.txt and /sitemap.xml on the given Flask app."""

    @app.route("/robots.txt")
    def robots_txt():
        return Response(ROBOTS_TXT, mimetype="text/plain")

    @app.route("/about-method")
    def about_method():
        return Response(ABOUT_METHOD_HTML, mimetype="text/html")

    @app.route("/sitemap.xml")
    def sitemap_xml():
        return Response(build_sitemap_xml(), mimetype="application/xml")

    return app
