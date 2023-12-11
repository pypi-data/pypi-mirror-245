from typing import Protocol
from uuid import UUID, uuid4

from ..models import Model
from sqlmodel import Field


class UserProtocol(Protocol):
    def get_user_id(self): ...


class User(Model, table=True, UserProtocol):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
