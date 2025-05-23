"""User credentials service module."""

from globals import JWT_ACCESS_EXPIRATION_TIME_MINUTES, JWT_REFRESH_EXPIRATION_TIME_MINUTES, \
    KAFKA_USER_CREDS_CREATE_TOPIC, KAFKA_USER_CREDS_DELETE_TOPIC
from log.loggers import USER_CREDS_SERVICE_LOGGER

from exceptions import ConflictException, BadRequestException, NotFoundException, NoContentException
from models.dtos import UserCredsCreate, UserCredsAuth, UserCredsUpdate, UserCredsReturnDto
from models.kafka_dtos import UserCredsCreateKafkaDto, UserCredsDeleteKafkaDto

from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import AsyncSessionMaker
from log.wrappers import log_entrance_debug
from models.entities import UserCredits
from sqlalchemy.orm import joinedload
from sqlalchemy import select, or_
from passlib.hash import bcrypt
from typing import List

from .jwt_token_service import create_token, validate_token, JwtPayload
from .session_service import create_session
from .kafka_service import KafkaProducer

import datetime
import uuid


@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def register(user_dto: UserCredsCreate) -> tuple[UserCredsReturnDto, str, str, str]:
    """Registers user with username and email and returns access token, refresh token and session_id.
    
    Args:
        user_dto (UserCredsCreate): User credentials data transfer object.
    
    Returns:
        tuple[UserCredsReturnDto, str, str, str]: user credentials data transfer object, access token, refresh token and session_id.
    
    Raises:
        ConflictException: If user with such name or email already exists.
    """
    
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

        await KafkaProducer().send_message(
            topic=KAFKA_USER_CREDS_CREATE_TOPIC,
            message=UserCredsCreateKafkaDto(new_user),
        )

        USER_CREDS_SERVICE_LOGGER.info(f"User was successfilly added | user id {new_user.id}")

        await session.commit()
        await session.refresh(new_user)

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

        return (UserCredsReturnDto(new_user), access_token, refresh_token, session_id)
        


@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def auth(user_dto: UserCredsAuth) -> tuple[UserCredsReturnDto, str, str, str]:
    """Authenticates user with username or email and password and returns access token, refresh token and session_id.
    
    Args:
        user_dto (UserCredsAuth): User credentials data transfer object.
    
    Returns:
        tuple[UserCredsReturnDto, str, str, str]: user credentials data transfer object, access token, refresh token and session_id.
    
    Raises:
        BadRequestException: If user credentials are invalid.
        NotFoundException: If user with such name or email is not found.
        ConflictException: If user with such name or email already exists.
    """
    
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

        return (UserCredsReturnDto(user), access_token, refresh_token, session_id)



@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def auth_with_jwt_token(token: str) -> tuple[UserCredsReturnDto, str, str, str]:
    """Authenticates user with JWT token and returns access token, refresh token and session_id.
    Args:
        token (str): JWT token.
    Returns:
        tuple[UserCredsReturnDto, str, str, str]: user credentials data transfer object, access token, refresh token and session_id.
    """

    async with AsyncSessionMaker() as session:
        session: AsyncSession

        jwt_data: JwtPayload = await validate_token(token)
        if jwt_data == None:
            raise BadRequestException("Invalid token")

        query = (
            select(UserCredits)
            .options(joinedload(UserCredits.role))
            .where(
                UserCredits.id == jwt_data.user_id
            )
        )
        user: UserCredits | None = (await session.execute(query)).scalars().first()

        if user == None:
            raise NotFoundException("Cannot find user with such name or email")
        
        if user.username != jwt_data.username or user.role.role != jwt_data.role or user.email != jwt_data.email:
            raise BadRequestException("Invalid token")

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

        return (UserCredsReturnDto(user), access_token, refresh_token, session_id)



@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def delete_user_creds(user_id: str) -> None:
    """Deletes user credentials by user id.
    
    Args:
        user_id (str): User id.
    
    Raises:
        NotFoundException: If user with such id is not found.
    """
    
    async with AsyncSessionMaker() as session:
        session: AsyncSession

        query = (
            select(UserCredits)
            .where(
                UserCredits.id == user_id
            )
        )
        deleting_user: UserCredits | None = (await session.execute(query)).scalars().first()

        if deleting_user == None:
            raise NotFoundException("Cannot find user with such id")

        await session.delete(deleting_user)

        await KafkaProducer().send_message(
            topic=KAFKA_USER_CREDS_DELETE_TOPIC,
            message=UserCredsDeleteKafkaDto(deleting_user),
        )

        USER_CREDS_SERVICE_LOGGER.info(f"User was successfully deleted | user id {deleting_user.id}")

        await session.commit()



@log_entrance_debug(USER_CREDS_SERVICE_LOGGER)
async def update_user_creds(user_id: str, user_dto: UserCredsUpdate) -> UserCredsReturnDto:
    """Updates user credentials by user id.
    
    Args:
        user_id (str): User id.
        user_dto (UserCredsUpdate): User credentials data transfer object.
    
    Returns:
        UserCredsReturnDto: User credentials data transfer object.

    Raises:
        NotFoundException: If user with such id is not found.
    """
    
    async with AsyncSessionMaker() as session:
        session: AsyncSession

        query = (
            select(UserCredits)
            .where(
                UserCredits.id == user_id
            )
        )
        user: UserCredits | None = (await session.execute(query)).scalars().first()

        if user == None:
            raise NotFoundException("Cannot find user with such id")

        is_smth_changed: bool = False

        if user_dto.username != None:
            is_smth_changed = True
            user.username = user_dto.username
        if user_dto.email != None:
            is_smth_changed = True
            user.email = user_dto.email
        if user_dto.new_password != None and user_dto.old_password != None:
            if bcrypt.verify(user_dto.old_password, user.password) == False:
                raise BadRequestException("Invalid password")
            else:
                is_smth_changed = True
                user.password = bcrypt.hash(user_dto.new_password)

        if is_smth_changed == True:
            await session.commit()
            
            return UserCredsReturnDto(user)
        else:
            raise NoContentException("Nothing to update")


