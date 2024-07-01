from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class User(Base):
    username: Mapped[str]
    email: Mapped[str | None] = mapped_column(unique=True)

    first_name: Mapped[str]
    last_name: Mapped[str | None]

    _password: Mapped[bytes]

    is_active: Mapped[bool]
    is_admin: Mapped[bool]

    results: Mapped[list["Result"]] = relationship("Result", back_populates="user")  # noqa: F821
