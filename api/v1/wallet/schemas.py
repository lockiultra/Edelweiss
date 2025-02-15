from pydantic import BaseModel
from enum import Enum


class CurrencyEnum(str, Enum):
    EDELIUM: str = 'Edelium'
    ALPENGLOW: str = 'Alpenglow'
    FROSTBYTE: str = 'Frostbyte'
    TON: str = 'Ton'
    BITCOIN: str = 'Bitcoin'
    ETHEREUM: str = 'Ethereum'


class Wallet(BaseModel):
    user_id: int
    currency: CurrencyEnum
    balance: float


class WalletCreate(BaseModel):
    user_id: int


class WalletDeposit(BaseModel):
    user_id: int
    currency: CurrencyEnum
    amount: float


class WalletTransfer(BaseModel):
    sender_id: int
    receiver_id: int
    currency: CurrencyEnum
    amount: float


class WalletWithdraw(BaseModel):
    user_id: int
    currency: CurrencyEnum
    amount: float
    address: str


class WalletBalance(BaseModel):
    user_id: int
    currency: CurrencyEnum
    balance: float
