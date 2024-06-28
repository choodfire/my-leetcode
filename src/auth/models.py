import uuid

import bcrypt
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlalchemy import UUID, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    _password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    @property
    def password(self) -> str:
        return self._password.decode("utf-8")

    @password.setter
    def password(self, password: SecretStr) -> None:
        _password_string = password.get_secret_value()
        self._password = bcrypt.hashpw(_password_string.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: SecretStr) -> bool:
        return pwd_context.verify(password.get_secret_value(), self.password)
