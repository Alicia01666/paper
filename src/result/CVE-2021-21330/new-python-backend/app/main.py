import asyncio

import aiohttp_autoreload
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_middlewares import cors_middleware
from database.db import ConnectPG
from modules.middlewares.authenticated import authenticated_middleware
from modules.middlewares.error_handle import error_middleware
from modules.repositories.user_repository import UserRepository
from modules.utils.config import DEBUG, PROD
from modules.utils.logger import logger_info
from router import routers


async def create_runner():
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True, origins=["http://localhost:3000"]),
            web.normalize_path_middleware(),
            authenticated_middleware,
            error_middleware,
        ]
    )
    app.add_routes(routes=routers)

    setup_aiohttp_apispec(app, swagger_path="/docs", version="0.0.2")
    return web.AppRunner(app)


async def start_server(host="0.0.0.0", port=8080):
    runner = await create_runner()
    await runner.setup()

    logger_info("Server start")
    site = web.TCPSite(runner, host, port)
    await site.start()


if __name__ == "__main__":
    connect_pg = ConnectPG()
    loop = asyncio.get_event_loop()

    if not PROD:
        asyncio.run_coroutine_threadsafe(connect_pg.init_database(), loop)
    if DEBUG:
        aiohttp_autoreload.start(loop)
    loop.run_until_complete(start_server())
    loop.run_forever()
