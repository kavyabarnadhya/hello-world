# UPSC News Digest

A Python script that fetches news from 7 India-focused sources, filters and summarizes UPSC-relevant articles using **Llama 3.3 70B via Groq**, and sends a beautifully formatted HTML email digest to your inbox every morning at 8:00 AM IST.

## What it does

- Fetches 3 articles each from 7 sources — **21 articles total** — across Indian national news, economy, governance, and international headlines
- Sends all articles to **Llama 3.3 70B** (via Groq) in a single API call for UPSC classification and sharp exam-focused summarization
- Filters out party politics, electoral rhetoric, and routine foreign news — keeps only substantive UPSC-relevant content
- Groups articles by topic in priority order: Polity & Governance → Economy → Social Issues → Environment & Ecology → Science & Technology → Security & Defence → History & Culture → International Relations
- Each topic section includes AI-generated **UPSC Exam Angles** (GS paper mapping, syllabus topics, exam themes)
- Each article summary is structured: core fact → specific act/article/scheme → data points → GS paper → exam implication
- Delivers a clean HTML email and runs automatically via GitHub Actions

## Sources

| Source | Focus |
|---|---|
| The Hindu (National) | Indian national news |
| Indian Express (India section) | Indian political & policy news |
| The Print | Indian politics & governance |
| LiveMint | Economy & markets |
| BBC World | Major international headlines |
| Economic Times (Economy & Policy) | Indian economic policy |
| DD News | Government announcements |

## Setup

### 1. Get a Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign in and navigate to **API Keys**
3. Click **Create API Key** and copy it

### 2. Generate a Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com)
2. Navigate to **Security** → enable **2-Step Verification** (required)
3. Go to **Security** → **2-Step Verification** → scroll down to **App passwords**
4. Select app: **Mail**, device: **Other** (name it "UPSC Digest"), click **Generate**
5. Copy the 16-character password shown

### 3. Add GitHub Secrets

In your GitHub repository go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret Name | Value |
|---|---|
| `SENDER_EMAIL` | Your Gmail address (e.g. `yourname@gmail.com`) |
| `SENDER_APP_PASSWORD` | The 16-character App Password from step 2 |
| `RECEIVER_EMAIL` | Email address(es) to receive the digest (comma-separated for multiple) |
| `GROQ_API_KEY` | Your Groq API key from step 1 |

The workflow runs automatically at **2:30 AM UTC (8:00 AM IST)** every day. You can also trigger it manually from the **Actions** tab → **Run UPSC News Digest** → **Run workflow**.

### 4. Run locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and fill in your real values

# Run the digest
python digest.py
```

## Project structure

```
upsc-news-digest/
├── digest.py                          # Main script
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable template
├── .gitignore                         # Ignores .env
├── README.md                          # This file
└── .github/
    └── workflows/
        └── daily_digest.yml           # GitHub Actions cron job
```

## Dependencies

- `feedparser` — RSS feed parsing
- `groq` — Groq API SDK (Llama 3.3 70B)
- `python-dotenv` — Local `.env` file loading
