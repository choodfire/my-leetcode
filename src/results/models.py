import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Interval, UUID

from src.models import Base
from src.results.consts import Language


class Result(Base):
    user_id = Column(UUID, ForeignKey('user.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    time = Column(Interval(native=True))
    language = Column(Enum(Language))
