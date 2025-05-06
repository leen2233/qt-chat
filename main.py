# Telegram-like chat app with dark theme and active chat highlighting
# Features: Sidebar with highlighted active chat, message display, input field, send button
# Dark theme only, no light theme

import sys

from PySide6 import QtWidgets

from components.chatbox import ChatBox
from components.sidebar import Sidebar
from data import CHAT_LIST


class ChatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Main widget and layout
        self.setWindowTitle("Telegram-like App")
        self.setMouseTracking(True)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow{ background-color: #262624; color: #ffffff; }
        """)

        # Sidebar (chat list)
        self.sidebar = Sidebar()
        self.sidebar.chat_selected.connect(self.chat_selected)

        # Main chat area
        self.chat_area = ChatBox()

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.chat_area)

        # Window settings
        self.resize(1000, 600)

        self.sidebar.load_chats(CHAT_LIST)

    def chat_selected(self, chat_id):
        chat_id = int(chat_id)
        for chat in CHAT_LIST:
            if chat.id == chat_id:
                self.chat_area.load_messages(chat.messages)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
