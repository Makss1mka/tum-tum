from fastapi import APIRouter, Response
from models.dtos import UserCredsCreate, UserCredsAuth, UserCredsAuthWithToken
from services.user_creds_service import register, auth, auth_with_jwt_token

user_creds_router = APIRouter()

@user_creds_router.post("/register")
async def router_register(resp: Response, user_dto: UserCredsCreate):
    access_token, refresh_token, session_id = await register(user_dto)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.set_cookie("access_token", value=access_token, httponly=True, samesite="strict")
    resp.set_cookie("refresh_token", value=refresh_token, httponly=True, samesite="strict")
    resp.status_code = 200

    return {"status": "OK"}


@user_creds_router.post("/auth")
async def router_auth(user_dto: UserCredsAuth, resp: Response):
    access_token, refresh_token, session_id = await auth(user_dto)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.set_cookie("access_token", value=access_token, httponly=True, samesite="strict")
    resp.set_cookie("refresh_token", value=refresh_token, httponly=True, samesite="strict")
    resp.status_code = 200

    return {"status": "OK"}


@user_creds_router.post("/auth_with_token")
async def router_auth_with_token(token: UserCredsAuthWithToken, resp: Response):
    _, _, session_id = await auth_with_jwt_token(token.token)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.status_code = 200

    return {"status": "OK"}


@user_creds_router.post("/refresh")
async def router_auth_with_token(token: UserCredsAuthWithToken, resp: Response):
    access_token, _, session_id = await auth_with_jwt_token(token.token)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.set_cookie("access_token", value=access_token, httponly=True, samesite="strict")
    resp.status_code = 200

    return {"status": "OK"}

