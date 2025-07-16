from database.models.logger_model import Logger
from database.schemas import BaseSQLSchema
from marshmallow_sqlalchemy import auto_field


class LoggerSchema(BaseSQLSchema):
    class Meta(BaseSQLSchema.Meta):
        model = Logger  # Optional: deserialize to model instances

    id: auto_field()
    logger_ip: auto_field()
    create_at: auto_field()
