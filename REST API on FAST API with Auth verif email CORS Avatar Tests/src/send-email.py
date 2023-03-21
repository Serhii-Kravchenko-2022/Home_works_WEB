from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME="serhii2323@meta.ua",
    MAIL_PASSWORD="QWERTY123123",
    MAIL_FROM="serhii2323@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Example email",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):

    """
    The send_in_background function is a simple example of how to send an email in the background.
    It uses the FastMail class and its send_message method, which takes a MessageSchema object as its first
    argument.
    The second argument is optional and allows you to specify which template file you want to use for your
    message body.

    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param body: EmailSchema: Validate the body of the request
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    message = MessageSchema(
        subject="Reset a user's password",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('send-email:app', port=8000, reload=True)