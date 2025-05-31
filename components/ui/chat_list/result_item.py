from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

from components.ui.rounded_avatar import RoundedAvatar


class ResultItem(QtWidgets.QWidget):
    clicked = Signal(object)  # Signal when item is clicked

    def __init__(self, id, avatar, name, email):
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

        # Track hover state
        self.is_hovered = False

        # Set up the layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.avatar = RoundedAvatar(avatar)

        # Add avatar container to layout
        self.main_layout.addWidget(self.avatar)

        self.name_part = QtWidgets.QVBoxLayout()

        self.name_label = QtWidgets.QLabel(name)
        self.name_label.setStyleSheet(
            "font-weight: bold; background-color: transparent; border-color: transparent; color: white"
        )
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.name_label.setContentsMargins(10, 0, 0, 0)

        self.email_label = QtWidgets.QLabel(email)
        self.email_label.setContentsMargins(10, 0, 0, 15)
        self.email_label.setStyleSheet(
            "font-size: 14px; color: #ccc; background-color: transparent; border-color: transparent"
        )

        self.name_part.addWidget(self.name_label)
        self.name_part.addWidget(self.email_label)

        self.main_layout.addLayout(self.name_part)

    def update_background(self, color, active=False):
        """Update the background color using palette"""
        if active:
            self.setStyleSheet(f"background-color: {color}; border-radius: 0px")
        else:
            self.setStyleSheet(f"background-color: {color}; border-radius: 14px;")

    def enterEvent(self, event):
        """Handle mouse enter event"""
        self.is_hovered = True
        self.update_background(self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event"""
        self.is_hovered = False
        self.update_background(self.normal_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press event"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)  # Emit signal with self as argument
        super().mousePressEvent(event)

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


    # def contextMenuEvent(self, event):
    #     context_menu = QtWidgets.QMenu(self)
    #     context_menu.addAction(qta.icon("mdi.archive-arrow-down-outline", color="white"), "Archieve")
    #     context_menu.addAction(qta.icon("mdi.pin-outline", color="white"), "Pin")
    #     context_menu.addAction(qta.icon("mdi.volume-mute", color="white"), "Mute Notifications")
    #     context_menu.addAction(qta.icon("mdi.playlist-remove", color="white"), "Clear History")
    #     context_menu.addSeparator()

    #     button = QtWidgets.QPushButton(qta.icon("mdi.delete", color="red"), "Delete")

    #     delete_chat_action = QWidgetAction(context_menu)
    #     delete_chat_action.setDefaultWidget(button)
    #     context_menu.addAction(delete_chat_action)

    #     context_menu.setStyleSheet(context_menu_style)
    #     action = context_menu.exec_(event.globalPos())
