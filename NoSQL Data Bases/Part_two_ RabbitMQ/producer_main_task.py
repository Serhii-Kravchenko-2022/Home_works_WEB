import pika

from seeds import seed_user_to_db

USERS_NUMBER = 10

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='send_message', exchange_type='direct')
channel.queue_declare(queue='message_queue', durable=True)
channel.queue_bind(exchange='send_message', queue='message_queue')

if __name__ == '__main__':
    try:
        count = 0
        while True:
            if count > USERS_NUMBER + 1:
                break
            user_id = seed_user_to_db()
            channel.basic_publish(
                exchange='send_message',
                routing_key='message_queue',
                body=user_id.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
            print(f'Send user ID: {user_id} for messaging')
            count += 1
        connection.close()
    except KeyboardInterrupt:
        print('Goodbye')
