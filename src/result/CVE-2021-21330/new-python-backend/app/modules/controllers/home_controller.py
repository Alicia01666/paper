from datetime import datetime, timedelta

from aiohttp import web
from aiohttp_apispec import docs, json_schema, querystring_schema
from modules.repositories.logger_repository import LoggerRepository
from modules.repositories.user_repository import UserRepository
from modules.schemas.request_schema import LoginRequest, VerifyRequest
from modules.schemas.response_schema import LoginResponse, VerifyResponse


@docs(
    tags=["Heath Check"],
    summary="Check heath code",
    description="Check heath code",
    responses={
        200: {
            "description": "Success response",
        },
    },
)
async def welcome(request: web.Request):
    return web.Response(text="Welcome to home page")


@docs(
    tags=["Login Function"],
    summary="Login handle",
    description="Login handle",
    parameters=[
        {
            "in": "header",
            "name": "Authorization",
            "schema": {"type": "string", "format": "uuid"},
            "required": "true",
        }
    ],
    responses={
        200: {
            "schema": LoginResponse,
            "description": "Success response",
        },
    },
)
@json_schema(LoginRequest())
async def login_handle(request: web.Request):
    data: dict = await request.json()
    data = LoginRequest().dump(data)
    user_repo = UserRepository()

    name = str(data["name"]).lower()
    user = await user_repo.get_user_master()

    ip = str(data["ip"])
    if name in list(user.conditions) and ip:
        logger_repo = LoggerRepository(user_repo.connect.engine)
        await logger_repo.login_logger(ip=ip)
        await logger_repo.close()

        # await logger_repo.clear_log()

        return web.json_response(
            LoginResponse().dump(
                {
                    "result": {"check_status": True, "message": "Login Success"},
                }
            )
        )

    await user_repo.close()
    return web.json_response(
        LoginResponse().dump(
            {
                "result": {
                    "check_status": False,
                    "message": "Login False",
                }
            }
        )
    )


@docs(
    tags=["Login Function"],
    summary="Verify login status",
    description="Verify login status",
    parameters=[
        {
            "in": "header",
            "name": "Authorization",
            "schema": {"type": "string", "format": "uuid"},
            "required": "true",
        }
    ],
    responses={
        200: {
            "schema": VerifyResponse,
            "description": "Success response",
        },
    },
)
@querystring_schema(VerifyRequest())
async def verify_handle(request: web.Request):
    data = request.query
    ip = data["ip"]
    logger_repo = LoggerRepository()

    if await logger_repo.check_logger(ip):
        await logger_repo.close()
        return web.json_response(
            VerifyResponse().dump({"result": {"check_status": True}})
        )

    await logger_repo.close()
    return web.json_response(VerifyResponse().dump({"result": {"check_status": False}}))


def check_expired(date_str: str) -> bool:
    time = datetime.strptime(date_str, "%d/%m/%Y, %H:%M:%S")
    return datetime.now() > (time + timedelta(minutes=30))
