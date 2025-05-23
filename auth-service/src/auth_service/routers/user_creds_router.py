"""User credentials service module."""

from models.dtos import UserCredsCreate, UserCredsAuth, UserCredsAuthWithToken, UserCredsReturnDto, UserCredsUpdate
from services.user_creds_service import register, auth, auth_with_jwt_token, delete_user_creds, update_user_creds
from fastapi import APIRouter, Response

user_creds_router = APIRouter()

@user_creds_router.post("/register")
async def router_register(resp: Response, user_dto: UserCredsCreate) -> UserCredsReturnDto:
    """Registers a new user.
    
    Args:
        resp (Response): Response object.
        user_dto (UserCredsCreate): User credentials data transfer object.

    Returns:
        UserCredsReturnDto: User credentials return data transfer object.
    """

    user_dto, access_token, refresh_token, session_id = await register(user_dto)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.set_cookie("access_token", value=access_token, httponly=True, samesite="strict")
    resp.set_cookie("refresh_token", value=refresh_token, httponly=True, samesite="strict")
    resp.status_code = 200

    return user_dto


@user_creds_router.post("/auth")
async def router_auth(user_dto: UserCredsAuth, resp: Response) -> UserCredsReturnDto:
    """Authenticates a user.
    Args:
        user_dto (UserCredsAuth): User credentials auth data transfer object.
        resp (Response): Response object.
    Returns:
        UserCredsReturnDto: User credentials return data transfer object.
    """

    user_dto, access_token, refresh_token, session_id = await auth(user_dto)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.set_cookie("access_token", value=access_token, httponly=True, samesite="strict")
    resp.set_cookie("refresh_token", value=refresh_token, httponly=True, samesite="strict")
    resp.status_code = 200

    return user_dto


@user_creds_router.post("/auth_with_token")
async def router_auth_with_token(token: UserCredsAuthWithToken, resp: Response) -> UserCredsReturnDto:
    """Authenticates a user using a JWT token.
    Args:
        token (UserCredsAuthWithToken): User credentials auth with token data transfer object.
        resp (Response): Response object.
    Returns:
        UserCredsReturnDto: User credentials return data transfer object.
    """

    user_dto, _, _, session_id = await auth_with_jwt_token(token.token)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.status_code = 200

    return user_dto


@user_creds_router.post("/refresh")
async def refresh_token(token: UserCredsAuthWithToken, resp: Response):
    """Refreshes the access token using the refresh token.
    Args:
        token (UserCredsAuthWithToken): User credentials auth with token data transfer object.
        resp (Response): Response object.
    """

    access_token, _, session_id = await auth_with_jwt_token(token.token)

    resp.set_cookie("session_id", value=session_id, httponly=True, samesite="strict")
    resp.set_cookie("access_token", value=access_token, httponly=True, samesite="strict")
    resp.status_code = 200

    return {"status": "OK"}


@user_creds_router.delete("/{user_id}")
async def delete_user_creds(user_id: str, resp: Response):
    await delete_user_creds(user_id)

    resp.status_code = 200

    return {"status": "OK", "message": "User deleted successfully"}


@user_creds_router.put("/{user_id}")
async def update_user_creds(user_id: str, user_dto: UserCredsUpdate, resp: Response):
    """Updates user credentials.
    
    Args:
        user_id (str): User ID.
        user_dto (UserCredsUpdate): User credentials auth data transfer object.
        resp (Response): Response object.
    """

    await update_user_creds(user_id, user_dto)

    resp.status_code = 200

    return {"status": "OK", "message": "User updated successfully"}
