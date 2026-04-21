import feedparser
import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta
import anthropic

# --- НАЛАШТУВАННЯ ---
EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

# --- ДЖЕРЕЛА ---
all_feeds = {
    "Politico EU":      "https://www.politico.eu/feed/",
    "Politico Germany": "https://www.politico.eu/tag/german-politics/feed/",
    "Atlantic Council": "https://www.atlanticcouncil.org/feed/",
    "Politico UK":      "https://news.google.com/rss/search?q=site:politico.eu+uk&hl=en",
    "Politico France":  "https://news.google.com/rss/search?q=site:politico.eu+france&hl=en",
    "CFR":              "https://news.google.com/rss/search?q=site:cfr.org&hl=en",
    "Chatham House":    "https://news.google.com/rss/search?q=site:chathamhouse.org&hl=en",
    "Politico US":      "https://news.google.com/rss/search?q=site:politico.com&hl=en",
    "ISW":              "https://news.google.com/rss/search?q=site:understandingwar.org&hl=en",
}

# --- ЗБІР СТАТЕЙ ---
now = datetime.now(timezone.utc)
cutoff = now - timedelta(hours=24)
all_articles = []

for name, url in all_feeds.items():
    feed = feedparser.parse(url)
    for article in feed.entries:
        try:
            pub_date = datetime(*article.published_parsed[:6], tzinfo=timezone.utc)
            if pub_date >= cutoff:
                all_articles.append({
                    "source": name,
                    "title": article.title,
                    "link": article.link,
                    "date": article.published
                })
        except Exception:
            continue

print(f"Зібрано статей: {len(all_articles)}")

# --- AI РЕЗЮМУВАННЯ ---
articles_text = ""
for article in all_articles:
    articles_text += f"- {article['title']} ({article['source']})\n"

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=5000,
    messages=[
        {"role": "user", "content": f"""Ось список новинних заголовків за сьогодні:

{articles_text}

Згрупуй їх по темах (наприклад: Україна, Близький Схід, Політика ЄС, США і тд).
Для кожної групи напиши резюме українською. Загальний обсяг всіх резюме — не більше 10000 символів.
Розподіли їх між темами на свій розсуд — важливіші теми можуть отримати більше тексту, менш важливі — менше.
Формат відповіді — строго JSON:
{{
  "groups": [
    {{
      "topic": "Назва теми",
      "summary": "Резюме...",
      "articles": ["точний заголовок 1", "точний заголовок 2"]
    }}
  ]
}}
Повертай ТІЛЬКИ JSON, без зайвого тексту.
"""}
    ]
)

# --- ПАРСИНГ JSON ---
response_text = message.content[0].text
clean_text = response_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
data = json.loads(clean_text)

# --- HTML ---
links = {}
for article in all_articles:
    links[article["title"]] = article["link"]

html = """
<html>
<head>
<style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
    h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; }
    h2 { color: #2980b9; margin-top: 30px; }
    p { line-height: 1.6; color: #333; }
    ul { background: white; padding: 15px 30px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    li { margin: 8px 0; }
    a { color: #2980b9; text-decoration: none; }
    a:hover { text-decoration: underline; }
    hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
</style>
</head>
<body>
<h1>📰 Мій дайджест новин</h1>
"""

for group in data["groups"]:
    html += f"<h2>{group['topic']}</h2>"
    html += f"<p>{group['summary']}</p>"
    html += "<ul>"
    for title in group["articles"]:
        link = next((v for k, v in links.items() if title[:30] in k), "#")
        html += f"<li><a href='{link}'>{title}</a></li>"
    html += "</ul><hr>"

html += "</body></html>"

# --- ВІДПРАВКА ---
msg = MIMEMultipart("alternative")
msg["Subject"] = "📰 Дайджест новин"
msg["From"] = EMAIL
msg["To"] = EMAIL
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, EMAIL, msg.as_string())

print("Лист відправлено! ✅")
