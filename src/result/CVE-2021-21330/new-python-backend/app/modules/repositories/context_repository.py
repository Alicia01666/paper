import typing

from database.models.context_model import Context
from database.schemas.context_schema import ContextSchema
from modules.repositories import BaseRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine


class ContextRepository(BaseRepository):
    def __init__(self, engine: AsyncEngine = None):
        """
        Initialize a new instance of the ContextRepository class.

        Parameters:
            engine (AsyncEngine, optional): The async engine to be used for database operations. Defaults to None.

        Attributes:
            model (type): The model class representing the context table in the database.
            schema (ContextSchema): The schema class used for serialization and deserialization of context data.

        """
        super().__init__(engine)
        self.model = Context
        self.schema = ContextSchema()

    async def get_all_context(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Retrieve all contexts from the database.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the serialized contexts.
        """
        async with self.connect.get_session() as session:
            query = select(Context)
            result = await session.execute(query)
            contexts = result.scalars().fetchall()

            return self.serialize(contexts, many=True)
