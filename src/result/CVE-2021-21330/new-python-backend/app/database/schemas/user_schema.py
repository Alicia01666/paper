from database.models.user_model import User
from database.schemas import BaseSQLSchema
from marshmallow_sqlalchemy import auto_field


class UserSchema(BaseSQLSchema):
    class Meta(BaseSQLSchema.Meta):
        model = User  # Optional: deserialize to model instances

    id: auto_field()
    name: auto_field()
    conditions: auto_field()
