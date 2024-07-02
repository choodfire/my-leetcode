from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserLogin):
    first_name: str
    last_name: str


class UserRead(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
