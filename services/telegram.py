import httpx
import os
from dotenv import load_dotenv

load_dotenv()


class Telegram:

    def __init__(self):

        self.token = os.getenv("BOT_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")

    def send(self, title, url, source):

        message = f"""
📢 <b>Education Update</b>

🏛 <b>Source:</b> {source}

📄 <b>Title:</b>
{title}

🔗 {url}
"""

        api = f"https://api.telegram.org/bot{self.token}/sendMessage"

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