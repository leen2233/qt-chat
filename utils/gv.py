from typing import Optional

from PySide6.QtCore import QObject, Signal

from chat_types import ChatType
from lib.conn import Conn

data = {}
_conn: Optional[Conn] = None


class SignalManager(QObject):
    # Global signals
    chats_changed = Signal(list)
    selected_chat_changed = Signal(ChatType)
    messages_changed = Signal(dict)

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.__initialized = True

signal_manager = SignalManager()


def set(key, value):
    global data
    data[key] = value

    if key == "chats":
        signal_manager.chats_changed.emit(value)
    elif key == "selected_chat":
        signal_manager.selected_chat_changed.emit(value)
    elif key.startswith("chat_messages_"):
        if data["selected_chat"].id and data["selected_chat"].id == key.split("chat_messages_")[1]:
            signal_manager.messages_changed.emit(value)

def get(key, default=None):
    return data.get(key, default)


def set_conn(conn_object):
    global _conn
    _conn = conn_object

def get_conn():
    return _conn

def send_data(data: dict):
    if _conn:
        _conn.send_data(data)
    else:
        print("connection not ready yet")



# def add_callback(key, callback: Callable):
#     global callbacks

#     if key in callbacks:
#         callbacks[key].append(callback)
#     else:
#         callbacks[key] = [callback]
