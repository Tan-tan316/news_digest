import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta
import os

# --- НАЛАШТУВАННЯ ---
EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")

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

# --- HTML ---
html = "<h1>📰 Мій дайджест новин</h1>"
for article in all_articles:
    html += f"<h3><a href='{article['link']}'>{article['title']}</a></h3>"
    html += f"<p>{article['source']} | {article['date']}</p>"
    html += "<hr>"

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