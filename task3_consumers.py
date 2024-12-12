import pika

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Назва обмінника
EXCHANGE_NAME = 'social_media_events'

# Оголошення обмінника
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

# Можливі user_id
user_ids = ['user1', 'user2', 'user3', 'user4', 'user5']

def create_consumer(user_id):
    # Створення черги для конкретного користувача
    queue_name = f'{user_id}_queue'
    channel.queue_declare(queue=queue_name)
    
    # Прив'язка до обмінника з патерном для всіх подій користувача
    # post.<user_id>.* - означає будь-які дії для цього користувача
    channel.queue_bind(
        exchange=EXCHANGE_NAME, 
        queue=queue_name, 
        routing_key=f"post.{user_id}.*"
    )
    
    def callback(ch, method, properties, body):
        print(f"[{user_id} Consumer] Отримано повідомлення [{method.routing_key}]: {body.decode()}")
    
    # Підписка на чергу
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=callback, 
        auto_ack=True
    )
    
    return queue_name

# Створення consumer для кожного користувача
consumers = [create_consumer(user_id) for user_id in user_ids]

print('Consumers запущено. Очікування повідомлень. Ctrl+C для виходу')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()