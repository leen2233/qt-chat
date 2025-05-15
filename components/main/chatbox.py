import random
from typing import List

import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QTimer, Signal
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QHBoxLayout

from chat_types import ChatType, MessageType
from components.ui.message import Message
from components.ui.rounded_avatar import RoundedAvatar
from components.ui.text_edit import TextEdit
from components.ui.typing_indicator import TypingIndicator
from data import CHAT_LIST
from styles import replying_to_label_style


class ChatBox(QtWidgets.QWidget):
    sidebar_toggled_signal = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sidebar_toggled = False
        self.chat = None
        self.reply_opened = False
        self.reply_to_message = None
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet("""
            QWidget { background-color: #262624; color: #ffffff; }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)

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
        self.search_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.search_button.setStyleSheet("background-color: transparent; border: none;")
        self.search_button.setIconSize(QSize(20, 20))

        self.call_button = QtWidgets.QPushButton(qta.icon("fa5s.phone-alt", color="white"), "")
        self.call_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.call_button.setStyleSheet("background-color: transparent; border: none;")
        self.call_button.setIconSize(QSize(20, 20))

        self.sidebar_button = QtWidgets.QPushButton(qta.icon("msc.layout-sidebar-right-off", color="white"), "")
        self.sidebar_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.sidebar_button.setStyleSheet("background-color: transparent; border: none;")
        self.sidebar_button.setIconSize(QSize(25, 25))
        self.sidebar_button.clicked.connect(self.sidebar_toggle)

        self.more_button = QtWidgets.QPushButton(qta.icon("mdi.dots-vertical", color="white"), "")
        self.more_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.more_button.setStyleSheet("background-color: transparent; border: none; padding-right: 15px")
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
        self.scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #30302e;
                width: 8px;
                border-radius: 3px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background: #404344;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: #606060;
            }
            """)
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
        self.input_part = QtWidgets.QVBoxLayout()

        self.reply_to_widget = QtWidgets.QWidget()
        self.reply_to_widget.setMaximumHeight(0)
        self.reply_to_widget.setContentsMargins(0, 0, 0, 0)
        self.reply_to_layout = QHBoxLayout(self.reply_to_widget)
        self.reply_to_layout.setContentsMargins(0, 0, 0, 0)
        self.reply_to_text = QtWidgets.QLabel("Hi there!")
        self.reply_to_text.setStyleSheet(replying_to_label_style)
        close_reply_button = QtWidgets.QPushButton(qta.icon("mdi.close", color="white", size=(40, 40)), "")
        close_reply_button.setIconSize(QSize(22, 22))
        close_reply_button.setStyleSheet("background-color: #4c4c4b; border: none; border-radius: 5px")
        close_reply_button.setFixedSize(35, 35)
        close_reply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_reply_button.clicked.connect(self.close_reply)
        self.reply_to_layout.addWidget(self.reply_to_text)
        self.reply_to_layout.addWidget(close_reply_button)
        # reply_to.setStyleSheet(
        #     "background-color: #30302e; border-radius: 10px; border: 0.5px solid grey; margin-bottom: 0px; text-align: left; padding-left: 20px; border-bottom: none"
        # )
        input_and_button_layout = QHBoxLayout()

        self.chat_input = TextEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.setMaximumHeight(150)
        self.chat_input.setMinimumHeight(50)
        self.chat_input.setFixedHeight(50)
        self.chat_input.textChanged.connect(self.adjust_input_height)
        self.chat_input.setStyleSheet("padding: 10px")
        self.chat_input.enterPressed.connect(self.send_my_message)

        self.chat_input.setViewportMargins(10, 10, 10, 10)
        self.chat_input.setStyleSheet("background-color: #30302e; border-radius: 10px; border: 0.5px solid grey")

        self.send_button = QtWidgets.QPushButton(qta.icon("fa6.paper-plane", color="white", size=(40, 40)), "")
        self.send_button.setIconSize(QSize(22, 22))
        self.send_button.setFixedSize(50, 50)  # Set a fixed size for the button
        self.send_button.setStyleSheet(
            "background-color: #c96442; color: white; border-radius: 10px; font-weight: bold;"
        )
        self.send_button.clicked.connect(self.send_my_message)

        input_and_button_layout.addWidget(self.chat_input)
        input_and_button_layout.addWidget(self.send_button)

        self.input_part.addWidget(self.reply_to_widget)
        self.input_part.addLayout(
            input_and_button_layout,
        )

        # Add components to main layout
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.scroll_area)
        self.layout.addLayout(self.input_part)

    def adjust_input_height(self):
        doc_height = self.chat_input.document().size().height()
        new_height = min(max(doc_height + 10, 50), 150)  # Adjust between min and max
        self.chat_input.setFixedHeight(new_height)

    def add_message(self, message_item: MessageType, next=None, previous=None):
        message = Message(message=message_item)
        message.reply_clicked.connect(self.open_reply)
        message.message_highlight.connect(self.highlight_message)
        self.messages_container.addWidget(message)
        QTimer.singleShot(50, self.scroll_to_bottom)

        return message

    def highlight_message(self, message_id: str):
        print("ID: ", message_id)
        for index in range(self.messages_container.count()):
            item = self.messages_container.itemAt(index)
            if item and item.widget() and item.widget().message_type.id == message_id:
                self.scroll_area.ensureWidgetVisible(item.widget())
                item.widget().highlight()
        self.chat_input.setFocus(Qt.MouseFocusReason)

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def show_typing_indicator(self):
        indicator = TypingIndicator()
        indicator.start()
        self.messages_container.insertWidget(self.messages_container.count() - 1, indicator)

    def send_my_message(self):
        text = self.chat_input.toPlainText()
        if text.strip():
            message_type = MessageType(
                id=random.randint(1, 1000), text=text, sender="me", time="now", reply_to=self.reply_to_message
            )
            self.add_message(message_type)
            if self.reply_opened:
                self.close_reply()
            if self.chat:
                for chat in CHAT_LIST:
                    if chat.id == self.chat.id:
                        chat.messages.append(message_type)
                        break
            self.chat_input.setText("")

    def load_messages(self, messages: List[MessageType]):
        for i in reversed(range(self.messages_container.count())):
            item = self.messages_container.itemAt(i)
            if item.widget():  # Check if item has a widget
                item.widget().deleteLater()
            self.messages_container.removeItem(item)
        for message in messages:
            self.add_message(message)

    def change_chat_user(self, chat: ChatType):
        self.avatar.change_source(chat.avatar)
        self.username.setText(chat.name)
        self.last_seen.setText(chat.time)
        self.chat = chat
        self.chat_input.setFocus(Qt.MouseFocusReason)

    def sidebar_toggle(self):
        self.sidebar_button.setIcon(
            qta.icon("msc.layout-sidebar-right-off", color="white")
            if self.sidebar_toggled
            else qta.icon("msc.layout-sidebar-right-off", color="#c96442")
        )
        self.sidebar_toggled = not self.sidebar_toggled
        self.sidebar_toggled_signal.emit(self.sidebar_toggled)
        self.chat_input.setFocus(Qt.MouseFocusReason)

    def close_reply(self):
        self.animation = QtCore.QPropertyAnimation(self.reply_to_widget, b"maximumHeight")
        self.animation.setDuration(200)  # Animation duration in milliseconds
        self.animation.setStartValue(35)
        self.animation.setEndValue(0)  # Final width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)  # Smooth animation curve
        self.animation.start()
        self.reply_opened = False
        self.reply_to_message = None

    def open_reply(self, message: MessageType):
        index = int(self.reply_to_text.width() / 5.8)
        self.reply_to_message = message
        self.reply_to_text.setText(message.text[:index])
        self.chat_input.setFocus(Qt.MouseFocusReason)
        if not self.reply_opened:
            self.animation = QtCore.QPropertyAnimation(self.reply_to_widget, b"maximumHeight")
            self.animation.setDuration(200)  # Animation duration in milliseconds
            self.animation.setStartValue(0)
            self.animation.setEndValue(35)  # Final width
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)  # Smooth animation curve
            self.animation.start()
            self.reply_opened = True
