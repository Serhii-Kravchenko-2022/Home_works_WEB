from model import Users
import connect


def user_id_data(id_user: str):
    user = Users.objects(id=id_user)
    return user


def user_delivery_status(id_user: str):
    return user_id_data(id_user).is_sent


def user_send_method(id_user: str):
    return user_delivery_status(id_user).email_or_sms



