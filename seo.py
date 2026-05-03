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
.hero-extra-link{margin-top:18px;font-size:15px}
.hero-extra-link a{color:#1a3a8f;text-decoration:none;border-bottom:1px solid rgba(26,58,143,.35);padding-bottom:1px;font-weight:500}
.hero-extra-link a:hover{color:#0b1f5c;border-color:#0b1f5c}
.article-promo{padding:56px 0;background:#f7f5f0}
.article-promo .promo-card{max-width:760px;margin:0 auto;padding:36px 32px;background:#fff;border:1px solid #e6e2d8;border-radius:16px;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.article-promo .promo-badge{display:inline-block;font-size:34px;margin-bottom:6px;line-height:1}
.article-promo h2{margin:6px 0 14px;font-size:24px;line-height:1.35;color:#1a1a1a}
.article-promo p{margin:0 0 22px;font-size:16px;color:#4a4a4a;line-height:1.6}
.article-promo .btn{display:inline-block;padding:13px 30px;background:#111;color:#fff;border-radius:10px;text-decoration:none;font-weight:600;transition:transform .15s,background .2s}
.article-promo .btn:hover{background:#000;transform:translateY(-1px)}
@media (max-width:640px){.article-promo{padding:36px 0}.article-promo .promo-card{padding:26px 20px}.article-promo h2{font-size:20px}}

#report-what{padding:60px 0;background:#fafaf7}
#report-what h2{text-align:center;margin:0 0 8px}
#report-what .section-sub{text-align:center;font-size:16px;color:#555;margin:0 auto 32px;max-width:640px}
.report-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;max-width:1080px;margin:0 auto}
.report-card{background:#fff;border:1px solid #e8e4d8;border-radius:14px;padding:24px 22px;transition:transform .15s,box-shadow .2s}
.report-card:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(0,0,0,.06)}
.report-card .rc-icon{font-size:28px;margin-bottom:10px;line-height:1}
.report-card h3{margin:0 0 8px;font-size:17px;color:#111;font-weight:600;line-height:1.3}
.report-card p{margin:0;font-size:14px;color:#555;line-height:1.55}
.report-cta{text-align:center;margin-top:30px}
.btn-ghost{display:inline-block;padding:12px 26px;background:transparent;color:#111;border:1.5px solid #111;border-radius:10px;text-decoration:none;font-weight:600;transition:all .2s}
.btn-ghost:hover{background:#111;color:#fff}
.disclaimer-section{padding:30px 0 0;background:#fff}
.disclaimer-card{max-width:760px;margin:0 auto;display:flex;gap:16px;align-items:flex-start;padding:18px 22px;background:#f4f6fb;border-left:3px solid #4a6cf7;border-radius:8px}
.disclaimer-card .disc-icon{font-size:20px;line-height:1;flex-shrink:0;margin-top:2px}
.disclaimer-card p{margin:0;font-size:14px;color:#3a4456;line-height:1.6}
@media (max-width:640px){ #report-what{padding:40px 0}.report-grid{grid-template-columns:1fr}}

.price.featured{position:relative;border:2px solid #4a6cf7;transform:scale(1.03)}
.price.featured .popular-badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#4a6cf7;color:#fff;padding:4px 14px;border-radius:999px;font-size:12px;font-weight:700;letter-spacing:.3px;white-space:nowrap}
@media (max-width:760px){.price.featured{transform:none}}

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
<h1>Зрозумійте, як працювати<br>з кандидатом — ще до найму</h1>
<p class="lead">Структурований звіт на основі відповідей кандидата: як він приймає рішення, що його мотивує, як давати задачі і де можуть бути ризики.</p>
<a href="/register" class="btn">Створити акаунт безкоштовно</a>
<a href="#how" class="btn secondary">Як це працює</a>
<p class="hero-extra-link"><a href="/sample-report">Подивитись приклад звіту →</a></p>
<p class="hero-extra-link"><a href="/about-method">Не впевнені? Прочитайте за 5 хвилин чому це працює →</a></p>
<p class="free-badge" style="margin-top:18px;color:#666;font-size:0.95em">🎁 Перший тест — безкоштовно. Реєстрація — лише email.</p>
</div></section>

<section id="report-what"><div class="container">
<h2>Що ви отримаєте у звіті</h2>
<p class="section-sub">Не „тест з оцінкою“, а практичні підказки для роботи з людиною.</p>
<div class="report-grid">
<div class="report-card"><div class="rc-icon">🧭</div><h3>Як людина приймає рішення</h3><p>Швидко чи обережно. Самостійно чи чекає підтвердження. Як реагує на тиск і дедлайни.</p></div>
<div class="report-card"><div class="rc-icon">⚡</div><h3>Що її мотивує</h3><p>Гроші, визнання, стабільність чи нові виклики. Шо триматиме на итривалому горизонті.</p></div>
<div class="report-card"><div class="rc-icon">💬</div><h3>Як з нею працювати</h3><p>Стиль комунікації, формат задач, тип контролю. Як говорити зокрема з цією людиною.</p></div>
<div class="report-card"><div class="rc-icon">⚠️</div><h3>Потенційні ризики</h3><p>Де може бути розчарування. Що варто перевірити на співбесіді чи в іспитному терміні.</p></div>
<div class="report-card"><div class="rc-icon">🔄</div><h3>Як давати зворотний зв’язок</h3><p>Як хвалити і як критикувати, щоби людина почула — і хотіла змінюватись.</p></div>
</div>
<div class="report-cta"><a href="/sample-report" class="btn-ghost">Подивитись приклад звіту</a></div>
</div></section>
<section id="why"><div class="container">
<h2>Чому HR обирають MetaProfile</h2>
<div class="grid">
<div class="card"><h3>Економія часу</h3><p>Замість 2-годинної співбесіди з психологом — структурований AI-звіт за 15 хвилин. Працює 24/7 без черг.</p></div>
<div class="card"><h3>Обʼєктивність</h3><p>AI обробляє відповіді за єдиним алгоритмом — без впливу настрою, симпатій чи втоми. Кожен кандидат отримує одну й ту ж шкалу оцінки.</p></div>
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
<div class="card"><h3>🛍️ Підбір менеджера з продажу</h3><p>Власник магазину перевіряє 5 кандидатів за вечір замість тижня співбесід. Отримує обʼєктивний профіль: стресостійкість, мотивація, схильність до маніпуляцій — і бачить потенційні ризики ще до фінального рішення.</p></div>
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

<section class="disclaimer-section"><div class="container">
<div class="disclaimer-card">
<div class="disc-icon">ℹ️</div>
<p>MetaProfile не ставить діагнози і не замінює співбесіди. Це інструмент, який допомагає краще підготуватись до розмови, побачити ризики і адаптувати управління.</p>
</div>
</div></section>
<section id="prices"><div class="container">
<h2>Тарифи</h2>
<p style="text-align:center;background:#fff7e6;border:1px solid #ffd591;border-radius:12px;padding:14px 20px;max-width:560px;margin:0 auto 28px;color:#874d00"><strong>🎁 Спробуйте безкоштовно:</strong> 1 тест у подарунок при реєстрації — без картки.</p>
<div class="prices">
<div class="price"><h3>Базовий</h3><div class="amount">99 грн</div><p>За один тест</p>
<ul><li>Основний особистісний профіль</li><li>AI-аналіз відповідей</li><li>Звіт онлайн</li></ul>
<a href="/register" class="btn">Почати</a></div>
<div class="price featured"><div class="popular-badge">Найпопулярніше</div><h3>Розширений</h3><div class="amount">249 грн</div><p>За один тест</p>
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
<p>Ви помічали, що з одними людьми ви розумієтесь з півслова, а з іншими — ніби говорите різними мовами? Справа не в характері. Справа в тому, як людина обробляє інформацію.</p>
<h2>Метапрограми — фільтри сприйняття</h2>
<p>Метапрограми — це стійкі патерни того, як людина фільтрує реальність. Вони визначають, на що людина звертає увагу, як приймає рішення і що її мотивує.</p>
<h2>Чотири ключові типи</h2>
<p>У кожної людини є свої домінуючі фільтри. Ось чотири з них, які найбільше впливають на те, чи легко вам буде з людиною знайти спільну мову:</p>
<ul>
<li>Мотивація: людина прагне успіху чи уникає проблем? Якщо це людина-оптиміст, орієнтована на досягнення — з нею легко працювати разом. Якщо вона уникає невдач — потрібено інший підхід.</li>
<li>Референція: хтось довіряє лише власному досвіду, хтось — думці інших. Це впливає на те, як людина приймає рішення.</li>
<li>Стиль роботи: самостійно чи в команді. Одним потрібні чіткі інструкції, іншим — свобода дій. Одні працюють краще на самоті, інші — серед людей.</li>
</ul>
<h2>Це не типізація — це опис</h2>
<p>Метапрограми не оцінюють людину як хорошу чи погану. Вони показують, як саме людина опрацьовує інформацію. Це не «правильно» чи «неправильно» — це просто інакше.</p>
<h2>Як це допомагає в житті</h2>
<p>Коли ви розумієте метапрограми людини — ви перестаєте очікувати, що вона буде такою ж, як ви. Ви починаєте говорити її мовою. Це знімає напругу і конфлікти у спілкуванні.</p>
<h2>В бізнесі та підборі персоналу</h2>
<p>Коли компанія наймає людину на позицію — головний ризик не в навичках. Головний ризик у тому, що людина не впишеться в команду чи культуру. Це не дрібниця. Це глибокий конфлікт, який коштує грошей і часу.</p>
<h2>Як це працює на практиці</h2>
<p>MetaProfile визначає ключові метапрограми людини через тест. Ви отримуєте звіт — не жаргон і не ярлики, а конкретні підказки: як з людиною говорити, як її мотивувати, як давати зворотний зв’язок, на що звертати увагу.</p>
<div class="cta-box">
<p style="margin:0 0 6px;font-size:17px">Спробувати на собі</p>
<a class="btn" href="/register">Створити акаунт безкоштовно</a>
</div>
</article>
</body>
</html>"""

SAMPLE_REPORT_HTML = r"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>Приклад звіту — МetaProfile</title>
<meta name="description" content="Так виглядає реальний звіт після тестування">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://www.metaprofile.online/sample-report">
<style>
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#fafaf7;color:#1a1a1a;line-height:1.65}
a{color:#1a3a8f}
header.top{padding:18px 22px;background:#fff;border-bottom:1px solid #eee}
header.top .row{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}
header.top .logo{font-weight:700;color:#111;text-decoration:none;font-size:18px}
header.top a.back{color:#1a3a8f;text-decoration:none;font-size:14px}
.demo-banner{background:#fff8e1;border-bottom:1px solid #ffe082;padding:10px 22px;text-align:center;font-size:14px;color:#7a5a00}
.report{max-width:820px;margin:0 auto;padding:32px 22px 60px}
h1{font-size:30px;margin:0 0 6px;color:#111}
.lead{color:#555;margin:0 0 22px;font-size:15px}
.meta-card{background:#fff;border:1px solid #e8e4d8;border-radius:12px;padding:18px 22px;margin-bottom:22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}
.meta-card .item .lbl{color:#888;font-size:12px;text-transform:uppercase;letter-spacing:.4px;margin-bottom:2px}
.meta-card .item .val{color:#111;font-weight:600;font-size:15px}
.section{background:#fff;border:1px solid #e8e4d8;border-radius:12px;padding:24px 26px;margin-bottom:18px}
.section h2{margin:0 0 12px;font-size:19px;color:#111;display:flex;align-items:center;gap:10px}
.section h2 .num{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;background:#4a6cf7;color:#fff;border-radius:50%;font-size:14px;font-weight:700}
.section p{margin:0 0 12px;font-size:15px;color:#333}
.section ul{margin:8px 0 0;padding-left:22px}
.section li{margin-bottom:6px;font-size:15px;color:#333}
.rec-box{margin-top:12px;padding:12px 16px;background:#eef3ff;border-left:3px solid #4a6cf7;border-radius:6px;font-size:14px;color:#1a3a8f}
.cta-final{margin-top:30px;padding:30px 26px;background:#111;color:#fff;border-radius:14px;text-align:center}
.cta-final h3{margin:0 0 8px;font-size:22px;color:#fff}
.cta-final p{margin:0 0 18px;font-size:15px;opacity:.85}
.cta-final .btn{display:inline-block;padding:13px 30px;background:#fff;color:#111;text-decoration:none;border-radius:10px;font-weight:600}
@media (max-width:640px){h1{font-size:24px}.section{padding:18px 18px}}

.score-row{display:flex;align-items:center;gap:12px;margin:6px 0 14px}
.score-bar{flex:1;height:10px;background:#eee;border-radius:6px;overflow:hidden}
.score-fill{height:100%;background:linear-gradient(90deg,#4a6cf7,#7a8cff);border-radius:6px}
.score-label{font-size:13px;color:#555;min-width:120px}
.score-value{font-size:13px;color:#111;font-weight:600;min-width:40px;text-align:right}
.quote{margin:10px 0;padding:10px 14px;background:#f7f5ee;border-left:3px solid #c9b87a;border-radius:6px;font-style:italic;color:#5a4a1a;font-size:14px}
.tag-row{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 14px}
.tag{background:#eef3ff;color:#1a3a8f;padding:4px 10px;border-radius:14px;font-size:12px;font-weight:500}
.fit{display:flex;align-items:center;gap:14px;background:linear-gradient(135deg,#1a3a8f,#4a6cf7);color:#fff;padding:18px 22px;border-radius:12px;margin:18px 0}
.fit-num{font-size:42px;font-weight:800;line-height:1}
.fit-text strong{display:block;font-size:16px;margin-bottom:4px}
.fit-text span{font-size:13px;opacity:.9}
.section h3.sub{margin:14px 0 6px;font-size:15px;color:#111}
.warn{background:#fff5f0;border-left:3px solid #e57373;padding:10px 14px;border-radius:6px;font-size:14px;color:#7a3a1a;margin:8px 0}
</style>
</head>
<body>
<header class="top"><div class="row"><a class="logo" href="/">MetaProfile</a><a class="back" href="/">← На головну</a></div></header>
<div class="demo-banner">📋 Так виглядає реальний звіт після тестування</div>
<main class="report">
<h1>Приклад звіту</h1>
<p class="lead">Це демо-звіт на основі вигаданого кандидата. Реальні звіти мають таку саму структуру і глибину аналізу.</p>
<div class="meta-card">
<div class="item"><div class="lbl">Кандидат</div><div class="val">Олена К.</div></div>
<div class="item"><div class="lbl">Позиція</div><div class="val">Менеджер з продажу</div></div>
<div class="item"><div class="lbl">Дата тестування</div><div class="val">15.04.2026</div></div>
<div class="item"><div class="lbl">Формат</div><div class="val">Розширений</div></div>
</div>

<div class="fit">
<div class="fit-num">78<span style="font-size:20px;opacity:.8">/100</span></div>
<div class="fit-text"><strong>Загальна відповідність позиції</strong><span>Кандидатка добре підходить для ролі менеджера з продажу з помірними застереженнями щодо стресостійкості.</span></div>
</div>
<div class="tag-row">
<span class="tag">Швидке прийняття рішень</span>
<span class="tag">Орієнтація на результат</span>
<span class="tag">Потреба в структурі</span>
<span class="tag">Чутлива до визнання</span>
<span class="tag">Середня стресостійкість</span>
</div>

<section class="section"><h2><span class="num">1</span>Як приймає рішення</h2>
<p>Олена приймає рішення швидко та інтуїтивно, спираючись на власний досвід більше, ніж на формальний аналіз. Це допомагає в динамічних комерційних ситуаціях, але може створювати слабкі місця у командній роботі, де потрібне обґрунтування вибору.</p>
<div class="score-row"><div class="score-label">Швидкість</div><div class="score-bar"><div class="score-fill" style="width:85%"></div></div><div class="score-value">85%</div></div>
<div class="score-row"><div class="score-label">Аналітичність</div><div class="score-bar"><div class="score-fill" style="width:42%"></div></div><div class="score-value">42%</div></div>
<div class="score-row"><div class="score-label">Опора на дані</div><div class="score-bar"><div class="score-fill" style="width:38%"></div></div><div class="score-value">38%</div></div>
<div class="score-row"><div class="score-label">Готовність делегувати</div><div class="score-bar"><div class="score-fill" style="width:55%"></div></div><div class="score-value">55%</div></div>
<div class="quote">«Я зазвичай відразу бачу, як людина буде реагувати. Не люблю довгих обговорень — краще спробувати і скоригувати» — відповідь кандидатки на відкрите запитання.</div>
<div class="rec-box"><strong>Рекомендація:</strong> не тисніть довгим аналізом і багатоповерховими викладами. Дайте короткий контекст і очікуйте рішення протягом 1–2 годин. Для важливих рішень додавайте чеклист критеріїв — це компенсує низьку схильність до формального аналізу.</div>
</section>

<section class="section"><h2><span class="num">2</span>Що мотивує</h2>
<p>Головні драйвери Олени — визнання результатів, стабільність та чіткі правила гри. Гроші важливі, але не є єдиним драйвером — вони працюють як гігієнічний фактор. Конкуренція через агресію може демотивувати — кандидатка очікує справедливих правил і прозорої системи премій.</p>
<h3 class="sub">Мапа мотиваційних пріоритетів</h3>
<div class="score-row"><div class="score-label">Визнання / статус</div><div class="score-bar"><div class="score-fill" style="width:88%"></div></div><div class="score-value">88%</div></div>
<div class="score-row"><div class="score-label">Стабільність</div><div class="score-bar"><div class="score-fill" style="width:74%"></div></div><div class="score-value">74%</div></div>
<div class="score-row"><div class="score-label">Кар’єрний ріст</div><div class="score-bar"><div class="score-fill" style="width:62%"></div></div><div class="score-value">62%</div></div>
<div class="score-row"><div class="score-label">Приналежність до команди</div><div class="score-bar"><div class="score-fill" style="width:55%"></div></div><div class="score-value">55%</div></div>
<div class="score-row"><div class="score-label">Грошова винагорода</div><div class="score-bar"><div class="score-fill" style="width:48%"></div></div><div class="score-value">48%</div></div>
<div class="score-row"><div class="score-label">Автономія</div><div class="score-bar"><div class="score-fill" style="width:30%"></div></div><div class="score-value">30%</div></div>
<div class="rec-box"><strong>Рекомендація:</strong> покажіть чіткий кар’єрний трек і прозорі KPI з преміями. Уникайте грошових провокацій на інтерв’ю («а якщо ми дамо на 30% менше») — це знижує довіру. Публічне визнання на зустрічах команди розблокує додаткову мотивацію.</div>
</section>

<section class="section"><h2><span class="num">3</span>Стиль роботи в команді</h2>
<p>Олена комфортніше почуває себе у малих командах (3–6 осіб) із чіткими ролями. Схильна брати на себе відповідальність за свою ділянку, але неохоче лізе у «чужі» зони. Наради без чіткої повістки сприймає як витрату часу.</p>
<h3 class="sub">Комунікація</h3>
<ul>
<li>Пряма, лаконічна. Не любить довгих листів без конкретики.</li>
<li>Відповідає швидко в месенджерах, довше в електронній пошті.</li>
<li>Не боїться відкрито озвучити незгоду, але очікує взаємної поваги.</li>
</ul>
<h3 class="sub">Роль у взаємодії</h3>
<p>Частіше бере роль «виконавця-драйвера»: рухає процес до результату. Не претендує на лідерство в колективі, але очікує, що її експертизу будуть враховувати при прийнятті рішень.</p>
</section>

<section class="section"><h2><span class="num">4</span>Як з нею працювати</h2>
<ul>
<li><strong>Ставте вимірні цілі та дедлайни.</strong> Чим конкретніший результат — тим вища включеність. Розмиті формулювання («попрацюй над якістю») будуть ігноруватися.</li>
<li><strong>Давайте ініціативу в межах процесу.</strong> Повна свобода без рамок викликає тривогу. Оптимально: 70% процесу фіксований, 30% — для власних рішень.</li>
<li><strong>Регулярний фідбек (1 раз на 2 тижні).</strong> Без підтвердження результатів поступово втрачає енергію.</li>
<li><strong>У конфліктах — пауза.</strong> Не втягуйте в емоційну дискусію. Дайте 24 години на обдумування — повертається з конструктивними рішеннями.</li>
<li><strong>Делегування «вгору».</strong> Охоче бере на себе операційні завдання, гірше — стратегічні без контексту.</li>
</ul>
</section>

<section class="section"><h2><span class="num">5</span>Потенційні ризики</h2>
<p>Нижче — сценарії, в яких сильні сторони Олени можуть працювати проти неї. Це не діагноз, а зони підвищеної уваги.</p>
<div class="warn"><strong>Вигорання при частій зміні пріоритетів.</strong> Якщо компанія регулярно змінює квартальні цілі без пояснень — втратить включеність протягом 2–3 місяців.</div>
<div class="warn"><strong>Перфекціонізм у простих задачах.</strong> Може надто довго допрацьовувати дрібниці замість того, щоб рухатися далі.</div>
<div class="warn"><strong>Реакція на публічну критику.</strong> Жорсткий фідбек при колегах знижує лояльність довше, ніж у середнього працівника. Краще виносити критику у форматі 1-на-1.</div>
<div class="warn"><strong>Опір процесам «зверху».</strong> Нові регламенти без пояснення вигод будуть виконуватися формально.</div>
</section>

<section class="section"><h2><span class="num">6</span>Як давати зворотний зв’язок</h2>
<p>Олена добре сприймає критику, якщо вона конкретна і супроводжується рекомендаціями. Уникайте загальних оцінок («ти розумний співробітник», «ти над цим не допрацювала») — вони сприймаються як фальшиві або суб’єктивні.</p>
<h3 class="sub">Шаблон фідбеку</h3>
<ul>
<li><strong>Факт:</strong> що саме відбулося (без інтерпретації).</li>
<li><strong>Вплив:</strong> до чого це призвело для команди або результату.</li>
<li><strong>Очікування:</strong> як би ви хотіли, щоб вона діяла наступного разу.</li>
<li><strong>Підтримка:</strong> який ресурс компанія дає для змін.</li>
</ul>
<p>Формат 1-на-1, без свідків, ранок або перша половина дня. Під кінець тижня реакції на важливий фідбек будуть різкішими.</p>
</section>

<section class="section"><h2><span class="num">7</span>Перші 90 днів: як ввести в роль</h2>
<h3 class="sub">Тижні 1–2</h3>
<ul>
<li>Чітко описати зону відповідальності та ключових стейкхолдерів.</li>
<li>Познайомити з продуктовою базою та дати доступ до CRM без «перевірки лояльності».</li>
<li>Призначити ментора з досвідом понад 2 роки в компанії.</li>
</ul>
<h3 class="sub">Місяць 2</h3>
<ul>
<li>Дати перший самостійний проект з вимірним результатом (напр. «відпрацювати 30 лідів з визначеної бази»).</li>
<li>Визначити перший «quick win» для публічного визнання на командній зустрічі.</li>
<li>Провести калібрувальний фідбек-сесію (45 хв) про сильні сторони та зони росту.</li>
</ul>
<h3 class="sub">Місяць 3</h3>
<ul>
<li>Перевести на повний KPI-план з премією.</li>
<li>Зафіксувати «карту розвитку» на 6–12 місяців (зрозумілі критерії просування).</li>
<li>Обговорити «червоні прапорці» прямо: що вас може справді демотивувати.</li>
</ul>
</section>

<section class="section"><h2><span class="num">8</span>Короткий підсумок</h2>
<p><strong>Сильні сторони:</strong> швидкість рішень, орієнтація на результат, відповідальність за свою ділянку, пряма комунікація.</p>
<p><strong>Зони уваги:</strong> потреба в структурі та визнанні, середня стресостійкість при жорсткій публічній критиці, опір «процесам зверху» без пояснень.</p>
<p><strong>Рекомендація:</strong> підходить для позиції з чіткими KPI та прозорою кар’єрною драбиною. Перед офером — фінальне інтерв’ю з керівником відділу.</p>
</section>

<section class="section" style="background:#fffbe6;border-color:#f3e1a8">
<h2 style="color:#7a5a00"><span class="num" style="background:#c9a227">i</span>Важливо</h2>
<p style="color:#5a4a1a;font-size:14px">Цей звіт — допоміжний інструмент для HR та керівників, а не психологічний діагноз. Рішення про найм має завжди включати інтерв’ю, перевірку досвіду та рекомендації. Результати можуть змінюватися залежно від контексту та життєвої ситуації кандидата.</p>
</section>

<div class="cta-final"><h3>Протестуйте на собі чи кандидаті</h3><p>Перший тест — безкоштовно. Отримаєте такий самий звіт по вашому кандидату.</p><a class="btn" href="/register">Створити акаунт безкоштовно</a></div>
</main>
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
        (base + "/sample-report", "0.7", "monthly"),
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

    @app.route("/sample-report")
    def sample_report():
        return Response(SAMPLE_REPORT_HTML, mimetype="text/html")

    @app.route("/sitemap.xml")
    def sitemap_xml():
        return Response(build_sitemap_xml(), mimetype="application/xml")

    return app
