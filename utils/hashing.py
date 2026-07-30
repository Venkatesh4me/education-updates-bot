import hashlib


def generate_hash(title, url):

    text = title + url

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()