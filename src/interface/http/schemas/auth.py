import uuid

from pydantic import BaseModel


class UserRegistrationSchema(BaseModel):
    """User registration schema"""

    username: str
    password: str

class UserLoginSchema(BaseModel):
    """User login schema"""
    login: str
    password: str



class UserSchema(BaseModel):
    """User schema"""
    username: str
    id: uuid.UUID

class TokenSchema(BaseModel):
    """Token schema"""
    key: str

class LoginResponseSchema(BaseModel):
    """Login response schema"""
    user: UserSchema
    token_key: TokenSchema
