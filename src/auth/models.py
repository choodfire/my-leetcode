import bcrypt
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.results.models import Result

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    username: Mapped[str]
    email: Mapped[str | None] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    results: Mapped[list["Result"]] = relationship("Result", back_populates="users")
    _password: Mapped[bytes]

    @property
    def password(self) -> str:
        return self._password.decode("utf-8")

    @password.setter
    def password(self, password: SecretStr) -> None:
        _password_string = password.get_secret_value()
        self._password = bcrypt.hashpw(_password_string.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: SecretStr) -> bool:
        return pwd_context.verify(password.get_secret_value(), self.password)
