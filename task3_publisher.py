import pika
import random
import time

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Назва обмінника
EXCHANGE_NAME = 'social_media_events'

# Оголошення обмінника типу topic
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

# Можливі дії
actions = ['create', 'update', 'delete']

# Можливі user_id
user_ids = ['user1', 'user2', 'user3', 'user4', 'user5']

def generate_message(user_id, action):
    messages = {
        'create': f"Новий пост від {user_id}",
        'update': f"Оновлення профілю {user_id}",
        'delete': f"Видалення контенту {user_id}"
    }
    return messages[action]

# Надсилання повідомлень
try:
    for _ in range(20):
        # Випадковий user_id та дія
        user_id = random.choice(user_ids)
        action = random.choice(actions)
        
        # Формування ключа маршрутизації ТОЧНО за форматом post.<user_id>.<action>
        routing_key = f"post.{user_id}.{action}"
        
        message = generate_message(user_id, action)
        
        # Надсилання повідомлення
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=message
        )
        print(f"Надіслано повідомлення: {routing_key} - {message}")
        
        time.sleep(1)

finally:
    connection.close()