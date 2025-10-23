import os
from datetime import datetime, timezone

from src.utils.slug import slugify

UPLOAD_DIR = "uploads/news"


async def upload_image(image):
    if image:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        slug_datetime = slugify(str(datetime.now(timezone.utc)))
        filename = f"{slug_datetime}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        return file_path
    return None
