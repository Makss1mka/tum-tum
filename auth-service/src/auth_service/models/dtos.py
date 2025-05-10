from pydantic import BaseModel, Field, EmailStr

class UserCredsCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(..., min_length=3, max_length=60)
    password: str = Field(..., min_length=3, max_length=30)

class UserCredsAuth(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=20)
    email: EmailStr | None = Field(None, min_length=3, max_length=60)
    password: str = Field(..., min_length=3, max_length=20)

class UserCredsAuthWithToken(BaseModel):
    token: str = Field(...)
