import re
from unicodedata import normalize


def slugify(value: str) -> str:
    value = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9\s]", "", value).strip().lower()
    value = re.sub(r"[\s-]+", "-", value)
    return value or "item"
