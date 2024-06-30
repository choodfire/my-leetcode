from datetime import datetime, timedelta

from pydantic import BaseModel


class ResultWrite(BaseModel):
    language: str
    code: str


class ResultRead(ResultWrite):
    id: int
    time: timedelta
    created_at: datetime
    user_id: int
