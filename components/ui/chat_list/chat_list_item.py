import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from qtpy.QtWidgets import QWidgetAction

from components.ui.rounded_avatar import RoundedAvatar
from styles import context_menu_style
from utils.time import format_timestamp


class ChatListItem(QtWidgets.QWidget):
    clicked = Signal(object)  # Signal when item is clicked

    def __init__(self, chat):
        super().__init__()
        self.chat = chat
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

        self.avatar = RoundedAvatar(self.chat.user.avatar, name=self.chat.user.display_name)

        # Add avatar container to layout
        self.main_layout.addWidget(self.avatar)

        self.name_part = QtWidgets.QVBoxLayout()

        self.name_time_part = QtWidgets.QHBoxLayout()
        self.name_time_part.setContentsMargins(0, 15, 0, 0)
        self.name_time_part.setSpacing(0)
        self.name_time_part.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.name_label = QtWidgets.QLabel(self.chat.user.display_name)
        self.name_label.setStyleSheet(
            "font-weight: bold; background-color: transparent; border-color: transparent; color: white"
        )
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.name_label.setContentsMargins(10, 0, 0, 0)

        self.time_label = QtWidgets.QLabel(format_timestamp(chat.updated_at))
        self.time_label.setStyleSheet(
            "font-size: 12px; color: #888; background-color: transparent; border-color: transparent"
        )

        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setContentsMargins(10, 0, 10, 0)

        self.name_time_part.addWidget(self.name_label)
        self.name_time_part.addWidget(self.time_label)

        self.last_message_label = QtWidgets.QLabel(self.chat.last_message)
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
