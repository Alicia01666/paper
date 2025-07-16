from database.models import Base
from database.models.context_model import Context
from database.models.user_model import User
from modules.utils.config import HOST, PASSWORD, PG_URL, PORT, SCHEMA, USER
from modules.utils.constant import LIST_CONTEXT, LIST_CORRECT_ANSWER
from modules.utils.logger import logger_error, logger_info
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


def get_engine() -> AsyncEngine:
    """
    Returns an asynchronous SQLAlchemy engine object for connecting to a PostgreSQL database.

    :return: An asynchronous SQLAlchemy engine object.
    """
    url = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{SCHEMA}"
    # if PG_URL is not None:
    #     url = f"postgresql+asyncpg://{PG_URL}"
    engine = create_async_engine(url)
    return engine


class ConnectPG(object):
    def __new__(cls, engine: AsyncEngine = None):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConnectPG, cls).__new__(cls)
        return cls.instance

    def __init__(self, engine: AsyncEngine = None):
        self._engine = engine if engine else get_engine()

    @property
    def engine(self):
        return self._engine

    async def init_database(self):
        try:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

                await conn.execute(
                    insert(User).values(
                        id=1, name="Ngao Ngo", conditions=LIST_CORRECT_ANSWER
                    )
                )
                await conn.execute(insert(Context).values(LIST_CONTEXT))

                await conn.commit()

            await self._engine.dispose()
            logger_info("Init database done!")
        except Exception as error:
            logger_error(str(error))

    def get_session(self) -> AsyncSession:
        return AsyncSession(self._engine, expire_on_commit=False)
