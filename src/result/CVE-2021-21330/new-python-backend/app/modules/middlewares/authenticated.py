from aiohttp import web
from modules.schemas.response_schema import ErrorResponse
from modules.utils.config import ALLOW_TOKEN


@web.middleware
async def authenticated_middleware(request: web.Request, handler):
    if not request.path.startswith("/api/app/"):
        return await handler(request)

    try:
        scheme, token = request.headers["Authorization"].strip().split(" ")
    except KeyError:
        return web.json_response(
            ErrorResponse().dump(
                {
                    "status_code": 401,
                    "error_detail": {
                        "error_code": "",
                        "message": "Missing authorization header",
                    },
                }
            ),
            status=401,
        )
    except ValueError:
        return web.json_response(
            ErrorResponse().dump(
                {
                    "status_code": 403,
                    "error_detail": {
                        "error_code": "",
                        "message": "Invalid authorization header",
                    },
                }
            ),
            status=403,
        )

    if scheme != "Bearer":
        return web.json_response(
            ErrorResponse().dump(
                {
                    "status_code": 403,
                    "error_detail": {
                        "error_code": "",
                        "message": "Invalid token scheme",
                    },
                }
            ),
            status=403,
        )
    if token not in ALLOW_TOKEN:
        return web.json_response(
            ErrorResponse().dump(
                {
                    "status_code": 403,
                    "error_detail": {
                        "error_code": "",
                        "message": "Token doesn't exist",
                    },
                }
            ),
            status=403,
        )

    return await handler(request)
