import feedparser


class RSSParser:

    def __init__(self, keywords):
        self.keywords = [k.lower() for k in keywords]

    def parse(self, feed_url, base_url=None):

        feed = feedparser.parse(feed_url)

        articles = []

        for entry in feed.entries:

            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()

            if not title or not link:
                continue

            # If keywords list is empty, include everything
            if not self.keywords:
                articles.append({
                    "title": title,
                    "url": link
                })
                continue

            title_lower = title.lower()

            if any(keyword in title_lower for keyword in self.keywords):
                articles.append({
                    "title": title,
                    "url": link
                })

        return articles