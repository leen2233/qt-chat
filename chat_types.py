from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class MessageType:
    class Status(Enum):
        SENDING = "sending"
        SENT = "sent"
        FAILED = "failed"
        READ = "read"

    id: str
    text: str
    is_mine: bool
    time: float
    status: Status | str = Status.SENDING

    reply_to: Optional["MessageType"] = None



@dataclass
class StatType:
    photos: Optional[int]
    videos: Optional[int]
    files: Optional[int]
    links: Optional[int]
    voices: Optional[int]


@dataclass
class UserType:
    username: str
    email: str
    id: str
    last_seen: float
    full_name: Optional[str] = None
    display_name: str = ""
    avatar: Optional[str] = None
    is_online: bool = False


@dataclass
class ChatType:
    id: str
    last_message: str
    updated_at: float
    user: UserType
