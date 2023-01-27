from model import Users
import connect

MESSAGE = 'This is your message'


class MySendExcept(Exception):
    pass


def send_message_sms(id_user: str):
    """
    Send SMS with message on phone to user with id

    param id_user: str
    :return: None
    """
    try:
        user = Users.objects(id=id_user)
        phone = user.phone
        ...
        user.update(is_send=True)
        pass
    except MySendExcept:
        pass
    except Exception as e:
        print(e)


def send_message_email(id_user: str):
    """
    Send message on email to user with id

    param id_user: str
    :return: None
    """
    try:
        user = Users.objects(id=id_user)
        email = user.email
        ...
        user.update(is_send=True)
        pass
    except MySendExcept:
        pass
    except Exception as e:
        print(e)


def send_message_to_user(id_user: str):
    """
    Send message on email to user with id

    param id_user: str
    :return: None
    """
    try:
        user = Users.objects(id=id_user)
        email = user.email
        if not user.is_send:
            ...
            user.update(is_send=True)
            print(f'Message{MESSAGE} successful send to user {user.fullname}')
        print(f'Message{MESSAGE} was sent to user {user.fullname} early')
    except MySendExcept:
        pass
    except Exception as e:
        print(e)
