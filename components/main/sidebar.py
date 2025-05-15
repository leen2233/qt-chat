from typing import Optional

import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from chat_types import ChatType
from components.ui.rounded_avatar import RoundedAvatar


class Divider(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(8)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("border-radius: 4px; background-color: #262624;")


class StatItem(QtWidgets.QWidget):
    def __init__(self, icon_name, text, on_click, color="white"):
        super().__init__()
        self.setFixedHeight(45)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.on_click = on_click

        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 10, 0)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setSpacing(25)

        self.hover_color = "#333333"
        self.normal_color = "transparent"

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(qta.icon(icon_name, color=color).pixmap(24, 24))
        self.text = QtWidgets.QLabel(text)
        self.text.setStyleSheet(f"color: {color}; font-size: 14px")
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)

    def update_background(self, color):
        """Update the background color using palette"""
        self.setStyleSheet(f"background-color: {color}; border-radius: 14px;")

    def enterEvent(self, event):
        """Handle mouse enter event"""
        self.update_background(self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event"""
        self.update_background(self.normal_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if self.on_click:
            self.on_click()


class Sidebar(QtWidgets.QWidget):
    sidebar_closed = QtCore.Signal(str)

    def __init__(self, chat: Optional[ChatType] = None, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.setObjectName("sidebar")
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("""#sidebar {background-color: #1f1e1d;border-radius: 14px;}""")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        info = QtWidgets.QLabel("User Info")
        info.setStyleSheet("font-size: 16px; color: white;")
        close_button = QtWidgets.QPushButton(qta.icon("mdi.close", color="white", size=(40, 40)), "")
        close_button.setIconSize(QtCore.QSize(30, 30))
        close_button.setStyleSheet("background: transparent; border: none;")
        close_button.clicked.connect(self.close)
        close_button.setCursor(QtCore.Qt.PointingHandCursor)
        header_layout.addWidget(info)
        header_layout.addStretch()
        header_layout.addWidget(close_button)

        user_info_layout = QtWidgets.QHBoxLayout()
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setAlignment(Qt.AlignLeft)
        user_info_layout.setSpacing(10)

        username_time_layout = QtWidgets.QVBoxLayout()
        username_time_layout.setContentsMargins(0, 0, 0, 0)
        username_time_layout.setAlignment(Qt.AlignLeft)
        username_time_layout.setSpacing(0)

        self.name = QtWidgets.QLabel(chat.name if chat else "")
        self.name.setStyleSheet("font-size: 20px; color: white;")
        self.time = QtWidgets.QLabel(chat.time if chat else "")
        self.time.setStyleSheet("font-size: 14px; color: grey;")
        username_time_layout.addWidget(self.name)
        username_time_layout.addWidget(self.time)

        self.avatar = RoundedAvatar(avatar_url=chat.avatar if chat else "", size=(60, 60))
        user_info_layout.addWidget(self.avatar)
        user_info_layout.addLayout(username_time_layout)

        phone_info_layout = QtWidgets.QHBoxLayout()
        phone_info_layout.setContentsMargins(10, 0, 0, 0)
        phone_info_layout.setAlignment(Qt.AlignLeft)
        phone_info_layout.setSpacing(20)
        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon("ri.contacts-book-2-fill", color="white").pixmap(40, 40))
        phone_number_description_layout = QtWidgets.QVBoxLayout()
        phone_number_description_layout.setSpacing(0)
        self.phone_number = QtWidgets.QLabel(chat.phone_number if chat else "")
        self.phone_number.setStyleSheet("font-size: 14px; color: white")
        self.phone_number.setCursor(QCursor(Qt.PointingHandCursor))
        description = QtWidgets.QLabel("Mobile")
        description.setStyleSheet("font-size: 10px; color: grey")
        phone_number_description_layout.addWidget(self.phone_number)
        phone_number_description_layout.addWidget(description)

        phone_info_layout.addWidget(icon)
        phone_info_layout.addLayout(phone_number_description_layout)

        username_info_layout = QtWidgets.QHBoxLayout()
        username_info_layout.setContentsMargins(10, 0, 0, 0)
        username_info_layout.setAlignment(Qt.AlignLeft)
        username_info_layout.setSpacing(20)
        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon("mdi6.information-outline", color="white").pixmap(40, 40))
        username_description_layout = QtWidgets.QVBoxLayout()
        username_description_layout.setSpacing(0)
        self.username = QtWidgets.QLabel("@" + chat.username if chat else "")
        self.username.setCursor(QCursor(Qt.PointingHandCursor))
        self.username.setStyleSheet("font-size: 14px; color: #c96442")
        description = QtWidgets.QLabel("Username")
        description.setStyleSheet("font-size: 10px; color: grey")
        username_description_layout.addWidget(self.username)
        username_description_layout.addWidget(description)

        username_info_layout.addWidget(icon)
        username_info_layout.addLayout(username_description_layout)

        self.stats = QtWidgets.QVBoxLayout()
        self.stats.setSpacing(2)
        if chat:
            if chat.stats.photos:
                self.stats.addWidget(
                    StatItem("mdi.google-photos", f"{chat.stats.photos} Photos", lambda: print("clicked"))
                )
            if chat.stats.videos:
                self.stats.addWidget(StatItem("fa5s.video", f"{chat.stats.videos} Videos", None))
            if chat.stats.files:
                self.stats.addWidget(StatItem("fa5.file-alt", f"{chat.stats.files} Files", None))
            if chat.stats.links:
                self.stats.addWidget(StatItem("fa5s.link", f"{chat.stats.links} Links", None))
            if chat.stats.voices:
                self.stats.addWidget(StatItem("ri.voiceprint-line", f"{chat.stats.voices} Voices", None))

        actions = QtWidgets.QVBoxLayout()
        actions.setSpacing(2)
        actions.addWidget(StatItem("mdi.share", "Share this contact", None))
        actions.addWidget(StatItem("mdi.square-edit-outline", "Edit this contact", None))
        actions.addWidget(StatItem("mdi.delete", "Delete this contact", None))
        actions.addWidget(StatItem("mdi.block-helper", "Block this user", None, color="red"))

        self.layout.addLayout(header_layout)
        self.layout.addLayout(user_info_layout)
        self.layout.addWidget(Divider())
        self.layout.addLayout(phone_info_layout)
        self.layout.addLayout(username_info_layout)
        self.layout.addWidget(Divider())
        self.layout.addLayout(self.stats)
        self.layout.addWidget(Divider())
        self.layout.addLayout(actions)

        self.setFixedWidth(0)
        QtCore.QTimer.singleShot(0, self.show_animation)

    def change_chat(self, chat: ChatType):
        self.avatar.change_source(chat.avatar)
        self.name.setText(chat.name)
        self.time.setText(chat.time)
        self.phone_number.setText(chat.phone_number)
        self.username.setText("@" + chat.username)
        while self.stats.count() > 0:
            item = self.stats.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if chat.stats.photos:
            self.stats.addWidget(StatItem("mdi.google-photos", f"{chat.stats.photos} Photos", lambda: print("clicked")))
        if chat.stats.videos:
            self.stats.addWidget(StatItem("fa5s.video", f"{chat.stats.videos} Videos", None))
        if chat.stats.files:
            self.stats.addWidget(StatItem("fa5.file-alt", f"{chat.stats.files} Files", None))
        if chat.stats.links:
            self.stats.addWidget(StatItem("fa5s.link", f"{chat.stats.links} Links", None))
        if chat.stats.voices:
            self.stats.addWidget(StatItem("ri.voiceprint-line", f"{chat.stats.voices} Voices", None))

    def close(self):
        self.sidebar_closed.emit("closed")
        self.hide_animation(self.deleteLater)

    def show_animation(self):
        self.animation = QtCore.QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)  # Animation duration in milliseconds
        self.animation.setStartValue(0)
        self.animation.setEndValue(300)  # Final width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)  # Smooth animation curve
        self.animation.start()

    def hide_animation(self, on_finished):
        self.animation = QtCore.QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(300)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        # Connect finished signal if callback provided
        if on_finished:
            self.animation.finished.connect(on_finished)

        self.animation.start()
