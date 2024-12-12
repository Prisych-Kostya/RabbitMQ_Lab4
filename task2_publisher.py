import pika
import time
import random

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Назва обмінника
EXCHANGE_NAME = 'days_of_week'

# Оголошення обмінника типу direct
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

# Дні тижня - ключі маршрутизації
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Функція для генерування (вибору) одного з декількох можливих повідомлення на день
def generate_message(day):
    messages = [
        f"Завдання на {day}",
        f"Плани на {day}",
        f"Огляд подій за {day}",
        f"Звіт за {day}",
    ]
    return random.choice(messages)


# Надсилання повідомлень
try:
    for _ in range(20):  # 20 повідомлень
        day = random.choice(days)
        message = generate_message(day)
        
        # Надсилання повідомлення з конкретним ключем маршрутизації
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=day,
            body=message
        )
        print(f"Надіслано повідомлення для {day}: {message}")
        
        time.sleep(1)

finally:
    connection.close()