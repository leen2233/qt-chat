import json
import socket
import time
from threading import Thread
from typing import Callable, Optional


class Conn:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(1.0)

        self.thread = None
        self._running = True

        self.connected_callback: Optional[Callable] = None
        self.disconnected_callback: Optional[Callable] = None

    def connect(self):
        self.server.connect((self.host, self.port))
        if self.connected_callback:
            self.connected_callback()

    def handle_disconnect(self):
        if self.disconnected_callback:
            self.disconnected_callback()

        print("trying again", self._running)
        if self._running:
            self.connect_with_retry()

    def loop(self):
        while self._running:
            try:
                message = self.server.recv(2048)
                message = self._decode(message)
                if message:
                    self.on_message(message)
                else:
                    self.handle_disconnect()
                    break
            except socket.timeout:  # Handle timeout
                if not self._running:  # Check _running after timeout
                    break
                continue
            except:
                self.handle_disconnect()
                break

    def close(self):
        self.server.close()

    def send_message(self, message: str):
        encoded = self._encode(message)
        self.server.send(encoded)

    def on_message(self, message: str):
        print("message got:", message)

    def send_data(self, body: dict):
        data = json.dumps(body)
        data = self._encode(data)
        self.server.send(data)

    def connect_with_retry(self):
        while self._running:
            try:
                self.connect()
                self._running = True
                self.loop()
                break
            except:
                print("Couldn't connect to server, retrying in 5 seconds...")
                time.sleep(5)

    def start(self):
        if self.disconnected_callback:
            self.disconnected_callback()
        self.thread = Thread(target=self.connect_with_retry)
        self.thread.start()

    def stop(self):
        self._running = False
        self.close()
        if self.thread:
            print(self._running, "eunning")
            self.thread.join()

    def _decode(self, text: bytes):
        return text.decode()

    def _encode(self, text: str):
        return text.encode()
