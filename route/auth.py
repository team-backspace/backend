import aiohttp
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Request
from fastapi.exceptions import HTTPException

from app.ratelimit import global_limiter
from app.decorator import auth_required
from utils.etc import create_url
from model import LoginUser, ProfileUser
from starlette.responses import RedirectResponse

router = InferringRouter()


@cbv(router)
class Auth:
    @router.get("/login", tags=["authentication"])
    @global_limiter.limit("100/second")
    async def login(self, request: Request, application: str):
        if application == "google_login":
            return {
                "login_url": create_url(
                    "https://accounts.google.com/o/oauth2/v2/auth?",
                    scope="email profile",
                    state="security_token",
                    redirect_uri="http://localhost/callback/login",
                    response_type="code",
                    client_id=request.app.config["google_application_id"],
                    access_type="online",
                )
            }
        elif application == "google_register":
            return {
                "login_url": create_url(
                    "https://accounts.google.com/o/oauth2/v2/auth?",
                    scope="email profile",
                    state="security_token",
                    redirect_uri="http://localhost/callback/register",
                    response_type="code",
                    client_id=request.app.config["google_application_id"],
                    access_type="online",
                )
            }

    @router.get("/callback/{action_type}", tags=["authentication"])
    @global_limiter.limit("100/second")
    async def auth_callback(self, action_type: str, request: Request, code: str):
        if action_type == "login":
            try:
                token = await self.get_token_google(
                    request=request, code=code, callback_type="login"
                )
            except Exception as _:
                raise HTTPException(status_code=400, detail="Bad Request")
            user_data = await self.get_user_google(token=token)
            if not await LoginUser.exists(email=user_data["email"]):
                raise HTTPException(status_code=403, detail="User Not Found")
            login_user = await LoginUser.get(email=user_data["email"])
            key = request.app.session_storage.create(
                data={"email": user_data["email"], "id": user_data["id"]},
                expired_at=None,
            )
            return RedirectResponse(url=f'http://localhost:8000/callback?type=login&token={key}')
        elif action_type == "register":
            try:
                token = await self.get_token_google(
                    request=request, code=code, callback_type="register"
                )
            except Exception as _:
                raise HTTPException(status_code=400, detail="Bad Request")
            user_data = await self.get_user_google(token=token)
            if await LoginUser.exists(email=user_data["email"]):
                raise HTTPException(status_code=403, detail="User Already Registed")
            await ProfileUser.create(
                id=user_data["id"],
                name=user_data["name"],
                bio="새로운 유저를 환영해주세요!",
                profile_url=user_data["picture"],
                banner_url="",
            )
            await LoginUser.create(email=user_data["email"], user_id=user_data["id"])
            key = request.app.session_storage.create(
                data={"email": user_data["email"], "id": user_data["id"]},
                expired_at=None,
            )
            return RedirectResponse(url=f'http://localhost:8000/callback?type=register&token={key}')

    @router.patch("/profile", tags=["user"])
    @global_limiter.limit("100/second")
    @auth_required
    async def edit_profile(self, request: Request):
        data = await ProfileUser.get(
            id=request.app.session_storage.json.get(request.headers["Authorization"])
        )
        body = await request.json()
        data.name = body["name"] if body.get("name", None) else data.name
        data.bio = body["bio"] if body.get("bio", None) else data.bio
        data.profile_url = (
            body["profile_url"] if body.get("profile_url", None) else data.profile_url
        )
        data.banner_url = (
            body["banner_url"] if body.get("banner_url", None) else data.banner_url
        )
        await data.save()
        return {}

    @router.post("/logout", tags=["authentication"])
    @global_limiter.limit("100/second")
    @auth_required
    async def logout(self, request: Request):
        request.app.session_storage.delete(request.headers["authorization"])
        return {}

    async def get_token_google(self, request: Request, code: str, callback_type: str):
        opts = {
            "client_id": request.app.config["google_application_id"],
            "client_secret": request.app.config["google_application_secret"],
            "redirect_uri": f"http://localhost/callback/{callback_type}",
            "grant_type": "authorization_code",
            "code": code,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://www.googleapis.com/oauth2/v4/token", data=opts
            ) as response:
                data = await response.json()
                return data["access_token"]

    async def get_user_google(self, token: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            ) as response:
                data = await response.json()
                return data
