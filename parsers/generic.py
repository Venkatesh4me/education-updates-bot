from urllib.parse import urljoin

from bs4 import BeautifulSoup


class GenericParser:
    def __init__(self, keywords):
        self.keywords = [k.lower() for k in keywords]

    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "lxml")

        articles = []

        for link in soup.find_all("a", href=True):

            title = link.get_text(" ", strip=True)

            href = urljoin(base_url, link["href"])

            if len(title) < 5:
                continue

            lower = title.lower()

            if any(keyword in lower for keyword in self.keywords):

                articles.append(
                    {
                        "title": title,
                        "url": href,
                    }
                )

        return articles