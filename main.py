# Telegram-like chat app with dark theme and active chat highlighting
# Features: Sidebar with highlighted active chat, message display, input field, send button
# Dark theme only, no light theme

import sys

from PySide6 import QtWidgets

from components.chat_list import ChatList
from components.chatbox import ChatBox
from components.sidebar import Sidebar
from data import CHAT_LIST


class ChatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_chat = None
        self.sidebar_opened = False

        # Main widget and layout
        self.setWindowTitle("Telegram-like App")
        self.setMouseTracking(True)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow{ background-color: #262624; color: #ffffff; }
        """)

        # chat list
        self.chat_list = ChatList()
        self.chat_list.chat_selected.connect(self.chat_selected)

        # Main chat area
        self.chat_area = ChatBox()
        self.chat_area.sidebar_toggled_signal.connect(self.toggle_sidebar)

        self.main_layout.addWidget(self.chat_list)
        self.main_layout.addWidget(self.chat_area)
        # Window settings
        self.resize(1000, 600)

        self.chat_list.load_chats(CHAT_LIST)

    def chat_selected(self, chat_id):
        chat_id = int(chat_id)
        for chat in CHAT_LIST:
            if chat.id == chat_id:
                self.selected_chat = chat
                self.chat_area.load_messages(chat.messages)
                self.chat_area.change_chat_user(chat)
                if self.sidebar_opened:
                    print("PRint sidebar opened")
                    self.sidebar.change_chat(chat)

    def sidebar_closed(self, state):
        self.sidebar_opened = False
        self.chat_area.sidebar_toggle()

    def toggle_sidebar(self, state: bool):
        if state is True:
            self.sidebar = Sidebar(self.selected_chat)
            self.sidebar.sidebar_closed.connect(self.sidebar_closed)
            self.main_layout.addWidget(self.sidebar)
            self.sidebar_opened = True
        else:
            self.sidebar_opened = False

            def remove_sidebar():
                self.sidebar.deleteLater()

            self.sidebar.hide_animation(on_finished=remove_sidebar)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
