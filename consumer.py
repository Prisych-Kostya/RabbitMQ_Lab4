import pika

# Параметри підключення
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Оголошення черги (має збігатися з Producer)
queue_name = 'messages'
channel.queue_declare(queue=queue_name)

# Лічильник отриманих повідомлень
message_count = 0

def callback(ch, method, properties, body):
    global message_count
    message_count += 1
    print(f"Отримано повідомлення {message_count}: {body.decode()}")

# Підписка на чергу
channel.basic_consume(
    queue=queue_name, 
    on_message_callback=callback, 
    auto_ack=True
)

print('Очікування повідомлень. Натисніть Ctrl+C для виходу')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\nЗагальна кількість отриманих повідомлень: {message_count}")
    channel.stop_consuming()

connection.close()