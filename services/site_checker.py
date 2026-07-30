from parsers.factory import ParserFactory
from utils.hashing import generate_hash


class SiteChecker:

    def __init__(self, downloader, storage, telegram, logger):

        self.downloader = downloader
        self.storage = storage
        self.telegram = telegram
        self.logger = logger

    def check(self, site):

        self.logger.info(f"Checking {site['name']}")

        keywords = site.get("keywords", [])

        parser = ParserFactory.get_parser(
            site["type"],
            keywords
        )

        if site["type"].lower() == "rss":

            articles = parser.parse(site["url"])

        else:

            result = self.downloader.fetch(site["url"])

            if not result["success"]:

                self.logger.error(result["error"])

                return {
                    "new": 0,
                    "old": 0
                }

            articles = parser.parse(
                result["html"],
                site["url"]
            )

        self.logger.info(
            f"{site['name']} -> Found {len(articles)} articles"
        )

        new_count = 0
        old_count = 0

        for article in articles:

            h = generate_hash(
                article["title"],
                article["url"]
            )

            if self.storage.exists(h):

                old_count += 1
                continue

            new_count += 1

            self.storage.add(h, article)

            self.telegram.send(
                article["title"],
                article["url"],
                site["name"]
            )

        return {
            "new": new_count,
            "old": old_count
        }