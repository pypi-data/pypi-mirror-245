from datetime import datetime, timezone

from sqlmodel import SQLModel


Model = SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
