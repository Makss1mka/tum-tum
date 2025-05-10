from exceptions import UnauthorizedException
from globals import JWT_SECRET_KEY
import datetime
from log.wrappers import log_entrance_debug
from log.loggers import JWT_SERVICE_LOGGER
import jwt

class JwtPayload:
    def __init__(self, user_id: str, username: str, role: str, exp_time: int):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.exp_time = exp_time

    def to_dict(self):
        return {
            "id": self.user_id,
            "sub": self.username,
            "role": self.role,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=self.exp_time)
        }
    
    @staticmethod
    def from_dict(dict_payload: dict):
        return JwtPayload(
            user_id=dict_payload.get("id", None),
            username=dict_payload.get("sub", None),
            role=dict_payload.get("role", None),
            exp_time=dict_payload.get("exp_time", None)
        )



@log_entrance_debug(JWT_SERVICE_LOGGER)
async def create_token(username: str, user_id: str, role: str, exp_time: int) -> str:
    payload = JwtPayload(
        user_id=user_id,
        username=username,
        role=role,
        exp_time=exp_time
    )
    
    token = jwt.encode(payload=payload.to_dict(), key=JWT_SECRET_KEY, algorithm="HS256")
    return token

@log_entrance_debug(JWT_SERVICE_LOGGER)
async def validate_token(token: str) -> JwtPayload:
    try:
        payload = jwt.decode(jwt=token, key=JWT_SECRET_KEY, algorithms=["HS256"])
        return JwtPayload.from_dict(payload)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")
