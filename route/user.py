from fastapi import Request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.exceptions import HTTPException


from app.ratelimit import global_limiter
from app.decorator import auth_required
from model import ProfileUser

router = InferringRouter()


@cbv(router)
class User:
    @router.get("/user/{user_id}", tags=["user"])
    @global_limiter.limit("100/second")
    async def get_user(self, request: Request, user_id: str):
        if user_id == '@me':
            if not request.headers.get("authorization", None):
                raise HTTPException(status_code=401, detail="Unauthorized")
            elif not request.app.session_storage.is_exist(
                    token=request.headers["authorization"]
            ):
                return HTTPException(status_code=403, detail="Authorization Error")
            user_data = request.app.session_storage.json.get(request.headers["Authorization"])
            data = await ProfileUser.get(id=user_data["id"])
        else:
            if not await ProfileUser.exists(id=user_id):
                raise HTTPException(status_code=404, detail="Not Found")
            data = await ProfileUser.get(id=user_id)

        return {
            "id": data.id,
            "name": data.name,
            "bio": data.bio,
            "profile_url": data.profile_url,
            "banner_url": data.banner_url,
        }

    @router.get("/online", tags=["user"])
    @global_limiter.limit("100/second")
    async def get_online_user(self, request: Request):
        return {"online_user": len(request.app.session_storage.json)}

    










