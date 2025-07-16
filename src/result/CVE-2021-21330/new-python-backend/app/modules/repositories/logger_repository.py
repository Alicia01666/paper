from datetime import datetime, timedelta

from aiohttp import web
from database.db import ConnectPG
from database.models.logger_model import Logger
from database.schemas.logger_schema import LoggerSchema
from modules.repositories import BaseRepository
from modules.utils.logger import logger_info
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine

TIME_FORMAT = "%d/%m/%Y, %H:%M:%S"


class LoggerRepository(BaseRepository):
    def __init__(self, engine: AsyncEngine = None):
        super().__init__(engine)
        self.model = Logger
        self.schema = LoggerSchema()

    async def login_logger(self, ip: str):
        current_time = datetime.now().strftime(TIME_FORMAT)
        async with self.connect.get_session() as session:
            await session.execute(
                insert(Logger).values(logger_ip=ip, create_at=current_time)
            )
            await session.commit()
            await session.aclose()

        logger_info(f"Logger success for ip:{ip}")

    async def check_logger(self, ip: str):
        async with self.connect.get_session() as session:
            result = await session.execute(
                select(Logger)
                .where(Logger.logger_ip == ip)
                .order_by(Logger.create_at.desc())
            )
            logger: Logger | None = result.scalars().first()
            if logger is None:
                return False
            await session.aclose()

            return not self.__check_is_outtime_logger(create_at=logger.create_at)

    async def clear_log(self):
        async with self.connect.get_session() as session:
            result = await session.execute(select(Logger))
            loggers: list[Logger] = result.scalars().all()

            clear_loggers = [
                logger.id
                for idx, logger in enumerate(loggers)
                if idx >= 50
                or self.__check_is_outtime_logger(create_at=logger.create_at)
            ]

            await session.execute(delete(Logger).where(Logger.id.in_(clear_loggers)))
            await session.commit()
            await session.aclose()

    @classmethod
    def __check_is_outtime_logger(cls, create_at: str) -> bool:
        """
        Return true if
        """
        log_time = datetime.strptime(create_at, TIME_FORMAT)
        return datetime.now() > log_time + timedelta(hours=1)
