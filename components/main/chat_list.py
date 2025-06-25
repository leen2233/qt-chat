from typing import List

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal

from chat_types import ChatType, UserType
from components.ui.chat_list.chat_list_item import ChatListItem
from components.ui.chat_list.result_item import ResultItem
from components.ui.iconed_button import IconedButton
from utils import gv
from utils.time import format_timestamp


class ChatList(QtWidgets.QWidget):
    chat_selected = Signal(str)
    settings_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.active_item = None
        self.setMinimumWidth(250)
        self.setMaximumWidth(400)
        self.setObjectName("Sidebar")
        self.setContentsMargins(0, 0, 0, 0)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: #1f1e1d; border-radius: 14px")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.chats_layout = QtWidgets.QVBoxLayout(self)
        self.chats_layout.setContentsMargins(0, 0, 0, 0)
        self.chats_layout.setSpacing(0)
        self.chats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.search_chat_input = QtWidgets.QLineEdit()
        self.search_chat_input.setPlaceholderText("Search chats...")
        self.search_chat_input.setFixedHeight(60)
        self.search_chat_input.setTextMargins(10, 10, 10, 10)
        self.search_chat_input.setContentsMargins(10, 10, 10, 10)
        self.search_chat_input.setStyleSheet(
            "background-color: #30302e; border-radius: 10px; border: 0.5px solid grey; color: white"
        )
        self.search_chat_input.textChanged.connect(self.search_chat)

        self.connecting_label = QtWidgets.QLabel("Connecting...")
        self.connecting_label.setFixedHeight(60)
        self.connecting_label.setContentsMargins(10, 0, 0, 0)
        self.connecting_label.setStyleSheet(
            "background-color: #30302e; border-radius: 10px; color: white; border: 0.5px solid grey; margin: 10;"
        )
        self.connecting_label.setVisible(False)

        self.settings_button = IconedButton("mdi.cog-outline", "Settings", color="white", height=70, margin=5)
        self.settings_button.clicked.connect(lambda: self.settings_clicked.emit())

        self.main_layout.addWidget(self.search_chat_input)
        self.main_layout.addWidget(self.connecting_label)
        self.main_layout.addLayout(self.chats_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.settings_button)

        # Sidebar items
        self.chat_items = []
        self.result_items = []

    def load_chats(self, chats: List[ChatType]):
        self.clear_chat_layout()
        self.chat_items = []
        for chat in chats:
            updated_at_str = format_timestamp(chat.updated_at)
            item = ChatListItem(chat.id, chat.user.avatar, chat.user.display_name, chat.last_message, updated_at_str)
            item.clicked.connect(lambda item: self.handle_item_click(chat_item=item))
            self.chat_items.append(item)
            self.chats_layout.addWidget(self.chat_items[-1])

        if self.chat_items:
            self.set_active_item(self.chat_items[0])
            self.chat_selected.emit(str(self.chat_items[0].id))

    def handle_item_click(self, result_item = None, chat_item = None):
        item = result_item or chat_item
        if item:
            if gv.get("selected_chat") and gv.get("selected_chat", "").id == item.id:
                return
            self.set_active_item(item)
            self.chat_selected.emit(str(item.id))
            self.request_load_chat(result_item=result_item, chat_item=chat_item)


    def set_active_item_by_id(self, chat_id):
        for item in self.chat_items:
            if item.id == chat_id:
                self.set_active_item(item)
                break

    def set_active_item(self, active_item):
        if self.active_item:
            self.active_item.set_active(False)

        active_item.set_active(True)
        self.active_item = active_item

    def handle_connected(self):
        self.connecting_label.setVisible(False)
        self.search_chat_input.setVisible(True)

    def handle_disconnected(self):
        self.connecting_label.setVisible(True)
        self.search_chat_input.setVisible(False)

    def search_chat(self):
        query = self.search_chat_input.text()
        if query:
            gv.send_data({"action": "search_users", "data": {"q": query}})
        else:
            self.clear_chat_layout()
            for item in self.chat_items:
                self.chats_layout.addWidget(item)

    def clear_chat_layout(self):
        while self.chats_layout.count():
            item = self.chats_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def request_load_chat(self, result_item = None, chat_item = None):
        gv.send_data({"action": "get_messages", "data": {"user_id": result_item.id if result_item else None, "chat_id": chat_item.id if chat_item else None}})

    def load_search_results(self, results: List[UserType]):
        self.clear_chat_layout()
        for result in results:
            item = ResultItem(result.id, "", result.username, result.email)
            item.clicked.connect(lambda item: self.handle_item_click(result_item=item))
            self.result_items.append(item)
            self.chats_layout.addWidget(self.result_items[-1])
