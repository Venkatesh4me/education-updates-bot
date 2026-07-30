import os
from datetime import datetime

import httpx
from dotenv import load_dotenv

load_dotenv()


class Telegram:

    def __init__(self):

        self.token = os.getenv("BOT_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")

    def send(self, title, url, source):

        now = datetime.now().strftime("%d %b %Y %I:%M %p")

        message = f"""
📢 <b>NEW UPDATE</b>

🏛 <b>Source</b>
{source}

📄 <b>Title</b>
<a href="{url}">{title}</a>

🕒 <b>Detected</b>
{now}
"""

        api = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:

            response = httpx.post(
                api,
                data={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                },
                timeout=30
            )

            return response.status_code == 200

        except Exception:
            return False