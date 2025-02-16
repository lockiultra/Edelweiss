from pydantic import BaseModel, Field


class Block(BaseModel):
    index: int
    timestamp: float
    data: dict
    previous_hash: str
    hash: str


class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float
    currency: str = Field(default='alpenglow')
