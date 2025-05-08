import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from qtpy.QtCore import Qt

from chat_types import ChatType
from components.rounded_avatar import RoundedAvatar


class Sidebar(QtWidgets.QWidget):
    sidebar_closed = QtCore.Signal(str)

    def __init__(self, chat: ChatType, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self.setObjectName("sidebar")
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("""#sidebar {background-color: #1f1e1d;border-radius: 14px;}""")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        info = QtWidgets.QLabel("User Info")
        info.setStyleSheet("font-size: 16px; color: white;")
        close_button = QtWidgets.QPushButton(qta.icon("mdi.close", color="white", size=(40, 40)), "")
        close_button.setIconSize(QtCore.QSize(30, 30))
        close_button.setStyleSheet("background: transparent; border: none;")
        close_button.clicked.connect(self.close)
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
        username_time_layout.setSpacing(5)

        self.name = QtWidgets.QLabel(chat.name if chat else "")
        self.name.setStyleSheet("font-size: 20px; color: white;")
        self.time = QtWidgets.QLabel(chat.time if chat else "")
        self.time.setStyleSheet("font-size: 14px; color: grey;")
        username_time_layout.addWidget(self.name)
        username_time_layout.addWidget(self.time)

        self.avatar = RoundedAvatar(avatar_url=chat.avatar if chat else "", size=(60, 60))
        user_info_layout.addWidget(self.avatar)
        user_info_layout.addLayout(username_time_layout)

        self.layout.addLayout(header_layout)
        self.layout.addLayout(user_info_layout)

        self.setFixedWidth(0)
        QtCore.QTimer.singleShot(0, self.show_animation)

    def change_chat(self, chat: ChatType):
        self.avatar.change_source(chat.avatar)
        self.name.setText(chat.name)
        self.time.setText(chat.time)

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
