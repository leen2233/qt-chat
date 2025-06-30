import json
import os
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QObject, Signal

from chat_types import ChatType, MessageType, UserType
from lib.conn import Conn

data = {}
data_loaded = False
_conn: Optional[Conn] = None
instance = 0
DATA_BLACKLIST = ["is_authenticated"]

class SignalManager(QObject):
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
    elif key == "is_authenticated" and value:
        if data_loaded and data.get("last_updated_time"):
            data_to_send = {'action': "get_updates", "data": {"last_time": data.get("last_updated_time")}}
        else:
            data_to_send = {'action': "get_chats", "data": {}}
        send_data(data_to_send)
        return

    save_data(data)


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


def save_data(data: dict):
    with open(f"data{instance}.json", "w") as f:
        data_to_save = deepcopy(data)
        for key, value in data.items():
            if key in DATA_BLACKLIST:
                data_to_save.pop(key)

        data_to_save["chats"] = [asdict(item) for item in data_to_save.get("chats", [])]
        data_to_save["selected_chat"] = asdict(data_to_save["selected_chat"]) if data_to_save.get("selected_chat") else {}
        data_to_save["waiting_messages"] = [asdict(item) for item in data_to_save.get("waiting_messages", [])]
        for key, value in data_to_save.items():
            if key.startswith("chat_messages_"):
                data_to_save[key]["messages"] = [asdict(item) for item in value.get('messages', [])]
        data_to_save["last_updated_time"] = datetime.now().timestamp()

        f.write(json.dumps(data_to_save))


def load_data():
    global data, data_loaded

    if not os.path.exists(f"data{instance}.json"):
        with open(f"data{instance}.json", "w") as f:
            f.write("{}")

    with open(f"data{instance}.json", "r") as file:
        try:
            loaded_data = json.load(file)
        except Exception as e:
            print(e, "error when recovering")
            loaded_data = {}
            return

    loaded_data["chats"] = [
        ChatType(**{k: v for k, v in item.items() if k != "user"}, user=UserType(**item.get("user", {})))
        for item in loaded_data.get("chats", [])
    ]
    if loaded_data.get("selected_chat"):
        user_data = loaded_data["selected_chat"].pop("user", {})
        loaded_data["selected_chat"] = ChatType(**loaded_data["selected_chat"], user=UserType(**user_data))
    if loaded_data.get("waiting_messages"):
        loaded_data["waiting_messages"] = [MessageType(**item) for item in loaded_data.get("waiting_messages", [])]
    for key, value in loaded_data.items():
        if key.startswith("chat_messages_"):
            loaded_data[key]["messages"] = [MessageType(**item) for item in value.get('messages', [])]

    for key, value in loaded_data.items():
        if value:
            data[key] = value
    data_loaded = True

    signal_manager.chats_changed.emit(data.get("chats", []))
    if data.get("selected_chat"):
        signal_manager.selected_chat_changed.emit(data.get("selected_chat"))

    for key, value in loaded_data.items():
        if key.startswith("chat_messages_") and data["selected_chat"].id and data["selected_chat"].id == key.split("chat_messages_")[1]:
            signal_manager.messages_changed.emit(data[key])


def set_instance(instance_number):
    global instance
    instance = instance_number
