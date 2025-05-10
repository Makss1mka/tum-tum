from globals import JWT_ACCESS_EXPIRATION_TIME_MINUTES, JWT_REFRESH_EXPIRATION_TIME_MINUTES
from exceptions import ConflictException, BadRequestException, NotFoundException
from models.dtos import UserCredsCreate, UserCredsAuth
from log.loggers import USER_CREDS_SERVICE_LOGGER
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import AsyncSessionMaker
from log.wrappers import log_entrance_debug
from sqlalchemy import select, or_, and_
from models.entities import UserCredits
from sqlalchemy.orm import joinedload
from passlib.hash import bcrypt
from typing import List

from .session_service import create_session
from .jwt_token_service import create_token, validate_token, JwtPayload

import datetime
import uuid


#
# Returns access token, refresh token and session_id
#
@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def register(user_dto: UserCredsCreate) -> tuple[str, str, str]:
    async with AsyncSessionMaker() as session:
        session: AsyncSession

        users: List[UserCredits] = (await session.execute(
            select(UserCredits)
            .where(
                or_(
                    UserCredits.username == user_dto.username,
                    UserCredits.email == user_dto.email
                )
            )
        )).scalars().all()

        if len(users) != 0:
            if len(users) > 1:
                raise ConflictException("Those name and email have already taken.")
            elif users[0].username == user_dto.username:
                raise ConflictException("This name has already taken.")
            else:
                raise ConflictException("This email has already taken.")

        new_user = UserCredits(
            id=str(uuid.uuid4()),
            username=user_dto.username,
            password=bcrypt.hash(user_dto.password),
            email=user_dto.email,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            role_id=0
        )

        session.add(new_user)

        session_id: str = await create_session(
            user_id=new_user.id,
            username=new_user.username,
            role="USER"
        )
        access_token: str = await create_token(
            user_id=new_user.id,
            username=new_user.username,
            role="USER",
            exp_time=JWT_ACCESS_EXPIRATION_TIME_MINUTES
        ) 
        refresh_token: str = await create_token(
            user_id=new_user.id,
            username=new_user.username,
            role="USER",
            exp_time=JWT_REFRESH_EXPIRATION_TIME_MINUTES
        )

        USER_CREDS_SERVICE_LOGGER.info(f"User was successfilly added | user id {new_user.id}")

        await session.commit()
        await session.refresh(new_user)

        return (access_token, refresh_token, session_id)
        

#
# Returns access token, refresh token and session_id
#
@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def auth(user_dto: UserCredsAuth) -> tuple[str, str, str]:
    if user_dto.username == None and user_dto.email == None:
        raise BadRequestException("Invalid creds for authentification")

    async with AsyncSessionMaker() as session:
        session: AsyncSession

        query = (
            select(UserCredits)
            .options(joinedload(UserCredits.role))
            .where(
                or_(
                    UserCredits.email == user_dto.email,
                    UserCredits.username == user_dto.username
                )          
            )
        )
        user: UserCredits | None = (await session.execute(query)).scalars().first()

        if user == None:
            raise NotFoundException("Cannot find user with such name or email")
        
        if bcrypt.verify(user_dto.password, user.password) == False:
            raise BadRequestException("Invalid password")

        session_id: str = await create_session(
            user_id=str(user.id),
            username=user.username,
            role=user.role.role
        )
        access_token: str = await create_token(
            user_id=str(user.id),
            username=user.username,
            role=user.role.role,
            exp_time=JWT_ACCESS_EXPIRATION_TIME_MINUTES
        ) 
        refresh_token: str = await create_token(
            user_id=str(user.id),
            username=user.username,
            role=user.role.role,
            exp_time=JWT_REFRESH_EXPIRATION_TIME_MINUTES
        )

        return (access_token, refresh_token, session_id)


#
# Returns access token, refresh token and session_id
#
@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def auth_with_jwt_token(token: str) -> tuple[str, str, str]:
    jwt_data: JwtPayload = await validate_token(token)

    session_id: str = await create_session(
        user_id=jwt_data.user_id,
        username=jwt_data.username,
        role=jwt_data.role
    )
    access_token: str = await create_token(
        user_id=jwt_data.user_id,
        username=jwt_data.username,
        role=jwt_data.role,
        exp_time=JWT_ACCESS_EXPIRATION_TIME_MINUTES
    ) 
    refresh_token: str = await create_token(
        user_id=jwt_data.user_id,
        username=jwt_data.username,
        role=jwt_data.role,
        exp_time=JWT_REFRESH_EXPIRATION_TIME_MINUTES
    )

    return (access_token, refresh_token, session_id)


