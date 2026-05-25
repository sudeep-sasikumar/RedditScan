# SubSight — Reddit Research Tool

## What is SubSight

A free Reddit research tool. You describe your research goal to Claude (in chat), Claude gives you a JSON config, you paste it in, SubSight scrapes Reddit and presents the results in a clean UI.

## Why No AI Inside the App

The app itself has no AI layer — keeping it completely free to run. The intelligence comes from your Claude.ai subscription used separately in a chat session.

## How to Use the AI Step

Open Claude.ai and send this message (edit the topic):

> "Give me SubSight JSON parameters to research pain points of UK tradesmen that could be solved by a mobile app or website. Return only the JSON in this exact format:
> ```json
> {
>   "subreddits": [...],
>   "search_queries": [...],
>   "filters": { "sort": "top", "time_filter": "year", "min_score": 5 },
>   "research_label": "..."
> }
> ```"

Then paste Claude's response into SubSight's JSON Mode input.

## Prerequisites

- Python 3.11+
- A free Reddit API account (instructions below)
- Claude.ai account (for generating search parameters — free tier works)

## Reddit API Setup

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app" at the bottom
3. Name: SubSight | Type: script | Redirect URI: http://localhost:8080
4. Click "create app"
5. `client_id` = short string directly under the app name
6. `client_secret` = the "secret" field

## Local Setup (Claude Code on Mobile)

```bash
git clone {your_repo}
cd subsight
cp .env.example .env
# Edit .env — fill in your 3 Reddit credentials
cd backend
pip install -r requirements.txt
python main.py
# Open http://localhost:8000 in your mobile browser
```

## Deploy to Hostinger VPS (Phase 2)

SSH into VPS, then:

```bash
git clone {your_repo}
cd subsight
cp .env.example .env && nano .env
docker-compose up -d
# Access at http://{your_vps_ip}:8000
```
