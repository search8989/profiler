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
<a href="/register" class="cta">Спробувати</a>
</nav>
</div></header>
<section class="hero"><div class="container">
<span class="tagline">AI-аналіз за 15 хвилин</span>
<h1>Психологічний профіль кандидата<br>онлайн за 15 хвилин</h1>
<p class="lead">MetaProfile — AI-платформа для психологічного тестування кандидатів та оцінки персоналу. Об\u0027єктивний звіт про сильні сторони, мотивацію та ризики — без багатогодинних співбесід.</p>
<a href="/register" class="btn">Створити акаунт безкоштовно</a>
<a href="#how" class="btn secondary">Як це працює</a>
</div></section>
<section id="why"><div class="container">
<h2>Чому HR обирають MetaProfile</h2>
<div class="grid">
<div class="card"><h3>Економія часу</h3><p>Замість 2-годинної співбесіди з психологом — структурований AI-звіт за 15 хвилин. Працює 24/7 без черг.</p></div>
<div class="card"><h3>Об\u0027єктивність</h3><p>AI аналізує відповіді без упередженості, симпатій чи втоми. Результат однаковий для всіх кандидатів.</p></div>
<div class="card"><h3>Доступна ціна</h3><p>Від 99 грн за тест замість тисяч гривень за консультацію психолога. Платите тільки за фактичні тести.</p></div>
<div class="card"><h3>Готовий звіт</h3><p>Професійний звіт із сильними сторонами, ризиками та рекомендаціями. Можна додати до досьє кандидата.</p></div>
<div class="card"><h3>Зменшення помилок найму</h3><p>За дослідженнями, помилка найму коштує бізнесу значних сум. Об\u0027єктивний скринінг суттєво знижує цей ризик.</p></div>
<div class="card"><h3>Повністю онлайн</h3><p>Кандидат проходить тест із будь-якого пристрою. Ви отримуєте звіт у своєму кабінеті MetaProfile.</p></div>
</div>
</div></section>
<section id="how"><div class="container">
<h2>Як це працює</h2>
<div class="steps">
<div class="step"><h3>1. Реєстрація</h3><p>Створіть безкоштовний акаунт за хвилину — потрібен лише email.</p></div>
<div class="step"><h3>2. Поповнення</h3><p>Поповніть баланс на потрібну суму. Один тест — від 99 грн.</p></div>
<div class="step"><h3>3. Тестування</h3><p>Запустіть тест. Кандидат проходить його онлайн за 15 хвилин.</p></div>
<div class="step"><h3>4. Звіт</h3><p>Отримайте AI-звіт з профілем кандидата у своєму кабінеті.</p></div>
</div>
</div></section>
<section id="cases"><div class="container">
<h2>Сценарії використання</h2>
<div class="grid">
<div class="card"><h3>Підбір у малий бізнес</h3><p>Власник магазину чи кав\u0027ярні замість інтуїтивного «здається, гарна людина» отримує об\u0027єктивний профіль і знижує ризик хибного найму.</p></div>
<div class="card"><h3>HR-відділи компаній</h3><p>Команда рекрутерів використовує MetaProfile як перший фільтр у воронці. На очну співбесіду доходять лише кандидати з відповідним профілем.</p></div>
<div class="card"><h3>Психологи та коучі</h3><p>Приватні фахівці використовують сервіс для попередньої діагностики клієнтів — швидко формують гіпотези й готуються до сесії якісніше.</p></div>
</div>
</div></section>
<section id="prices"><div class="container">
<h2>Тарифи</h2>
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
<section id="faq"><div class="container" style="max-width:820px">
<h2>Поширені запитання</h2>
<details><summary>Що таке MetaProfile і кому це підходить?</summary><p>MetaProfile — онлайн-сервіс психологічного тестування кандидатів з AI-аналізом. Підходить HR-фахівцям, рекрутерам, психологам, керівникам команд і власникам бізнесу.</p></details>
<details><summary>Скільки часу займає тестування?</summary><p>Кандидат проходить тест приблизно за 15 хвилин. Звіт формується одразу після завершення.</p></details>
<details><summary>Скільки коштує один тест?</summary><p>Базовий — 99 грн, Розширений — 249 грн, Повний — 499 грн. Без щомісячних абонплат, ви платите тільки за проведені тести.</p></details>
<details><summary>Чим AI-аналіз кращий за традиційні тести?</summary><p>AI обробляє відповіді без суб\u0027єктивного людського фактору й одразу формує структурований звіт з рекомендаціями.</p></details>
<details><summary>Чи безпечні дані кандидатів?</summary><p>Так. Дані зберігаються на захищених серверах. Доступ до результатів має лише власник акаунта.</p></details>
<details><summary>Як отримати звіт після тестування?</summary><p>Звіт доступний у вашому особистому кабінеті одразу після завершення тесту.</p></details>
<details><summary>Чи можна провести тест для кількох кандидатів?</summary><p>Так. Кількість тестів не обмежена — оплата за кожен тест окремо.</p></details>
<details><summary>Як поповнити баланс?</summary><p>У розділі «Поповнити баланс» вказані банківські реквізити. Після оплати баланс зараховується протягом 1–2 годин.</p></details>
</div></section>
<section><div class="container" style="text-align:center">
<h2>Готові спробувати?</h2>
<p style="color:#555;margin-bottom:24px">Реєстрація безкоштовна. Перший тест — від 99 грн.</p>
<a href="/register" class="btn">Створити акаунт</a>
</div></section>
<footer><div class="container">
<p><strong>MetaProfile</strong> — онлайн психологічне тестування кандидатів з AI-аналізом.</p>
<p style="margin-top:8px">© 2026 MetaProfile · <a href="/login">Вхід</a> · <a href="/register">Реєстрація</a></p>
</div></footer>
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

    @app.route("/sitemap.xml")
    def sitemap_xml():
        return Response(build_sitemap_xml(), mimetype="application/xml")

    return app
