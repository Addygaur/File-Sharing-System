from dataclasses import dataclass, field
from datetime import datetime
import uuid
from enum import Enum


@dataclass(frozen=True)
class UserInfo:

    first_name: str
    last_name: str
    email: str
    password: str
    role: str = 'user'
    user_id: str = None
    is_active: bool = False
    creation_datetime: datetime = None

    def __post_init__(self):
        if not self.is_active:
            object.__setattr__(self, "is_active", True)
        if not self.user_id:
            object.__setattr__(self, "user_id", str(uuid.uuid4().hex))
        if not self.creation_datetime:
            object.__setattr__(self, "creation_datetime", datetime.now())

    @staticmethod
    def from_json(json_data):
        return UserInfo(**json_data)

    def to_json(self):
        payload = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "is_active": str(self.is_active),
            "creation_datetime": str(self.creation_datetime)
        }
        return payload


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'
