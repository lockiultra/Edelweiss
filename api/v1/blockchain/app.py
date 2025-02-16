import time
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from api.v1.blockchain.blockchain import Blockchain
from api.v1.blockchain.schemas import Transaction
from api.v1.blockchain.rabbitmq_consumer import start_consumer


@asynccontextmanager
async def lifespan(app: FastAPI): # noqa
    time.sleep(40)
    consumer_task = asyncio.create_task(start_consumer())
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        consumer_task.cancel()


app = FastAPI(lifespan=lifespan)
blockchain = Blockchain()


@app.get('/')
async def health_check():
    return {'message': 'Blockchain service is running'}


@app.get('/chain')
async def get_chain():
    return blockchain.get_chain()


@app.post('/add_transaction')
async def add_transaction(transaction: Transaction):
    if transaction.currency.lower() != 'alpenglow':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect token name'
        )
    new_block = blockchain.add_block(transaction.dict())
    return {'message': 'Block added', 'block': new_block}
