from database.models.context_model import Context
from database.schemas import BaseSQLSchema
from marshmallow_sqlalchemy import auto_field


class ContextSchema(BaseSQLSchema):
    class Meta(BaseSQLSchema.Meta):
        model = Context  # Optional: deserialize to model instances

    id: auto_field()
    path: auto_field()
    label: auto_field()
    context: auto_field()
