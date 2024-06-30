from datetime import datetime, timedelta

from pydantic import BaseModel


class ResultWrite(BaseModel):
    created_date: datetime
    time: timedelta


class ResultRead(ResultWrite):
    id: int
