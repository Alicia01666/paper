from database.models.user_model import User
from modules.repositories import BaseRepository
from modules.utils.constant import LIST_CORRECT_ANSWER
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine


class UserRepository(BaseRepository):
    def __init__(self, engine: AsyncEngine = None):
        super().__init__(engine)

    async def get_user_by_id(self, id: int) -> User:
        async with self.connect.get_session() as session:
            result = await session.execute(select(User).where(User.id == id))
            await session.aclose()
            return result.scalar_one_or_none()

    async def get_user_master(self) -> User:
        return await self.get_user_by_id(id=1)
