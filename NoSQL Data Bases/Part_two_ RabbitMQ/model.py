from mongoengine import Document, StringField, BooleanField


class Users(Document):
    fullname = StringField(max_length=150, required=True, unique=True)
    email = StringField(max_length=100)
    is_sent = BooleanField(default=False)
    phone = StringField(max_length=50)
    email_or_sms = BooleanField(default=True)
