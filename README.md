# 📰 Daily News Digest

Автоматизований агрегатор новин який збирає статті з 9 геополітичних джерел, фільтрує їх за останні 24 години та надсилає щоденний HTML-дайджест на пошту.

## 🔍 Що робить
- Збирає статті з 9 джерел через RSS та Google News RSS
- Фільтрує тільки статті опубліковані за останні 24 години
- Формує чистий HTML-лист
- Надсилає автоматично щоранку через Gmail
- Працює на GitHub Actions — без сервера

## 📡 Джерела
- Politico EU, UK, France, Germany
- Politico US
- Atlantic Council
- CFR (Council on Foreign Relations)
- Chatham House
- ISW (Institute for the Study of War)

## 🛠 Технології
- Python (feedparser, smtplib, datetime)
- GitHub Actions для автоматичного запуску
- Gmail SMTP для відправки

## 🔐 Безпека
Email та пароль зберігаються як GitHub Secrets і ніколи не hardcode-яться в коді.

## 🚀 Заплановані покращення
- AI-резюмування згруповане по темах (Claude API)
- Фільтрація по ключових словах
