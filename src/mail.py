import httpx
from fastapi import BackgroundTasks

from src.core.config import Config

RESEND_API_URL = Config.RESEND_API_URL
RESEND_API_KEY = Config.RESEND_API_KEY
MAIL_FROM = Config.MAIL_FROM


async def send_resend_email(to: str, subject: str, html: str):
    """Send email using Resend API."""
    headers = {"Authorization": f"Bearer {RESEND_API_KEY}"}
    payload = {
        "from": f"Your Website <{MAIL_FROM}>",
        "to": [to],
        "subject": subject,
        "html": html,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(RESEND_API_URL, json=payload,
                                     headers=headers)
        response.raise_for_status()
        return response.json()


def send_resend_email_bg(bg_tasks: BackgroundTasks, to: str,
                         subject: str, html: str):
    """Background task wrapper for FastAPI."""
    bg_tasks.add_task(send_resend_email, to, subject, html)


# from fastapi_mail import FastMail, ConnectionConfig, MessageSchema,
# MessageType
# from src.core.config import Config


# mail_config = ConnectionConfig(
#     MAIL_USERNAME=Config.MAIL_USERNAME,
#     MAIL_PASSWORD=Config.MAIL_PASSWORD,
#     MAIL_FROM=Config.MAIL_FROM,
#     MAIL_PORT=Config.MAIL_PORT,
#     MAIL_SERVER=Config.MAIL_SERVER,
#     MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     MAIL_DEBUG=True

# )

# mail = FastMail(config=mail_config)


# def create_message(subject: str, recipient: str, html_content: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[recipient],
#         body=html_content,
#         subtype=MessageType.html,
#     )
#     return message
