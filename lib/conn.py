import asyncio
import json
from threading import Thread
from typing import Callable, Optional

import websockets


class Conn:
    def __init__(self, host: str, port: Optional[str], access_token: Optional[str] = None):
        if port:
            self.uri = f"ws://{host}:{port}/"
        else:
            self.uri = f"wss://{host}/"
        self.websocket = None
        self.access_token = access_token

        self.connected_callback: Optional[Callable] = None
        self.disconnected_callback: Optional[Callable] = None
        self.on_message_callback: Optional[Callable] = None

        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self._start_loop)
        self._running = True

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        while self._running:
            try:
                async with websockets.connect(self.uri) as websocket:
                    self.websocket = websocket
                    if self.connected_callback:
                        self.connected_callback()

                    if self.access_token:
                        self.send_data({
                            "action": "authenticate",
                            "data": {"access_token": self.access_token}
                        })

                    await self.listen()
            except Exception as e:
                print("Disconnected, retrying in 5 seconds...", e)
                if self.disconnected_callback:
                    self.disconnected_callback()
                await asyncio.sleep(5)

    async def listen(self):
        try:
            async for message in self.websocket:
                self.on_message(message)
        except Exception as e:
            print("Error in listen:", e)

    def on_message(self, message: str):
        try:
            data = json.loads(message)
            if self.on_message_callback:
                self.on_message_callback(data)
        except json.JSONDecodeError:
            print("invalid json")

    async def _send(self, message: str):
        if self.websocket:
            await self.websocket.send(message)

    def send_data(self, body: dict):
        message = json.dumps(body)
        self.loop.call_soon_threadsafe(lambda: asyncio.create_task(self._send(message)))

    def start(self):
        self.thread.start()

    def stop(self):
        self._running = False
        if self.websocket:
            self.loop.call_soon_threadsafe(lambda: asyncio.create_task(self.websocket.close()))
        self.thread.join()

    def _decode(self, text: bytes):
        return text.decode()

    def _encode(self, text: str):
        return text.encode()
