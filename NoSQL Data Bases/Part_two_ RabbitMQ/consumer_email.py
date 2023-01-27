import pika

from send_message import send_message_email

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='send_message', durable=True)


def callback_result(ch, method, properties, body: bytes):
    """
    Required function for dispatching messages to user

    :param ch: BlockingChannel
    :param method: spec.Basic.Deliver
    :param properties: spec.BasicProperties
    :param body: bytes
    :return: messages to user
    """
    user_id = body.decode()
    send_message_email(user_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    try:
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='email_queue', on_message_callback=callback_result)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Goodbye")
