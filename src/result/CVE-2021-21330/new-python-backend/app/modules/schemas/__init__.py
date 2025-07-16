from typing import Any

from marshmallow import Schema


class BaseSchema(Schema):
    def dump(self, obj: Any = None, *, many: bool | None = None):
        if obj is not None:
            obj = self.load(obj)
        return super().dump(obj, many=many)

    def dumps(self, obj: Any = None, *args, many: bool | None = None, **kwargs):
        return super().dumps(obj, *args, many=many, **kwargs)
