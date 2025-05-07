from dataclasses import dataclass
from typing import List


@dataclass
class MessageType:
    text: str
    sender: str
    time: str


@dataclass
class ChatType:
    id: int
    avatar: str
    name: str
    last_message: str
    time: str
    messages: List[MessageType]
