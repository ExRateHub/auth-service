from pydantic import BaseModel


class UserRegistrationSchema(BaseModel):
    """User registration schema"""

    username: str
    password: str

class UserSchema(BaseModel):
    """User schema"""
    username: str