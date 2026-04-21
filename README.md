# 📰 Daily News Digest

An automated news aggregator that collects articles from 9 geopolitical and policy sources, filters them by the last 24 hours, and delivers a daily HTML email digest.

## 🔍 What it does
- Fetches articles from 9 sources via RSS and Google News RSS
- Filters only articles published in the last 24 hours
- Formats them into a clean HTML email
- Sends automatically every morning via Gmail
- Runs on GitHub Actions — no server needed

## 📡 Sources
- Politico EU, UK, France, Germany
- Politico US
- Atlantic Council
- CFR (Council on Foreign Relations)
- Chatham House
- ISW (Institute for the Study of War)

## 🛠 Tech stack
- Python (feedparser, smtplib, datetime)
- GitHub Actions for scheduling
- Gmail SMTP for delivery

## 🔐 Configuration
Sensitive credentials (email, app password) are stored as GitHub Secrets and never hardcoded.

## 🚀 Planned improvements
- AI-powered summarization grouped by topic (Gemini / Claude API)
- Keyword filtering by areas of interest
