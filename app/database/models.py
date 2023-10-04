from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime
from typing import List
import config

engine = create_async_engine(
    config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Location(Base):
    __tablename__ = 'location'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    name: Mapped[str] = mapped_column(String(120))
    buy_device: Mapped[str] = mapped_column(String(1), nullable=True)
    buy_stick: Mapped[str] = mapped_column(String(1), nullable=True)
    guarantee: Mapped[str] = mapped_column(String(1), nullable=True)
    firmware: Mapped[str] = mapped_column(String(1), nullable=True)
    cleaning: Mapped[str] = mapped_column(String(1), nullable=True)


class Admin(Base):
    __tablename__ = 'admin'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
