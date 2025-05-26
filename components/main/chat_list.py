from typing import List

import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from qtpy.QtWidgets import QWidgetAction

from chat_types import ChatType
from components.ui.iconed_button import IconedButton
from components.ui.rounded_avatar import RoundedAvatar
from styles import context_menu_style


class ChatItem(QtWidgets.QWidget):
    clicked = Signal(object)  # Signal when item is clicked

    def __init__(self, id, avatar, name, last_message, time):
        super().__init__()
        self.id = id
        self.setFixedHeight(70)
        self.setObjectName("chat-list-item")
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)

        # Create color objects for different states
        self.normal_color = "#1f1e1d"
        self.hover_color = "#333333"
        self.active_color = "#262624"

        self.setStyleSheet(f"background-color: {self.normal_color}; border-radius: 14px;")

        # Track hover and active states
        self.is_hovered = False
        self.is_active = False

        # Set up the layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.avatar = RoundedAvatar(avatar)

        # Add avatar container to layout
        self.main_layout.addWidget(self.avatar)

        self.name_part = QtWidgets.QVBoxLayout()

        self.name_time_part = QtWidgets.QHBoxLayout()
        self.name_time_part.setContentsMargins(0, 15, 0, 0)
        self.name_time_part.setSpacing(0)
        self.name_time_part.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.name_label = QtWidgets.QLabel(name)
        self.name_label.setStyleSheet(
            "font-weight: bold; background-color: transparent; border-color: transparent; color: white"
        )
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.name_label.setContentsMargins(10, 0, 0, 0)

        self.time_label = QtWidgets.QLabel(time)
        self.time_label.setStyleSheet(
            "font-size: 12px; color: #888; background-color: transparent; border-color: transparent"
        )

        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setContentsMargins(10, 0, 10, 0)

        self.name_time_part.addWidget(self.name_label)
        self.name_time_part.addWidget(self.time_label)

        self.last_message_label = QtWidgets.QLabel(last_message)
        self.last_message_label.setContentsMargins(10, 0, 0, 15)
        self.last_message_label.setStyleSheet(
            "font-size: 14px; color: #ccc; background-color: transparent; border-color: transparent"
        )

        self.name_part.addLayout(self.name_time_part)
        self.name_part.addWidget(self.last_message_label)

        self.main_layout.addLayout(self.name_part)

    def update_background(self, color, active=False):
        """Update the background color using palette"""
        if active:
            self.setStyleSheet(f"background-color: {color}; border-radius: 0px")
        else:
            self.setStyleSheet(f"background-color: {color}; border-radius: 14px;")

    def enterEvent(self, event):
        """Handle mouse enter event"""
        if not self.is_active:  # Only change color if not active
            self.is_hovered = True
            self.update_background(self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event"""
        if not self.is_active:  # Only change color if not active
            self.is_hovered = False
            self.update_background(self.normal_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press event"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)  # Emit signal with self as argument
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        context_menu = QtWidgets.QMenu(self)
        context_menu.addAction(qta.icon("mdi.archive-arrow-down-outline", color="white"), "Archieve")
        context_menu.addAction(qta.icon("mdi.pin-outline", color="white"), "Pin")
        context_menu.addAction(qta.icon("mdi.volume-mute", color="white"), "Mute Notifications")
        context_menu.addAction(qta.icon("mdi.playlist-remove", color="white"), "Clear History")
        context_menu.addSeparator()

        button = QtWidgets.QPushButton(qta.icon("mdi.delete", color="red"), "Delete")

        delete_chat_action = QWidgetAction(context_menu)
        delete_chat_action.setDefaultWidget(button)
        context_menu.addAction(delete_chat_action)

        context_menu.setStyleSheet(context_menu_style)
        action = context_menu.exec_(event.globalPos())

    def set_active(self, active):
        """Set this item as active/inactive"""
        self.is_active = active
        if active:
            self.is_hovered = False
            self.update_background(self.active_color, active=True)
        else:
            if self.is_hovered:
                self.update_background(self.hover_color)
            else:
                self.update_background(self.normal_color)


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

        self.connecting_label = QtWidgets.QLabel("Connecting...")
        self.connecting_label.setFixedHeight(60)
        self.connecting_label.setContentsMargins(10, 0, 0, 0)
        self.connecting_label.setStyleSheet("background-color: #30302e; border-radius: 10px; color: white; border: 0.5px solid grey; margin: 10;")
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

    def load_chats(self, chats: List[ChatType]):
        self.chat_items = []
        for chat in chats:
            item = ChatItem(chat.id, chat.avatar, chat.name, chat.last_message, chat.time)
            item.clicked.connect(self.handle_item_click)
            self.chat_items.append(item)
            self.chats_layout.addWidget(self.chat_items[-1])

        if self.chat_items:
            self.set_active_item(self.chat_items[0])
            self.chat_selected.emit(str(self.chat_items[0].id))

    def handle_item_click(self, item):
        self.set_active_item(item)
        self.chat_selected.emit(str(item.id))

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
