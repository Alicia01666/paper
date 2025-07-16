from aiohttp import web
from database.db import ConnectPG
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import class_mapper


class ModelError(Exception):
    pass


class SchemaError(Exception):
    pass


class SessionError(Exception):
    pass


class BaseRepository:
    def __init__(self, engine: AsyncEngine = None):
        """
        Initializes the BaseRepository class with an optional database engine.

        Args:
            engine (AsyncEngine, optional): The database engine. Defaults to None.
        """
        self.schema = None
        self.model = None
        self.connect = ConnectPG(engine)

    def serialize(self, obj, many: bool = False):
        """
        Serializes an object or a list of objects into a dictionary representation.

        Args:
            obj (object or list): The object(s) to be serialized.
            many (bool, optional): Whether to serialize a single object or a list of objects. Defaults to False.

        Returns:
            dict or list: The serialized object(s) in dictionary representation.
        """
        try:
            columns = [c.key for c in class_mapper(self.model().__class__).columns]
        except Exception:
            raise TypeError("Model must is not None")

        if many:
            return [self._serialize_item(item, columns) for item in obj]

        return self._serialize_item(obj, columns)

    async def close(self):
        """
        Closes the database connection by disposing the database engine.
        """
        await self.connect.engine.dispose()

    def _serialize_item(self, item, columns):
        """
        Serializes a single item into a dictionary representation.

        Args:
            item (object): The item to be serialized.
            columns (list): The columns of the item's model.

        Returns:
            dict: The serialized item in dictionary representation.
        """
        return {c: getattr(item, c) for c in columns}
