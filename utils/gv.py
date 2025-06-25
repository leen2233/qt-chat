from typing import Optional

from lib.conn import Conn

data = {}
_conn: Optional[Conn] = None

def set(key, value):
    global data
    data[key] = value

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
