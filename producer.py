import pika
import time
import random

# Параметри підключення
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Оголошення черги
queue_name = 'messages'
channel.queue_declare(queue=queue_name)

def generate_message():
    messages = [
        "Сьогодні хмарна погода",
        "Практика з RabbitMQ",
        "Налаштування брокерів повідомлень",
        "Виконання лабораторної №4"
    ]
    return random.choice(messages)

# Надсилання повідомлень
try:
    for i in range(20):
        message = generate_message()
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message
        )
        print(f"Надіслано повідомлення {i+1}: {message}")
        time.sleep(1)  # Інтервал між повідомленнями 1 сек

finally:
    connection.close()