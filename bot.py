import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.downloader import Downloader
from services.storage import Storage
from services.telegram import Telegram
from services.logger import logger
from services.site_checker import SiteChecker


class EducationBot:

    def __init__(self):

        base = Path(__file__).parent

        with open(base / "config/sites.json", "r", encoding="utf-8") as f:
            self.sites = json.load(f)

        self.downloader = Downloader()
        self.storage = Storage()
        self.telegram = Telegram()

        self.site_checker = SiteChecker(
            self.downloader,
            self.storage,
            self.telegram,
            logger
        )

    def run(self):

        logger.info("=" * 70)
        logger.info("Education Updates Bot Started")
        logger.info("=" * 70)
        start_time = time.perf_counter()

        total_new = 0
        total_old = 0

        enabled_sites = [
            site
            for site in self.sites
            if site.get("enabled", True)
        ]

        with ThreadPoolExecutor(max_workers=5) as executor:

            futures = {
                executor.submit(
                    self.site_checker.check,
                    site
                ): site
                for site in enabled_sites
            }

            for future in as_completed(futures):

                site = futures[future]

                try:

                    result = future.result()

                    logger.success(f"{site['name']} Completed")

                    logger.info(
                        f"{site['name']} -> New : {result['new']}"
                    )

                    logger.info(
                        f"{site['name']} -> Old : {result['old']}"
                    )

                    total_new += result["new"]
                    total_old += result["old"]

                except Exception as e:

                    logger.exception(
                        f"{site['name']} failed : {e}"
                    )
        elapsed = time.perf_counter() - start_time

        logger.success(f"Completed in {elapsed:.2f} seconds")
        logger.info("=" * 70)
        logger.success("Scan Completed Successfully")
        logger.info(f"Total New Articles : {total_new}")
        logger.info(f"Total Existing Articles : {total_old}")
        logger.info("=" * 70)