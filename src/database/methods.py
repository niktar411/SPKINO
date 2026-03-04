from src.database.model import session_maker
from src.database.model import MovieSessions
from src.utils.log import logger
import asyncio
from sqlalchemy import select, exists, insert, delete


async def healthcheck():
    async with session_maker() as session:
        try:
            query = select(MovieSessions)
            stdm = await session.execute(query)
            result = stdm.scalars().all()
            return result
        except Exception as e:
            logger.error(f"Ошибка в методе healthcheck: {e}")
            await session.rollback()

a = asyncio.run(healthcheck())
print(a)
