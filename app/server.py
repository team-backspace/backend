from fastapi import FastAPI, Request

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.ratelimit import global_limiter
from app.session import SessionStorage

from route.auth import router as auth_router
from tortoise.contrib.fastapi import register_tortoise

from route.project import router as project_router

server = FastAPI(
    title="Spacebook Backend",
    description="Spacebook Backend, fastapi",
    version="0.1",
    docs_url="/development-docs",
    redoc_url="/development-redoc",
)
server.state_limiter = global_limiter
server.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

server.include_router(auth_router)
server.include_router(project_router)
server.session_storage = SessionStorage(secret="dbwd2d92bedad2hadb000883n2d9a2")


register_tortoise(
    server,
    db_url="sqlite://database/db.sqlite3",
    modules={"models": ["model"]},
    generate_schemas=True,
)


@server.get("/")
async def main(_request: Request):
    return {"hello": "world"}
