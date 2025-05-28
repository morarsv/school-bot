import logging
from sqlalchemy import select, update, func
from datetime import datetime
from src.database.models import Users
from sqlalchemy.ext.asyncio import async_sessionmaker

logger = logging.getLogger(__name__)


async def get_user_by_tg_id(
        async_session: async_sessionmaker,
        telegram_id: int
) -> Users:
    async with async_session() as session:
        stmt = (select(Users).where(Users.telegram_id == telegram_id))
        return await session.scalar(stmt)


async def get_user_by_hero_name(
        async_session: async_sessionmaker,
        hero_name: str
) -> Users:
    async with async_session() as session:
        lower_hero_name = hero_name.lower()
        stmt = (select(Users).where(func.lower(Users.hero_name) == lower_hero_name))
        return await session.scalar(stmt)


async def update_xp_by_tg_id(
        async_session: async_sessionmaker,
        telegram_id: int,
        xp: int
) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.telegram_id == telegram_id).
                values(
                    xp=xp
                ))
        await session.execute(stmt)
        await session.commit()


async def update_coins_by_tg_id(
        async_session: async_sessionmaker,
        telegram_id: int,
        coins: int
) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.telegram_id == telegram_id).
                values(
                    coins=coins
                ))
        await session.execute(stmt)
        await session.commit()


async def update_coins_and_xp_by_tg_id(
        async_session: async_sessionmaker,
        telegram_id: int,
        xp: int,
        coins: int
) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.telegram_id == telegram_id).
                values(
                    coins=coins,
                    xp=xp
                ))
        await session.execute(stmt)
        await session.commit()


async def update_school_lvl_and_coins_by_tg_id(
        async_session: async_sessionmaker,
        telegram_id: int,
        school_lvl: int,
        coins: int
) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.telegram_id == telegram_id).
                values(
                    school_lvl=school_lvl,
                    coins=coins
                ))
        await session.execute(stmt)
        await session.commit()


async def update_last_daily_reward_date_by_tg_id(
        async_session: async_sessionmaker,
        telegram_id: int,
        date: datetime
) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.telegram_id == telegram_id).
                values(
                    last_daily_reward_date=date
                ))
        await session.execute(stmt)
        await session.commit()


async def add_user(
        async_session: async_sessionmaker,
        user: Users
) -> None:
    async with async_session() as session:
        session.add(user)
        await session.commit()


async def get_all_users(
        async_session: async_sessionmaker
) -> list[Users]:
    async with async_session() as session:
        stmt = (select(Users).
                order_by(Users.hero_name.asc()))
        result = await session.scalars(stmt)
        return result.all()


async def get_rating_names_30(
        async_session: async_sessionmaker
) -> list[Users]:
    async with async_session() as session:
        stmt = (select(Users).
                order_by(Users.hero_name.asc(), Users.xp.desc()).
                limit(30))
        result = await session.scalars(stmt)
        return result.all()


async def find_heroes(
        async_session: async_sessionmaker,
        hero_name: list[str]
) -> list[Users]:
    async with async_session() as session:
        hero_name_lowered = [name.lower() for name in hero_name]
        stmt = (select(Users).
                where(func.lower(Users.hero_name).in_(hero_name_lowered)))
        result = await session.scalars(stmt)
        return result.all()
