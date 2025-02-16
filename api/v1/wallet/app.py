import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.v1.wallet.db import init_db, get_db
from api.v1.wallet.schemas import WalletCreate, CurrencyEnum, WalletDeposit, WalletTransfer, WalletWithdraw
from api.v1.wallet.models import Wallet
from api.v1.wallet.dependencies import get_current_user
from api.v1.wallet.rabbitmq_consumer import start_consumer
from api.v1.wallet.rabbitmq_blockchain_publisher import blockchain_publisher_instance


@asynccontextmanager
async def lifespan(app: FastAPI): # noqa
    time.sleep(40)
    await init_db()
    consumer_task = asyncio.create_task(start_consumer())
    await blockchain_publisher_instance.connect()
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        consumer_task.cancel()
        await blockchain_publisher_instance.close()


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def service_health():
    return {'message': 'Wallet service is started'}


@app.post('/wallets/create')
async def create_wallets(wallet: WalletCreate, db: AsyncSession = Depends(get_db)):
    for currency in CurrencyEnum:
        new_wallet = Wallet(user_id=wallet.user_id, currency=currency, balance=0.0)
        db.add(new_wallet)
        await db.commit()
        await db.refresh(new_wallet)
    return {'message': 'All wallets created'}


@app.get('/wallets/')
async def get_wallets_by_user_id(db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    wallets = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    return wallets.scalars().all()


@app.post('/wallets/deposit')
async def deposit_to_wallet(deposit: WalletDeposit = Depends(), db: AsyncSession = Depends(get_db)):
    wallet = await db.execute(select(Wallet).where((Wallet.user_id == deposit.user_id) & (Wallet.currency == deposit.currency)))
    wallet = wallet.scalars().first()
    if not wallet:
        return {'message': 'Wallet not found'}
    wallet.balance += deposit.amount
    await db.commit()
    await db.refresh(wallet)

    if deposit.currency == CurrencyEnum.ALPENGLOW:
        transaction_data = {
            "sender": str(deposit.user_id),
            "receiver": str(deposit.user_id),
            "amount": deposit.amount,
            "currency": deposit.currency.value
        }
        await blockchain_publisher_instance.publish(transaction_data)

    return {'message': 'Wallet updated'}


@app.post('/wallets/withdraw')
async def withdraw_from_wallet(withdraw: WalletWithdraw = Depends(), db: AsyncSession = Depends(get_db), current_user: int = Depends(get_current_user)):
    wallet = await db.execute(select(Wallet).where(Wallet.user_id == withdraw.user_id and Wallet.currency == withdraw.currency))
    wallet = wallet.scalars().first()
    if not wallet:
        return {'message': 'Wallet not found'}
    if wallet.balance < withdraw.amount:
        return {'message': 'Not enough money'}
    wallet.balance -= withdraw.amount
    await db.commit()
    await db.refresh(wallet)

    if withdraw.currency == CurrencyEnum.ALPENGLOW:
        transaction_data = {
            "sender": str(withdraw.user_id),
            "receiver": withdraw.address,
            "amount": withdraw.amount,
            "currency": withdraw.currency.value
        }
        await blockchain_publisher_instance.publish(transaction_data)

    return {'message': 'Wallet updated'}


@app.post('/wallets/transfer')
async def transfer_to_wallet(transfer: WalletTransfer = Depends(), db: AsyncSession = Depends(get_db), current_user: int = Depends(get_current_user)):
    if current_user != transfer.user_id:
        return {'message': 'You are not authorized'}
    sender_wallet = await db.execute(select(Wallet).where(Wallet.user_id == transfer.sender_id and Wallet.currency == transfer.currency))
    sender_wallet = sender_wallet.scalars().first()
    if not sender_wallet:
        return {'message': 'Sender wallet not found'}
    if sender_wallet.balance < transfer.amount:
        return {'message': 'Not enough money'}
    receiver_wallet = await db.execute(select(Wallet).where(Wallet.user_id == transfer.receiver_id and Wallet.currency == transfer.currency))
    receiver_wallet = receiver_wallet.scalars().first()
    if not receiver_wallet:
        return {'message': 'Receiver wallet not found'}
    receiver_wallet.balance += transfer.amount
    sender_wallet.balance -= transfer.amount
    await db.commit()
    await db.refresh(sender_wallet)
    await db.refresh(receiver_wallet)

    if transfer.currency == CurrencyEnum.ALPENGLOW:
        transaction_data = {
            "sender": str(transfer.sender_id),
            "receiver": str(transfer.receiver_id),
            "amount": transfer.amount,
            "currency": transfer.currency.value
        }
        await blockchain_publisher_instance.publish(transaction_data)

    return {'message': 'Transfer completed'}
