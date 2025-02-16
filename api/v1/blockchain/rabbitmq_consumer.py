import json
import aio_pika

import httpx


RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672/'


async def process_blockchain_transaction(message: aio_pika.IncomingMessage):
    async with message.process():
        payload = json.loads(message.body.decode())
        print("Получено сообщение для blockchain:", payload)
        async with httpx.AsyncClient() as client:
            response = await client.post("http://blockchain:8003/add_transaction", json=payload)
            print("Ответ /add_transaction:", response.status_code, response.text)


async def start_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("blockchain_transactions", aio_pika.ExchangeType.FANOUT, durable=True)
    queue = await channel.declare_queue("blockchain_service_queue", durable=True)
    await queue.bind(exchange)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await process_blockchain_transaction(message)
