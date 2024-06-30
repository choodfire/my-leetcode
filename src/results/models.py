from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.results.consts import Language


class Result(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    time: Mapped[timedelta]
    language: Mapped[Language]
