import pika

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Назва обмінника
EXCHANGE_NAME = 'days_of_week'

# Оголошення обмінника
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

# Дні тижня
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Функція для створення consumer для конкретного дня
def create_consumer(day):
    # Створення черги для конкретного дня
    queue_name = f'{day}_queue'
    channel.queue_declare(queue=queue_name)
    
    # Прив'язка черги до обмінника з ключем - день тижня
    channel.queue_bind(
        exchange=EXCHANGE_NAME, 
        queue=queue_name, 
        routing_key=day
    )
    
    def callback(ch, method, properties, body):
        print(f"[{day} Consumer] Отримано повідомлення: {body.decode()}")
    
    # Підписка на чергу
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=callback, 
        auto_ack=True
    )
    
    return queue_name

# Створення consumer для кожного дня
consumers = [create_consumer(day) for day in days]

print('Consumers запущено. Очікування повідомлень. Ctrl+C для виходу')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()