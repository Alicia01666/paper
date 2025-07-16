from aiohttp import web
from aiohttp_apispec import docs
from database.schemas.context_schema import ContextSchema
from modules.repositories.context_repository import ContextRepository
from modules.schemas.response_schema import ContentResponse


@docs(
    tags=["Context API"],
    summary="Get context for memories page",
    description="Get context for memories page",
    responses={
        200: {
            "schema": ContentResponse,
            "description": "Success response",
        },
    },
)
async def get_context(request: web.Request):
    repo = ContextRepository()
    contexts = await repo.get_all_context()
    await repo.close()

    return web.json_response(
        ContentResponse().dump(
            {
                "result": contexts,
            }
        )
    )
