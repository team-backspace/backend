from functools import wraps
from fastapi import Request
from fastapi.exceptions import HTTPException


def auth_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        app = request.app
        if not request.headers.get("authorization", None):
            raise HTTPException(status_code=401, detail="Unauthorized")
        elif not request.app.session_storage.is_exist(
            token=request.headers["authorization"]
        ):
            return HTTPException(status_code=403, detail="Authorization Error")
        return await func(*args, **kwargs)

    return wrapper
