from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageType:
    id: str
    text: str
    sender: str
    time: float
    status: str = "sending"
    is_mine: Optional[bool] = False

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
