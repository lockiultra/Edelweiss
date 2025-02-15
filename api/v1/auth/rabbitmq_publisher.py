import json
import asyncio
import aio_pika


RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672/'


class RabbitMQPublisher:
    def __init__(self):
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange: aio_pika.Exchange | None = None

    async def connect(self, retry_interval: int = 2, max_retries: int = 10):
        retries = 0
        while retries < max_retries:
            try:
                self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
                self.channel = await self.connection.channel()
                self.exchange = await self.channel.declare_exchange(
                    'user_events',
                    aio_pika.ExchangeType.FANOUT,
                    durable=True
                )
                print("Соединение с RabbitMQ установлено.")
                return
            except Exception as e:
                retries += 1
                print(f"Не удалось установить соединение с RabbitMQ, попытка {retries}/{max_retries}. Ошибка: {e}")
                await asyncio.sleep(retry_interval)
        raise Exception("Не удалось подключиться к RabbitMQ после нескольких попыток.")

    async def publish(self, message_data: dict):
        if not self.exchange:
            raise Exception("Обменник не инициализирован. Убедитесь, что вызван connect() перед публикацией сообщения.")
        message_body = json.dumps(message_data).encode()
        message = aio_pika.Message(body=message_body)
        await self.exchange.publish(message, routing_key='')

    async def close(self):
        if self.connection:
            await self.connection.close()


publisher_instance = RabbitMQPublisher()


async def publish_user_registered_event(user_data: dict):
    await publisher_instance.publish(user_data)
