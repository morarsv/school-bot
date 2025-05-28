
from dataclasses import dataclass

from pytz import timezone
from sqlalchemy import BigInteger, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.config_data.config import Config, load_config
from datetime import datetime
from uuid import UUID, uuid4

config: Config = load_config()

engine = create_async_engine(url=config.database.url, pool_size=10, max_overflow=20, pool_timeout=30,)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


@dataclass
class Users(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    telegram_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, nullable=False)
    hero_name: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    hero_class: Mapped[str] = mapped_column(String(30), nullable=False)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    coins: Mapped[int] = mapped_column(Integer, default=0)
    school_lvl: Mapped[int] = mapped_column(Integer, default=0)
    last_daily_reward_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone('Asia/Bangkok')),
    )

    def __repr__(self):
        return (f"<User(nickname={self.hero_name}, xp={self.xp},"
                f"telegram_id={self.telegram_id}, hero_class={self.hero_class},"
                f"coins={self.coins}, school_lvl={self.school_lvl},"
                f"last_daily_reward_date={self.last_daily_reward_date},"
                f"created_at={self.created_at})>")


async def async_database_run():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
