<div align="center">

![ticketnotifier](docs/banner.svg)

**Cinema showtime checks. Telegram alerts. Less refreshing.**

[![Monitor](https://github.com/Mohabashraf2010/ticketnotifier/actions/workflows/monitor.yml/badge.svg)](https://github.com/Mohabashraf2010/ticketnotifier/actions/workflows/monitor.yml)
![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Browser-Playwright-2EAD33)
![Telegram](https://img.shields.io/badge/Alerts-Telegram-26A5E4?logo=telegram&logoColor=white)

[Quick start](#quick-start) · [Automation](#github-actions) · [How it works](#how-it-works)

</div>

## Overview

**ticketnotifier** is a lightweight Python monitor for Cinemas. It renders a movie page with Chromium, checks for a selected show date, and sends a Telegram message with the booking link when the page indicates availability.

| Feature | What it does |
| --- | --- |
| Browser-based checks | Loads JavaScript-rendered content using Playwright. |
| Date-specific monitoring | Looks for the configured date in Scene's showtime markup. |
| Telegram notifications | Delivers the date and booking URL to your chosen chat. |
| Scheduled runs | Includes a GitHub Actions workflow scheduled every five minutes. |
| Local duplicate guard | Writes `sent.flag` after a successful notification. |

## Quick start

### 1. Install

Use Python 3.13, matching the included workflow.

```bash
git clone https://github.com/Mohabashraf2010/ticketnotifier.git
cd ticketnotifier
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

On Linux, use `python -m playwright install --with-deps chromium` if browser system dependencies are missing.

### 2. Configure

Create a `.env` file using [.env.example](.env.example) as a template:

```dotenv
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

Create your bot through Telegram's **@BotFather**, then start a conversation with the bot or add it to your target group. Set `CHAT_ID` to the destination chat's ID. Keep real credentials in `.env` or GitHub Actions secrets; `.env` is ignored by Git.

In [main.py](main.py), edit:

| Setting | Purpose |
| --- | --- |
| `URL` | Scene Cinemas movie page to check. |
| `TARGET_DATE` | Show date in `DD-MM-YYYY` format, matching the page markup. |
| `HEADLESS` | Set to `False` to watch the browser while debugging locally. |

The checked-in movie URL and date are an example from the original monitor. **Update them before running.**

### 3. Run

```bash
python main.py
```

Each invocation checks once and exits. After a successful alert, remove `sent.flag` when you want to monitor again or change the target date.

## GitHub Actions

1. Open your repository's **Settings → Secrets and variables → Actions**.
2. Add repository secrets named `BOT_TOKEN` and `CHAT_ID`.
3. Update `URL` and `TARGET_DATE` in `main.py`.
4. Open **Actions → ticketnotifier → Run workflow** for a manual check.

The included workflow requests a run every five minutes. Scheduled runs may be delayed by GitHub; this is not a guaranteed alert interval.

> **Duplicate alerts:** `sent.flag` only persists in the local working directory. The current workflow uses a fresh runner for every run, so it can send repeated alerts while the availability checks pass. Disable the scheduled workflow after receiving your alert if you no longer need monitoring.

## How it works

```text
Scene movie page → Chromium renders the page → Date checks → Telegram alert
```

The monitor requires all three conditions:

- `LoadShowtimes('TARGET_DATE')` exists in the rendered HTML.
- An element with `id="data-TARGET_DATE"` exists.
- The page does not contain `THERE IS NO SHOWTIMES AVAILABLE NOW!`.

These are page-markup checks, not a live seat-inventory or checkout check. Confirm actual availability on the cinema website. The selectors are specific to Scene Cinemas and may need updating if its website changes.

## Project structure

```text
ticketnotifier/
├── .github/workflows/monitor.yml   # Scheduled and manual checks
├── docs/banner.svg                # Project banner
├── .env.example                   # Credential template
├── main.py                        # Browser checks and Telegram alerts
└── requirements.txt               # Python dependencies
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Browser cannot launch | Install Chromium and, on Linux, its system dependencies. |
| No alert arrives | Check credentials, bot access to the chat, and the printed date checks. |
| Monitor exits immediately | Look for an existing `sent.flag`. |
| Repeated Actions alerts | See the duplicate-alert note above. |
| Date never matches | Verify `TARGET_DATE`, the movie URL, and Scene's current markup. |

---

Independent project; not affiliated with Scene Cinemas or Telegram.
