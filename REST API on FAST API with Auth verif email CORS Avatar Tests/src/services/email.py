from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service
from src.conf.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=EmailStr(settings.mail_from),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Rest API application",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):

    """
    The send_email function sends an email to the user with a link to confirm their email address.
    The function takes in three parameters:
    -email: the user's email address, which is used as a recipient for the message.
    -username: this is used in the body of the message, and will be displayed on screen when they click on it.
    It should be something like &quot;John Doe&quot; or &quot;Jane Smith&quot;.
    This parameter can also be left blank if you don't want it included in your message.
    -host: this is where we are hosting our application (e.g., http

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username to the template
    :param host: str: Create the link to the frontend
    :return: A coroutine object, which is a function that can be awaited
    :doc-author: Trelent
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)
