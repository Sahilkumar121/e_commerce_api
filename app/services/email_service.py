from typing import Any, cast

from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.core.mail import mail_config


async def send_welcome_email(email_to: EmailStr, user_name: str):
    template = f"<h1> Welcome {user_name}</h1>. <p> Thanks for joining us!.</p>"

    message = MessageSchema(
        subject="Welcome to our App!",
        recipients=cast(Any, [email_to]),
        body=template,
        subtype=MessageType.html,
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)
