"""User credentials service module."""

from pydantic import BaseModel, Field, EmailStr
from .entities import UserCredits

class UserCredsCreate(BaseModel):
    """User credentials create DTO.
    
    Fields:
        username (str): Username.
        email (str): Email.
        password (str): Password.
    """

    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(..., min_length=3, max_length=60)
    password: str = Field(..., min_length=3, max_length=30)


class UserCredsUpdate(BaseModel):
    """User credentials update DTO.
    
    Fields:
        username (str): Username.
        email (str): Email.
        new_password (str): New password.
        old_password (str): Old password.
    """

    username: str | None = Field(None, min_length=3, max_length=20)
    email: EmailStr | None = Field(None, min_length=3, max_length=60)
    new_password: str | None = Field(None, min_length=3, max_length=30)
    old_password: str | None = Field(None, min_length=3, max_length=30)


class UserCredsReturnDto:
    """User credentials return DTO.
    
    Fields:
        id (str): User id.
        username (str): Username.
        email (str): Email.
    """

    def __init__(self, user_dto: UserCredits):
        """Initializes UserCredsReturnDto with user credentials data transfer object.

        Args:
            user_dto (UserCredits): User credentials data transfer object.
        """

        self.id: str = user_dto.id
        self.username: str = user_dto.username
        self.email: str = user_dto.email


class UserCredsAuth(BaseModel):
    """User credentials auth DTO.
    
    Fields:
        username (str): Username.
        email (str): Email.
        password (str): Password.
    """

    username: str | None = Field(None, min_length=3, max_length=20)
    email: EmailStr | None = Field(None, min_length=3, max_length=60)
    password: str = Field(..., min_length=3, max_length=20)


class UserCredsAuthWithToken(BaseModel):
    """User credentials auth with token DTO.
    
    Fields:
        token (str): JWT token.
    """

    token: str = Field(...)
