from typing import Dict

from chat_types import ChatType, MessageType, UserType
from utils import gv


class ActionHandler:
    def __init__(self, data, window) -> None:
        self.window = window
        self.data = data
        print("\n[RECV]", self.data, end="\n")

    def handle(self):
        if hasattr(self, self.data.get("action")):
            getattr(self, self.data.get("action"))()
        else:
            print("[unknown action], data: ", self.data)

    def authenticate(self):
        if self.data.get("success") is False:
            data = {"action": "refresh_access_token", "data": {"refresh_token": self.window.refresh_token}}
            self.window.conn.send_data(data)
        self.window.on_authenticate(self.data)

    def refresh_access_token(self):
        if self.data.get("success") is False or not self.data.get("data", {}).get("access_token"):
            self.window.on_logout.emit()
        else:
            self.access_token = self.data.get("data", {}).get("access_token")
            self.window.settings.setValue("access_token", self.access_token)
            data = {"action": "authenticate", "data": {"access_token": self.access_token}}
            self.window.conn.send_data(data)

    def search_users(self):
        results = self.data.get("data", {}).get("results")
        results = [UserType(**user) for user in results]
        self.window.search_results_received.emit(results)

    def get_messages(self):
        results = self.data.get("data", {}).get("results")
        has_more = self.data.get("data", {}).get("has_more")
        chat_id = self.data.get("data", {}).get("chat").get("id")
        messages = []
        for message_data in results:
            if message_data.get("reply_to"):
                message_data["reply_to"] = MessageType(**message_data["reply_to"], is_mine=message_data["reply_to"]["sender"] == gv.get("user", {}).get("id"))

            messages.append(MessageType(**message_data, is_mine=message_data["sender"] == gv.get("user", {}).get("id")))

        existing_messages = gv.get(f"chat_messages_{chat_id}", {}).get("messages")
        if existing_messages:
            messages.extend(existing_messages)

        gv.set(f"chat_messages_{chat_id}", {"messages": messages, "has_more": has_more})

        # self.window.fetched_messages.emit(messages, has_more, not(is_same_chat))

    def get_chats(self):
        try:
            results = self.data.get("data", {}).get("results")
            chats = []
            for chat in results:
                user = chat.get("user")
                user = UserType(**user)
                chat_obj = ChatType(
                    user=user,
                    id=chat.get("id"),
                    last_message=chat.get("last_message"),
                    updated_at=chat.get("updated_at"),
                )
                chats.append(chat_obj)
            self.window.chats = chats
            gv.set("chats", chats)
            # self.window.fetched_chats.emit(chats)
        except Exception as e:
            print(e, "error")

    def new_message(self):
        message = self.data.get("data", {}).get("message")
        chat_id = self.data.get("data", {}).get("message", {}).get("chat_id")
        local_id = self.data.get("data", {}).get("local_id")
        if message.get("reply_to"):
            message["reply_to"] = MessageType(**message["reply_to"], is_mine=message["reply_to"]["sender"] == gv.get("user", {}).get("id"))

        if local_id:
            waiting_messages = gv.get("waiting_messages", [])
            for m in waiting_messages:
                if m.id == local_id:
                    waiting_messages.remove(m)
            gv.set("waiting_messages", waiting_messages)

        messages = gv.get(f"chat_messages_{chat_id}", [])

        if local_id:
            for m in messages.get("messages", []):
                if m.id == local_id:
                    m.id = message.get("id")
                    m.status = message.get("status")
                    m.local_id = local_id
        else:
            message = MessageType(**message, is_mine=message["reply_to"]["sender"] == gv.get("user", {}).get("id"))
            messages.get("messages", []).append(message)
        gv.set(f"chat_messages_{chat_id}", messages)

    def delete_message(self):
        if not self.data.get("success"):
            print("[DELETE MESSAGE FAILED]", self.data.get("data"))

        message_id = self.data.get("data", {}).get("message_id")
        chat_id = self.data.get("data", {}).get("chat_id")

        messages = gv.get(f"chat_messages_{chat_id}", {})
        for message in messages.get("messages", []):
            if message.id == message_id:
                messages.get("messages", []).remove(message)

        gv.set(f"chat_messages_{chat_id}", messages)

    def edit_message(self):
        if not self.data.get("success"):
            print("[EDIT MESSAGE FAILED]", self.data.get("data"))

        message_id = self.data.get("data", {}).get("message_id")
        text = self.data.get("data", {}).get("text")
        chat_id = self.data.get("data", {}).get("chat_id")

        messages = gv.get(f"chat_messages_{chat_id}", {})
        for message in messages.get("messages", []):
            if message.id == message_id:
                message.text = text

        gv.set(f"chat_messages_{chat_id}", messages)


    def status_change(self):
        user_id = self.data.get("data", {}).get("user_id")
        status = self.data.get("data", {}).get("status")
        last_seen = self.data.get("data", {}).get("last_seen")

        chats = gv.get("chats", [])
        for chat in chats:
            if chat.user and chat.user.id == user_id:
                chat.user.is_online = status == "online"
                chat.user.last_seen = last_seen

        self.window.chats = chats
        gv.set("chats", chats)
        # self.window.fetched_chats.emit(chats)

    def read_message(self):
        message_ids = self.data.get("data", {}).get("message_ids")
        chat_id = self.data.get("data", {}).get("chat_id")

        messages = gv.get(f"chat_messages_{chat_id}", {})
        for message in messages.get("messages", []):
            if message.id in message_ids:
                message.status = "read"

        gv.set(f"chat_messages_{chat_id}", messages)

    def get_updates(self):
        updates = self.data.get("data", {}).get("updates", [])
        updates_grouped = group_updates(updates)

        for chat_id, updates in updates_grouped.items():
            messages = gv.get(f"chat_messages_{chat_id}", {})

            for update in updates:
                if update.get("type") == "new_message":
                    messages.get("messages").append(update.get("message"))
                elif update.get("type") == "delete_message":
                    for message in messages.get("messages"):
                        if message.id == update.get("message_id"):
                            messages.get("messages").remove(message)
                elif update.get("type") == "edit_message":
                    for message in messages.get("messages"):
                        if message.id == update.get('message_id'):
                            message.text = update.get("text")
                elif update.get("type") == "read_message":
                    for message in messages.get("messages"):
                        if message.id in update.get('message_ids'):
                            message.status = "read"

            gv.set(f"chat_messages_{chat_id}", messages)


def group_updates(updates: list) -> Dict[str, list]:
    updates_grouped = {}
    for update in updates:
        if update.get("type") == "new_message":
            new_message = MessageType(**update.get("body").get("message"))
            if new_message.chat_id not in updates_grouped:
                updates_grouped[new_message.chat_id] = []

            updates_grouped[new_message.chat_id].append({"type": "new_message", "message": new_message})

        elif update.get("type") == "delete_message":
            chat_id = update.get("body", {}).get("chat_id")
            if chat_id not in updates_grouped:
                updates_grouped[chat_id] = []

            updates_grouped[chat_id].append({
                "type": "delete_message",
                "message_id": update.get("body", {}).get("message_id")
            })

        elif update.get("type") == "edit_message":
            chat_id = update.get("body", {}).get("chat_id")
            if chat_id not in updates_grouped:
                updates_grouped[chat_id] = []
            updates_grouped[chat_id].append({
                "type": "edit_message",
                "message_id": update.get("body", {}).get("message_id"),
                "text": update.get("body", {}).get("text")
            })

        elif update.get("type") == "read_message":
            chat_id = update.get("body", {}).get("chat_id")
            if chat_id not in updates_grouped:
                updates_grouped[chat_id] = []

            updates_grouped[chat_id].append({
                "type": "read_message",
                "message_ids": update.get("body", {}).get("message_ids")
            })

    return updates_grouped
