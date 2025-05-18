from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class MessageType:
    class Status(Enum):
        SENDING = "sending"
        SENT = "sent"
        FAILED = "failed"
        READ = "read"

    id: int
    text: str
    sender: str
    time: str
    status: Status = Status.SENDING
    
    reply_to: Optional["MessageType"] = None


@dataclass
class StatType:
    photos: Optional[int]
    videos: Optional[int]
    files: Optional[int]
    links: Optional[int]
    voices: Optional[int]


@dataclass
class ChatType:
    id: int
    avatar: str
    name: str
    last_message: str
    time: str
    phone_number: str
    username: str
    stats: StatType
    messages: List[MessageType]
