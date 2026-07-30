import json
from pathlib import Path


class Storage:

    def __init__(self):

        BASE_DIR = Path(__file__).parent.parent

        self.db_file = BASE_DIR / "state" / "database.json"

        if not self.db_file.exists():

            self.data = {
                "articles": {}
            }

            self.save()

        else:

            with open(self.db_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):

        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def exists(self, key):

        return key in self.data["articles"]

    def add(self, key, article):

        self.data["articles"][key] = article
        self.save()