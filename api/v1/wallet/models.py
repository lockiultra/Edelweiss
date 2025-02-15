from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    currency: Mapped[str] = mapped_column(String, index=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
