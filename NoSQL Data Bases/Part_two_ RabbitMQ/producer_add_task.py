from find_status import user_delivery_status, user_send_method

import pika

from seeds import seed_user_to_db

USERS_NUMBER = 10

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='send_email', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='send_email', queue='email_queue')

channel.exchange_declare(exchange='send_sms', exchange_type='direct')
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='send_sms', queue='sms_queue')


if __name__ == '__main__':
    try:
        count = 0
        while True:
            if count > USERS_NUMBER + 1:
                break
            user_id = seed_user_to_db()
            if not user_delivery_status(user_id):
                if user_send_method(user_id):
                    exchange = 'send_email'
                    routing_key = 'email_queue'
                else:
                    exchange = 'send_sms'
                    routing_key = 'sms_queue'
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=user_id.encode(),
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                    )
                )
                print(f'Send user ID: {user_id} for messaging')
            print(f'Message was sent to user ID: {user_id} early')
            count += 1
        connection.close()
    except KeyboardInterrupt:
        print('Goodbye')
