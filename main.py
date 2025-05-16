# Telegram-like chat app with dark theme and active chat highlighting
# Features: Sidebar with highlighted active chat, message display, input field, send button
# Dark theme only, no light theme

import sys

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt

from components.main.chat_list import ChatList
from components.main.chatbox import ChatBox
from components.main.sidebar import Sidebar
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
        self.main_layout.setSpacing(10)

        # Create and set up splitter
        self.splitter = QtWidgets.QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)  # Prevent collapsing sections
        self.splitter.setHandleWidth(1)

        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow{ background-color: #262624; color: #ffffff; }
        """)

        # chat list1
        self.chat_list = ChatList()
        self.chat_list.chat_selected.connect(self.chat_selected)

        # Main chat area
        self.chat_area = ChatBox()
        self.chat_area.sidebar_toggled_signal.connect(self.toggle_sidebar)

        self.splitter.addWidget(self.chat_list)
        self.splitter.addWidget(self.chat_area)
        self.splitter.setSizes([250, 750])
        self.main_layout.addWidget(self.splitter)

        self.chat_area.chat_input.setFocus(Qt.MouseFocusReason)
        # Window settings
        self.resize(1000, 600)

        self.setup_shortcuts()
        self.chat_list.load_chats(CHAT_LIST)

    def setup_shortcuts(self):
        ctrlTab = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Tab"), self)
        ctrlTab.activated.connect(self.select_next_chat)
        ctrlShiftTab = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+Tab"), self)
        ctrlShiftTab.activated.connect(self.select_previous_chat)

    def select_next_chat(self):
        for index, chat in enumerate(CHAT_LIST):
            if chat == self.selected_chat:
                if index == len(CHAT_LIST) - 1:
                    self.chat_selected(CHAT_LIST[0].id)
                else:
                    self.chat_selected(CHAT_LIST[index + 1].id)
                break

    def select_previous_chat(self):
        for index, chat in enumerate(CHAT_LIST):
            if chat == self.selected_chat:
                if index == 0:
                    self.chat_selected(CHAT_LIST[-1].id)
                else:
                    self.chat_selected(CHAT_LIST[index - 1].id)
                break

    def chat_selected(self, chat_id):
        chat_id = int(chat_id)
        for chat in CHAT_LIST:
            if chat.id == chat_id:
                self.selected_chat = chat
                self.chat_list.set_active_item_by_id(chat.id)
                self.chat_area.load_messages(chat.messages)
                self.chat_area.change_chat_user(chat)
                if self.sidebar_opened:
                    self.sidebar.change_chat(chat)

    def sidebar_closed(self, state):
        self.sidebar_opened = False
        self.chat_area.sidebar_toggle()

    def toggle_sidebar(self, state: bool):
        if state is True:
            self.sidebar = Sidebar(self.selected_chat)
            self.sidebar.sidebar_closed.connect(self.sidebar_closed)
            self.splitter.addWidget(self.sidebar)
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
