from random import randint

from faker import Faker

from model import Users
import connect

fake = Faker('uk_UA')


def seed_user_to_db():
    """
    Seed fake data to DB Users, return user id

    :return: str
    """
    fullname = fake.name()
    email = fake.ascii_free_email()
    phone = fake.phone_number()
    email_or_sms = bool(randint(0, 1))
    Users(fullname=fullname, email=email, phone=phone, email_or_sms=email_or_sms).save()
    return [_.id for _ in Users.objects(fullname=fullname)][0]


if __name__ == '__main__':
    seed_user_to_db()
