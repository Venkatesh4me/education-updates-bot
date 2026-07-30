import httpx


class Downloader:
    def __init__(self):
        self.client = httpx.Client(
            timeout=30,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                )
            },
        )

    def fetch(self, url):
        try:
            response = self.client.get(url)

            return {
                "success": True,
                "status": response.status_code,
                "html": response.text,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }