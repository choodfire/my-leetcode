import datetime

from sqlalchemy import Column, DateTime, Interval

from src.models import Base


class Result(Base):  # TODO: Add user, language
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    time = Column(Interval(native=True))
