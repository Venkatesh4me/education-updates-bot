import httpx


class Downloader:

    def __init__(self):

        self.client = httpx.Client(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                )
            },
            timeout=30,
            follow_redirects=True
        )

    def fetch(self, url):

        for attempt in range(1, 4):

            try:

                response = self.client.get(url)
                response.raise_for_status()

                return {
                    "success": True,
                    "status": response.status_code,
                    "html": response.text
                }

            except Exception as e:

                print(f"Retry {attempt}/3 : {url}")

                if attempt == 3:
                    return {
                        "success": False,
                        "status": None,
                        "html": "",
                        "error": str(e)
                    }