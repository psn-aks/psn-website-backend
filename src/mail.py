from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.core.config import Config


# BASE_DIR = Path(__file__).resolve().parent


mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    MAIL_DEBUG=True

)

mail = FastMail(config=mail_config)


def create_message(subject: str, recipient: str, html_content: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=html_content,
        subtype=MessageType.html,
    )
    return message


# async def send_message(message: dict):
#     msg = MessageSchema(
#         subject=message["subject"],
#         recipients=message["recipients"],
#         body=message["html"],
#         subtype="html",
#     )
#     await mail.send_message(msg)
