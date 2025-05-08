from typing import List

import qtawesome as qta
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from qtpy.QtCore import QSize

from chat_types import ChatType, MessageType
from components.rounded_avatar import RoundedAvatar

from .message import Message
from .typing_indicator import TypingIndicator


class ChatBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sidebar_toggled = False
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""
            QWidget { background-color: #262624; color: #ffffff; }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 10, 10)

        self.header_widget = QtWidgets.QWidget()
        self.header_widget.setFixedHeight(60)
        self.header_widget.setStyleSheet("background-color: #1f1e1d; border-radius: 14px")
        self.header_layout = QtWidgets.QHBoxLayout(self.header_widget)
        self.header_layout.setAlignment(Qt.AlignJustify)
        self.header_layout.setContentsMargins(10, 0, 0, 0)

        self.avatar = RoundedAvatar(
            "https://fastly.picsum.photos/id/354/200/200.jpg?hmac=ykMwenrB5tcaT_UHlYwh2ZzAZ4Km48YOmwJTFCiodJ4"
        )

        self.username = QtWidgets.QLabel("John Doe")
        self.username.setStyleSheet("font-size: 16px")
        self.username.setContentsMargins(0, 0, 0, 0)
        self.last_seen = QtWidgets.QLabel("Last seen: 10:30 AM")
        self.last_seen.setStyleSheet("font-size: 14px; color: grey")
        self.last_seen.setContentsMargins(0, 0, 0, 0)

        self.username_last_seen_layout = QtWidgets.QVBoxLayout()
        self.username_last_seen_layout.setSpacing(0)
        self.username_last_seen_layout.setContentsMargins(0, 0, 0, 0)
        self.username_last_seen_layout.setAlignment(Qt.AlignVCenter)
        self.username_last_seen_layout.addWidget(self.username)
        self.username_last_seen_layout.addWidget(self.last_seen)

        self.search_button = QtWidgets.QPushButton(qta.icon("fa5s.search", color="white"), "")
        self.search_button.setStyleSheet("background-color: transparent; border: none;")
        self.search_button.setIconSize(QSize(20, 20))

        self.call_button = QtWidgets.QPushButton(qta.icon("fa5s.phone-alt", color="white"), "")
        self.call_button.setStyleSheet("background-color: transparent; border: none;")
        self.call_button.setIconSize(QSize(20, 20))

        self.sidebar_button = QtWidgets.QPushButton(qta.icon("msc.layout-sidebar-right-off", color="white"), "")
        self.sidebar_button.setStyleSheet("background-color: transparent; border: none;")
        self.sidebar_button.setIconSize(QSize(25, 25))
        self.sidebar_button.clicked.connect(self.sidebar_toogle)

        self.more_button = QtWidgets.QPushButton(qta.icon("mdi.dots-vertical", color="white"), "")
        self.more_button.setStyleSheet("background-color: transparent; border: none;")
        self.more_button.setIconSize(QSize(25, 25))

        self.header_layout.addWidget(self.avatar)
        self.header_layout.addLayout(self.username_last_seen_layout)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.search_button)
        self.header_layout.addWidget(self.call_button)
        self.header_layout.addWidget(self.sidebar_button)
        self.header_layout.addWidget(self.more_button)

        # Scroll area for messages
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        # Container for messages
        self.messages_widget = QtWidgets.QWidget()
        self.messages_container = QtWidgets.QVBoxLayout(self.messages_widget)
        self.messages_container.setAlignment(Qt.AlignBottom)
        self.messages_container.setContentsMargins(0, 0, 0, 20)
        self.messages_container.addStretch()

        self.scroll_area.setWidget(self.messages_widget)

        # Input area
        self.input_part = QtWidgets.QHBoxLayout()

        self.chat_input = QtWidgets.QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.setFixedHeight(50)
        self.chat_input.setTextMargins(10, 10, 10, 10)
        self.chat_input.setStyleSheet("background-color: #30302e; border-radius: 10px; border: 0.5px solid grey")
        self.chat_input.returnPressed.connect(self.send_my_message)

        self.send_button = QtWidgets.QPushButton(qta.icon("fa6.paper-plane", color="white", size=(40, 40)), "")
        self.send_button.setIconSize(QSize(22, 22))
        self.send_button.setFixedSize(50, 50)  # Set a fixed size for the button
        self.send_button.setStyleSheet(
            "background-color: #c96442; color: white; border-radius: 10px; font-weight: bold;"
        )
        self.send_button.clicked.connect(self.send_my_message)

        self.input_part.addWidget(self.chat_input)
        self.input_part.addWidget(self.send_button)

        # Add components to main layout
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.scroll_area)
        self.layout.addLayout(self.input_part)

    def add_message(self, text: str, author: str, message_time: str):
        is_mine = author == "me"
        message = Message(text, author, message_time, is_mine)
        self.messages_container.insertWidget(self.messages_container.count() - 1, message)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

        return message

    def show_typing_indicator(self):
        indicator = TypingIndicator()
        indicator.start()
        self.messages_container.insertWidget(self.messages_container.count() - 1, indicator)

    def send_my_message(self):
        text = self.chat_input.text()
        if text.strip():
            self.add_message(text, "me", "now")
            self.chat_input.setText("")
            self.show_typing_indicator()

    def load_messages(self, messages: List[MessageType]):
        for i in reversed(range(self.messages_container.count())):
            item = self.messages_container.itemAt(i)
            if item.widget():  # Check if item has a widget
                item.widget().deleteLater()
            self.messages_container.removeItem(item)
        for message in messages:
            self.add_message(message.text, message.sender, message.time)

    def change_chat_user(self, chat: ChatType):
        self.avatar.change_source(chat.avatar)
        self.username.setText(chat.name)
        self.last_seen.setText(chat.time)

    def sidebar_toogle(self):
        self.sidebar_button.setIcon(
            qta.icon("msc.layout-sidebar-right-off", color="white")
            if self.sidebar_toggled
            else qta.icon("msc.layout-sidebar-right-off", color="#c96442")
        )
        self.sidebar_toggled = not self.sidebar_toggled
