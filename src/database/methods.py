from src.database.model import session_maker, MovieInfo, MovieTicket, MovieSessions
from src.utils.log import logger
import asyncio
from sqlalchemy import select, exists, insert, delete


async def get_movies():
    async with session_maker() as session:
        try:
            query = select(MovieInfo).order_by(MovieInfo.start_time)
            stdm = await session.execute(query)
            result = stdm.scalars().all()
            return result
        except Exception as e:
            logger.error(f"Ошибка в методе healthcheck: {e}")
            await session.rollback()

async def get_tickets():
    async with session_maker() as session:
        try:
            query = select(MovieTicket).order_by(MovieTicket.start_time)
            stdm = await session.execute(query)
            result = stdm.scalars().all()
            return result
        except Exception as e:
            logger.error(f"Ошибка в методе healthcheck: {e}")
            await session.rollback()

async def get_sessions():
    async with session_maker() as session:
        try:
            query = select(MovieSessions).order_by(MovieSessions.start_time)
            stdm = await session.execute(query)
            result = stdm.scalars().all()
            return result
        except Exception as e:
            logger.error(f"Ошибка в методе healthcheck: {e}")
            await session.rollback()
