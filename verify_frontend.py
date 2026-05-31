import collections
import html
import os
from digest import render_html, TOPIC_ORDER
from playwright.sync_api import sync_playwright

def verify_html():
    # Mock data
    grouped = collections.defaultdict(list)
    category_angles = {}

    for i, topic in enumerate(TOPIC_ORDER[:3]): # Just 3 topics for verification
        category_angles[topic] = [f"UPSC Angle {j} for {topic} - GS-I relevance" for j in range(2)]
        for k in range(2):
            grouped[topic].append({
                "title": f"Significant Article {k} in {topic}",
                "source": "Reliable Source",
                "summary": f"This summary covers {topic} in depth, mentioning GS-II and constitutional articles. Important for UPSC aspirants.",
                "link": f"https://example.com/{topic}/{k}"
            })

    html_content = render_html(grouped, category_angles)

    os.makedirs("/home/jules/verification", exist_ok=True)
    temp_html_path = "/home/jules/verification/test_digest.html"
    with open(temp_html_path, "w") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Use absolute path with file:// protocol
        abs_path = os.path.abspath(temp_html_path)
        page.goto(f"file://{abs_path}")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="/home/jules/verification/digest_verification.png", full_page=True)
        browser.close()

    print(f"Screenshot saved to /home/jules/verification/digest_verification.png")

if __name__ == "__main__":
    verify_html()
