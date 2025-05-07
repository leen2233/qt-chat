from typing import List

import qtawesome as qta
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from qtpy.QtCore import QSize

from chat_types import MessageType

from .message import Message
from .typing_indicator import TypingIndicator


class ChatBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { background-color: #262624; color: #ffffff; }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

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
