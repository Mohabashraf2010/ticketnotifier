from pathlib import Path

import requests
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# CONFIGURATION
# ==========================================================

URL = "https://cfc.scenecinemas.com/movie-details/spider-man-brand-new-day.html"


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Thursday you're waiting for
TARGET_DATE = "05-08-2026"

# Run browser in background
HEADLESS = True

# Prevent duplicate notifications
FLAG_FILE = Path("sent.flag")


# ==========================================================
# TELEGRAM
# ==========================================================

def send_telegram(message: str):

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(
        telegram_url,
        data=payload,
        timeout=20
    )

    response.raise_for_status()


# ==========================================================
# CHECK WEBSITE
# ==========================================================

def get_rendered_html():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=HEADLESS)

        page = browser.new_page()

        page.goto(URL)

        page.wait_for_load_state("networkidle")

        # Give JavaScript a little extra time
        page.wait_for_timeout(3000)

        html = page.content()

        browser.close()

    return html


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("Spider-Man Ticket Monitor")
    print("=" * 60)

    # Don't notify twice
    if FLAG_FILE.exists():

        print("Notification already sent before.")
        return

    print("Opening Scene...")

    html = get_rendered_html()

    # -------------------------------
    # Independent Checks
    # -------------------------------

    has_loadshowtimes = (
        f"LoadShowtimes('{TARGET_DATE}')" in html
    )

    has_date_id = (
        f'id="data-{TARGET_DATE}"' in html
    )

    no_showtimes_message = (
        "THERE IS NO SHOWTIMES AVAILABLE NOW!" in html
    )

    # -------------------------------
    # Debug Output
    # -------------------------------

    print()
    print("Checks")
    print("-" * 30)

    print(f"LoadShowtimes : {has_loadshowtimes}")
    print(f"Date ID       : {has_date_id}")
    print(f"No Showtimes  : {no_showtimes_message}")

    tickets_available = (
        has_loadshowtimes
        and has_date_id
        and not no_showtimes_message
    )

    print()
    print(f"Tickets Available: {tickets_available}")

    # -------------------------------
    # Send Notification
    # -------------------------------

    if tickets_available:

        message = f"""
🎬 Spider-Man Thursday Tickets Are LIVE!

Date:
{TARGET_DATE}

Book now:
{URL}
"""

        try:

            send_telegram(message)

            FLAG_FILE.write_text("sent")

            print()
            print("✅ Telegram notification sent.")
            print("✅ sent.flag created.")

        except Exception as e:

            print()
            print("❌ Failed to send Telegram notification.")
            print(e)

    else:

        print()
        print("❌ Thursday tickets not available yet.")


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":
    main()