from fastapi import APIRouter, Request, BackgroundTasks, status, Form

from src.mail import create_message, mail
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
    print(name, address, message)
    recipient_mail = Config.MAIL_USERNAME
    html_content = message
    html_content = f"""
    <h3>New Contact Form Message</h3>
    <p><b>From:</b> {name} &lt;{address}&gt;</p>
    <p><b>Message:</b></p>
    <p>{message}</p>
    """

    subject = f"New Message from {address}: {name}"
    message = create_message(subject, recipient_mail, html_content)

    bg_tasks.add_task(mail.send_message, message)

    return JSONResponse(
        content={"message": "Email sent successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
