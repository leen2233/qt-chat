from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MessageType:
    text: str
    sender: str
    time: str


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
