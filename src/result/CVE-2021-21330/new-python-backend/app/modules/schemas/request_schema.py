from marshmallow import fields
from modules.schemas import BaseSchema


class VerifyRequest(BaseSchema):
    ip = fields.Str(description="ip", required=True, allow_none=False)


class LoginRequest(BaseSchema):
    ip = fields.Str(description="ip", required=True, allow_none=False)
    name = fields.Str(description="name", required=True, allow_none=False)
