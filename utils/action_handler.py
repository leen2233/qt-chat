from chat_types import ChatType, MessageType, UserType


class ActionHandler:
    def __init__(self, data, window) -> None:
        self.window = window
        self.data = data

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
        messages = []
        for message_data in results:
            if message_data.get("reply_to"):
                message_data["reply_to"] = MessageType(**message_data["reply_to"])

            messages.append(MessageType(**message_data))

        self.window.fetched_messages.emit(messages)

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
            self.window.fetched_chats.emit(chats)
        except Exception as e:
            print(e, "error")

    def new_message(self):
        message = self.data.get("data", {}).get("message")
        if message.get("reply_to"):
            message["reply_to"] = MessageType(**message["reply_to"])
        message = MessageType(**message)
        self.window.new_message.emit(message)

    def status_change(self):
        user_id = self.data.get("data", {}).get("user_id")
        status = self.data.get("data", {}).get("status")
        last_seen = self.data.get("data", {}).get("last_seen")

        print(f"[[[  {user_id}  -  {status} -  {last_seen} ]]]")

        chats = self.window.chats
        for chat in chats:
            if chat.user and chat.user.id == user_id:
                chat.user.is_online = status == "online"
                chat.user.last_seen = last_seen

        self.window.chats = chats
        self.window.fetched_chats.emit(chats)
