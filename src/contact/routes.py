from fastapi import APIRouter, Request, BackgroundTasks, status, Form

from src.utils.mail import send_resend_email_bg
from fastapi.responses import JSONResponse
from src.core.config import Config


contact_router = APIRouter()


@contact_router.post("/send-mail", status_code=status.HTTP_202_ACCEPTED)
async def send_mail(request: Request,
                    bg_tasks: BackgroundTasks,
                    name: str = Form(...),
                    address: str = Form(...),
                    message: str = Form(...),
                    ):

    recipient_mail = Config.MAIL_USERNAME
    html_content = f"""
    <h3>New Contact Form Message</h3>
    <p><b>From:</b> {name} &lt;{address}&gt;</p>
    <p><b>Message:</b></p>
    <p>{message}</p>
    """

    subject = f"New Message from {name} ({address})"
    send_resend_email_bg(bg_tasks, recipient_mail, subject, html_content)

    return JSONResponse(
        content={"message": "Email sent successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
