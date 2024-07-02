from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    first_name: Mapped[str]
    last_name: Mapped[str]

    is_active: Mapped[bool]
    is_admin: Mapped[bool]

    results: Mapped[list["Result"]] = relationship("Result", back_populates="user")  # noqa: F821
