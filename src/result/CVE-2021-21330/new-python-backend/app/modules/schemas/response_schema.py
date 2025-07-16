from database.schemas.context_schema import ContextSchema
from marshmallow import fields
from modules.schemas import BaseSchema


class BaseResponse(BaseSchema):
    status = fields.Bool(default=True)
    status_code = fields.Integer(strict=True, default=200)


class VerifyStatus(BaseSchema):
    check_status = fields.Bool(required=True)


class LoginStatus(BaseSchema):
    check_status = fields.Bool(required=True)
    message = fields.Str(required=True)


class ContentResult(BaseSchema):
    id = fields.Int(required=True)
    path = fields.Str(required=True)
    label = fields.Str(required=True)
    context = fields.Str(dump_default="")


class ErrorDetail(BaseSchema):
    field = fields.Str()
    error_code = fields.Str(required=True)
    message = fields.Str(required=True)


class LoginResponse(BaseResponse):
    result = fields.Nested(LoginStatus(), required=True)


class VerifyResponse(BaseResponse):
    result = fields.Nested(VerifyStatus(), required=True)


class ContentResponse(BaseResponse):
    result = fields.Nested(ContentResult(many=True), required=True)


class ErrorResponse(BaseResponse):
    status = fields.Bool(default=False)
    error_detail = fields.Nested(ErrorDetail(), required=True)
