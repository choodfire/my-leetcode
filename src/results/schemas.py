from datetime import datetime, timedelta

from pydantic import BaseModel, field_validator

from src.results.consts import Language


class ResultWrite(BaseModel):
    language: Language
    code: str


class ResultRead(ResultWrite):
    id: int
    time: timedelta
    created_at: datetime
    user_id: int

    @field_validator("time")
    @classmethod
    def format_time(cls, value: timedelta) -> str:
        return str(value)
