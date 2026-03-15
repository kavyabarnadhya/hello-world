import os
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import collections
from datetime import datetime

import feedparser
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

FEEDS = {
    "The Hindu": "https://www.thehindu.com/news/feeder/default.rss",
    "Indian Express": "https://indianexpress.com/feed/",
    "The Print": "https://theprint.in/category/india/feed/",
    "LiveMint": "https://www.livemint.com/rss/news",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
}

TOPIC_COLORS = {
    "International Relations": "#c0392b",
    "Economy": "#27ae60",
    "Polity & Governance": "#2980b9",
    "Security & Defence": "#8e44ad",
    "History & Culture": "#d35400",
    "Environment & Ecology": "#16a085",
    "Social Issues": "#7f8c8d",
    "Science & Technology": "#2c3e50",
}

VALID_TOPICS = set(TOPIC_COLORS.keys()) | {"Not UPSC Relevant"}


def fetch_articles():
    articles = []
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:8]
            for entry in entries:
                summary = ""
                if hasattr(entry, "summary"):
                    summary = entry.summary
                elif hasattr(entry, "description"):
                    summary = entry.description
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": summary,
                    "source": source,
                })
            print(f"  [{source}] fetched {len(entries)} articles")
        except Exception as e:
            print(f"  [{source}] ERROR fetching feed: {e}")
    return articles


def classify_articles(articles):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    articles_text = ""
    for i, a in enumerate(articles):
        articles_text += (
            f"\n--- Article {i} ---\n"
            f"Title: {a['title']}\n"
            f"Source: {a['source']}\n"
            f"Summary: {a['summary'][:300]}\n"
        )

    prompt = f"""You are a UPSC exam preparation assistant. Analyze the following news articles and classify each one.

For each article return a JSON object with these fields:
- index: the article index number (int)
- topic: one of exactly these topics: {', '.join(sorted(TOPIC_COLORS.keys()))}, Not UPSC Relevant
- summary: 2-sentence plain English summary of the article
- upsc_angle: 1-line explanation of why this matters for UPSC exam preparation

Return ONLY a JSON array (no markdown, no code fences, no explanation) containing one object per article.
Drop articles that are "Not UPSC Relevant" — do not include them in the output at all.

Articles:
{articles_text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
            if raw.endswith("```"):
                raw = raw.rsplit("```", 1)[0]
            raw = raw.strip()

        classified = json.loads(raw)
    except Exception as e:
        print(f"ERROR in Groq classification: {e}")
        return []

    # Merge original article data back using index
    result = []
    for item in classified:
        idx = item.get("index")
        topic = item.get("topic", "")
        if topic == "Not UPSC Relevant" or topic not in TOPIC_COLORS:
            continue
        if idx is None or idx >= len(articles):
            continue
        original = articles[idx]
        result.append({
            "title": original["title"],
            "link": original["link"],
            "source": original["source"],
            "topic": topic,
            "summary": item.get("summary", ""),
            "upsc_angle": item.get("upsc_angle", ""),
        })
    return result


def render_html(grouped):
    today = datetime.now().strftime("%B %d, %Y")
    topics_present = list(grouped.keys())

    # Topic index bar
    index_bar_items = ""
    for topic in topics_present:
        color = TOPIC_COLORS[topic]
        anchor = topic.replace(" ", "-").replace("&", "and").lower()
        index_bar_items += (
            f'<a href="#{anchor}" style="display:inline-block;margin:4px;padding:6px 14px;'
            f'background:{color};color:#fff;border-radius:20px;text-decoration:none;'
            f'font-size:13px;font-weight:600;">{topic}</a>'
        )

    # Article sections
    sections_html = ""
    for topic in topics_present:
        color = TOPIC_COLORS[topic]
        anchor = topic.replace(" ", "-").replace("&", "and").lower()
        articles = grouped[topic]

        cards_html = ""
        for a in articles:
            cards_html += f"""
            <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;
                        padding:18px 20px;margin-bottom:16px;">
              <div style="margin-bottom:8px;">
                <a href="{a['link']}" style="font-size:17px;font-weight:700;color:#1a1a1a;
                   text-decoration:none;">{a['title']}</a>
              </div>
              <div style="margin-bottom:10px;">
                <span style="background:#f0f0f0;color:#555;font-size:12px;font-weight:600;
                             padding:3px 9px;border-radius:12px;">{a['source']}</span>
              </div>
              <p style="color:#444;font-size:14px;line-height:1.6;margin:0 0 12px 0;">
                {a['summary']}
              </p>
              <div style="background:#e8f4fd;border-left:4px solid #2980b9;
                          padding:10px 14px;border-radius:4px;margin-bottom:14px;">
                <span style="font-size:12px;font-weight:700;color:#2980b9;
                             text-transform:uppercase;letter-spacing:0.5px;">UPSC Angle</span>
                <p style="color:#1a3c5e;font-size:13px;margin:4px 0 0 0;line-height:1.5;">
                  {a['upsc_angle']}
                </p>
              </div>
              <a href="{a['link']}" style="color:{color};font-size:13px;font-weight:600;
                 text-decoration:none;">Read full article &rarr;</a>
            </div>"""

        sections_html += f"""
        <div id="{anchor}" style="margin-bottom:36px;">
          <h2 style="margin:0 0 16px 0;padding:12px 20px;background:{color};
                     color:#fff;border-radius:6px;font-size:18px;font-weight:700;">
            {topic}
          </h2>
          {cards_html}
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UPSC News Digest – {today}</title>
</head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif;">
  <div style="max-width:680px;margin:0 auto;padding:20px;">

    <!-- Header -->
    <div style="background:#1a1a2e;border-radius:10px;padding:28px 30px;margin-bottom:24px;text-align:center;">
      <h1 style="color:#fff;margin:0 0 6px 0;font-size:26px;font-weight:700;">
        UPSC News Digest
      </h1>
      <p style="color:#aaa;margin:0;font-size:14px;">{today}</p>
    </div>

    <!-- Topic Index Bar -->
    <div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;
                padding:16px 20px;margin-bottom:28px;">
      <p style="margin:0 0 10px 0;font-size:13px;font-weight:700;color:#555;
                text-transform:uppercase;letter-spacing:0.5px;">Topics in this digest</p>
      <div>{index_bar_items}</div>
    </div>

    <!-- Article Sections -->
    {sections_html}

    <!-- Footer -->
    <div style="text-align:center;padding:20px;color:#999;font-size:12px;">
      Generated automatically by UPSC News Digest &bull; Powered by Llama 3.3 via Groq
    </div>
  </div>
</body>
</html>"""
    return html


def send_email(html_body):
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_APP_PASSWORD")
    receiver_raw = os.getenv("RECEIVER_EMAIL")

    if not all([sender, password, receiver_raw]):
        raise ValueError("Missing one or more email env vars: SENDER_EMAIL, SENDER_APP_PASSWORD, RECEIVER_EMAIL")

    # Support comma-separated list of recipients
    receivers = [r.strip() for r in receiver_raw.split(",") if r.strip()]

    today = datetime.now().strftime("%B %d, %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"UPSC News Digest – {today}"
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    msg.attach(MIMEText(html_body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
    print(f"  Sent to: {', '.join(receivers)}")


if __name__ == "__main__":
    print("=== UPSC News Digest ===")

    print("\n[1/4] Fetching articles from RSS feeds...")
    try:
        articles = fetch_articles()
        print(f"  Total fetched: {len(articles)} articles")
    except Exception as e:
        print(f"FATAL: Could not fetch articles: {e}")
        raise

    print("\n[2/4] Classifying articles with Llama 3.3 via Groq (single API call)...")
    try:
        classified = classify_articles(articles)
        print(f"  UPSC relevant: {len(classified)} articles")
    except Exception as e:
        print(f"FATAL: Groq classification failed: {e}")
        raise

    if not classified:
        print("No UPSC-relevant articles found. Exiting without sending email.")
        exit(0)

    print("\n[3/4] Rendering HTML email...")
    try:
        grouped = collections.defaultdict(list)
        for a in classified:
            grouped[a["topic"]].append(a)
        html = render_html(grouped)
        print(f"  Topics covered: {', '.join(grouped.keys())}")
    except Exception as e:
        print(f"FATAL: HTML rendering failed: {e}")
        raise

    print("\n[4/4] Sending email via Gmail SMTP...")
    try:
        send_email(html)
        print("  Email sent successfully!")
    except Exception as e:
        print(f"FATAL: Email sending failed: {e}")
        raise

    print("\n=== Done! Digest delivered. ===")
