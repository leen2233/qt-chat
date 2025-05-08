from typing import List

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal

from chat_types import ChatType
from components.rounded_avatar import RoundedAvatar


class SidebarItem(QtWidgets.QWidget):
    clicked = Signal(object)  # Signal when item is clicked

    def __init__(self, id, avatar, name, last_message, time):
        super().__init__()
        self.id = id
        self.setFixedHeight(70)

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

        # Create color objects for different states
        self.normal_color = QtGui.QColor("#1f1e1d")
        self.hover_color = QtGui.QColor("#grey")
        self.active_color = QtGui.QColor("#262624")

        # Set initial palette
        self.update_background(self.normal_color)

        # Track hover and active states
        self.is_hovered = False
        self.is_active = False

        # Set up the layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(0)

        self.avatar = RoundedAvatar(avatar)

        # Add avatar container to layout
        self.layout.addWidget(self.avatar)

        self.name_part = QtWidgets.QVBoxLayout()

        self.name_time_part = QtWidgets.QHBoxLayout()
        self.name_time_part.setContentsMargins(0, 15, 0, 0)
        self.name_time_part.setSpacing(0)
        self.name_time_part.setAlignment(Qt.AlignVCenter)

        self.name_label = QtWidgets.QLabel(name)
        self.name_label.setStyleSheet(
            "font-weight: bold; background-color: transparent; border-color: transparent; color: white"
        )
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.name_label.setContentsMargins(10, 0, 0, 0)

        self.time_label = QtWidgets.QLabel(time)
        self.time_label.setStyleSheet(
            "font-size: 12px; color: #888; background-color: transparent; border-color: transparent"
        )

        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
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

        self.layout.addLayout(self.name_part)

    def update_background(self, color):
        """Update the background color using palette"""
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)

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
        print("button cicked ", event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self)  # Emit signal with self as argument
        super().mousePressEvent(event)

    def set_active(self, active):
        """Set this item as active/inactive"""
        self.is_active = active
        if active:
            self.is_hovered = False
            self.update_background(self.active_color)
        else:
            if self.is_hovered:
                self.update_background(self.hover_color)
            else:
                self.update_background(self.normal_color)


class Sidebar(QtWidgets.QWidget):
    chat_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.active_item = None
        self.setFixedWidth(250)
        self.setObjectName("Sidebar")
        self.setContentsMargins(0, 0, 0, 0)

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#1f1e1d"))
        self.setPalette(palette)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.chats_layout = QtWidgets.QVBoxLayout(self)
        self.chats_layout.setContentsMargins(0, 0, 0, 0)
        self.chats_layout.setSpacing(0)
        self.chats_layout.setAlignment(Qt.AlignTop)

        self.search_chat_input = QtWidgets.QLineEdit()
        self.search_chat_input.setPlaceholderText("Search chats...")
        self.search_chat_input.setFixedHeight(60)
        self.search_chat_input.setTextMargins(10, 10, 10, 10)
        self.search_chat_input.setContentsMargins(10, 10, 10, 10)
        self.search_chat_input.setStyleSheet(
            "background-color: #30302e; border-radius: 20px; border: 0.5px solid grey; color: white"
        )

        self.layout.addWidget(self.search_chat_input)
        self.layout.addLayout(self.chats_layout)

        # Sidebar items
        self.sidebar_items = []

    def load_chats(self, chats: List[ChatType]):
        for chat in chats:
            item = SidebarItem(chat.id, chat.avatar, chat.name, chat.last_message, chat.time)
            item.clicked.connect(self.handle_item_click)
            self.sidebar_items.append(item)
            self.chats_layout.addWidget(self.sidebar_items[-1])

        if self.sidebar_items:
            # self.active_item()
            self.set_active_item(self.sidebar_items[0])
            self.chat_selected.emit(str(self.sidebar_items[0].id))

    def handle_item_click(self, item):
        self.set_active_item(item)
        self.chat_selected.emit(str(item.id))

    def set_active_item(self, active_item):
        if self.active_item:
            self.active_item.set_active(False)

        active_item.set_active(True)
        self.active_item = active_item
