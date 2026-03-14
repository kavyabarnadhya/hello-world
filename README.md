# UPSC News Digest

A Python script that automatically fetches news from top Indian and international sources, filters and summarizes UPSC-relevant articles using Google Gemini Flash, and sends a beautifully formatted HTML email digest to your Gmail inbox every morning.

## What it does

- Fetches up to 8 articles each from The Hindu, Indian Express, The Print, LiveMint, and BBC World
- Sends all articles to **Gemini 2.0 Flash** in a single API call for UPSC-topic classification and summarization
- Groups articles by UPSC topic: Polity & Governance, Economy, International Relations, Environment & Ecology, Science & Technology, Social Issues, History & Culture, Security & Defence
- Delivers a clean HTML email with topic-colored sections, article summaries, and UPSC exam angles
- Runs automatically every day at 8:00 AM IST via GitHub Actions

## Setup

### 1. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key

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
| `RECEIVER_EMAIL` | Email address to receive the digest |
| `GEMINI_API_KEY` | Your Gemini API key from step 1 |

The workflow runs automatically at **2:30 AM UTC (8:00 AM IST)** every day. You can also trigger it manually from the **Actions** tab → **UPSC Daily News Digest** → **Run workflow**.

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
- `google-genai` — Google Gemini API SDK
- `python-dotenv` — Local `.env` file loading
