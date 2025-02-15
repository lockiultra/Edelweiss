from contextlib import asynccontextmanager
from datetime import datetime, UTC, timedelta
import time

import jwt

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.v1.common.utils import get_password_hash, verify_password
from api.v1.auth.models import User
from api.v1.auth.schemas import UserCreate, UserLogin
from api.v1.auth.db import get_db, init_db
from api.v1.auth.rabbitmq_publisher import publish_user_registered_event, publisher_instance


@asynccontextmanager
async def lifespan(app: FastAPI): # noqa
    time.sleep(40)
    await init_db()
    await publisher_instance.connect()
    yield
    await publisher_instance.close()


app = FastAPI(lifespan=lifespan)

SECRET_KEY = 'secret'


@app.get('/')
async def service_health():
    return {'message': 'Auth service is started'}


@app.post('/register')
async def register(user_create: UserCreate = Depends(), db: AsyncSession = Depends(get_db)):
    hashed_password: str = get_password_hash(user_create.password)
    new_user = User(username=user_create.username, password=hashed_password, email=user_create.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    event_data = {
        'event': 'user_registered',
        'data': {
            'user_id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
    }

    await publish_user_registered_event(event_data)

    return new_user


@app.post('/login')
async def login(user_login: UserLogin = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.username == user_login.username))
    user = user.scalars().first()
    if not user:
        return {"Message": "User not found"}
    if not verify_password(user_login.password, user.password):
        return {"Message": "Incorrect password"}
    payload = {
        'sub': user.username,
        'user_id': user.id,
        'exp': datetime.now(UTC) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return {'access_token': token, 'token_type': 'bearer'}


@app.get('/users')
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()
