from config.redis_conf import redis_client
from globals import SESSION_EXPIRATION_TIME
from log.wrappers import log_entrance_debug
from log.loggers import SESSION_SERVICE_LOGGER
from exceptions import UnauthorizedException
import uuid
import json

@log_entrance_debug(SESSION_SERVICE_LOGGER)
async def create_session(user_id: str, username: str, role: str) -> str:
    session_id = str(uuid.uuid4())

    session_data = json.dumps({    
        "user_id": user_id,
        "username": username,
        "role": role
    })

    await redis_client.set(session_id, session_data, ex=SESSION_EXPIRATION_TIME)

    return session_id

@log_entrance_debug(SESSION_SERVICE_LOGGER)
async def get_session(session_id: str) -> dict:
    session_data = redis_client.get(session_id)

    if session_data == None:
        UnauthorizedException("Session id is expired.")

    return json.loads(session_data)

