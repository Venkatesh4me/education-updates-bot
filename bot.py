import json
from pathlib import Path

from parsers.generic import GenericParser
from services.downloader import Downloader
from services.storage import Storage
from services.telegram import Telegram
from services.logger import logger
from utils.hashing import generate_hash


class EducationBot:

    def __init__(self):

        base = Path(__file__).parent

        with open(base / "config/sites.json", encoding="utf-8") as f:
            self.sites = json.load(f)

        with open(base / "config/keywords.json", encoding="utf-8") as f:
            self.keywords = json.load(f)

        self.downloader = Downloader()
        self.parser = GenericParser(self.keywords)
        self.storage = Storage()
        self.telegram = Telegram()

    def run(self):

        logger.info("=" * 60)
        logger.info("Education Updates Bot Started")
        logger.info("=" * 60)

        total_new = 0
        total_old = 0

        for site in self.sites:

            logger.info(f"Checking {site['name']}")

            result = self.downloader.fetch(site["url"])

            if not result["success"]:
                logger.error(result["error"])
                continue

            logger.success(
                f"Downloaded successfully (HTTP {result['status']})"
            )

            articles = self.parser.parse(
                result["html"],
                site["url"]
            )

            logger.info(f"Found {len(articles)} matching articles")

            new_count = 0
            old_count = 0

            for article in articles:

                article_hash = generate_hash(
                    article["title"],
                    article["url"]
                )

                if self.storage.exists(article_hash):

                    old_count += 1

                else:

                    new_count += 1
                    total_new += 1

                    self.storage.add(
                        article_hash,
                        article
                    )

                    logger.success(
                        f"New Article: {article['title']}"
                    )

                    sent = self.telegram.send(
                        article["title"],
                        article["url"],
                        site["name"]
                    )

                    if sent:
                        logger.success("Telegram message sent")
                    else:
                        logger.error("Failed to send Telegram message")

            total_old += old_count

            logger.info(f"New Articles : {new_count}")
            logger.info(f"Existing Articles : {old_count}")

        logger.info("=" * 60)
        logger.success("Scan Completed Successfully")
        logger.info(f"Total New Articles : {total_new}")
        logger.info(f"Total Existing Articles : {total_old}")
        logger.info("=" * 60)