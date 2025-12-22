import re
from unicodedata import normalize


def slugify(value: str) -> str:
    value = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9\s]", "", value).strip().lower()
    value = re.sub(r"[\s-]+", "-", value)
    return value or "item"


async def generate_slug_from_title(title: str, DBInstance) -> str:
    base = slugify(title)
    slug = base
    i = 2

    while True:
        result = await DBInstance.find_one(DBInstance.slug == slug)
        if not result:
            return slug
        slug = f"{base}-{i}"
        i += 1
