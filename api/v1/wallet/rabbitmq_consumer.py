import json

import aio_pika
import httpx


RABBITMQ_URL = 'amqp://guest:guest@rabbitmq'


async def process_user_registered_event(message: aio_pika.IncomingMessage):
    async with message.process():
        with open('log_1.txt', 'w') as f:
            f.write('process_user_registered_event')
        payload = json.loads(message.body.decode())
        if payload.get('event') != 'user_registered':
            return
        user_data = payload.get('data')
        user_id = user_data.get('user_id')
        async with httpx.AsyncClient() as client:
            response = await client.post('http://wallet:8002/wallets/create', json={'user_id': user_id})
        with open('log_2.txt', 'w') as f:
            f.write(f'{response.status_code} - {response.text}')


async def start_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange('user_events', aio_pika.ExchangeType.FANOUT, durable=True)
    queue = await channel.declare_queue('wallet_service_queue', durable=True)
    await queue.bind(exchange)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await process_user_registered_event(message)
