from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None
    first_name: str
    last_name: str | None
    password: str


class UserRead(BaseModel):
    username: str
    email: EmailStr | None
    first_name: str
    last_name: str | None
    is_active: bool
    is_admin: bool
