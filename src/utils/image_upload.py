from datetime import datetime, timezone
import cloudinary.uploader
from src.core.cloudinary_config import cloudinary


async def upload_image(image, subfolder: str = "news"):
    if not image:
        return None

    try:
        # Upload directly to Cloudinary
        upload_result = cloudinary.uploader.upload(
            image.file,
            folder=f"psn_website/{subfolder}",
            public_id=(
                f"news_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
                ),
            overwrite=True,
            resource_type="image"
        )
        return upload_result["secure_url"]
    except Exception as e:
        print("Cloudinary upload failed:", e)
        return None
