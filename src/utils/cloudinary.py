from datetime import datetime, timezone
import cloudinary.uploader
import cloudinary
from fastapi import UploadFile

from src.core.config import Config


cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_to_cloudinary(file: UploadFile, slug, subfolder,
                               resource_type="image"):
    if not file:
        return None

    try:
        file.file.seek(0)

        ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        public_id = f"{slug}_{ts}"
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder=f"psn_website/{subfolder}",
            public_id=public_id,
            overwrite=True,
            resource_type=resource_type
        )
        return upload_result["secure_url"]

    except Exception as e:
        print("Cloudinary upload failed:", e)
        return None
