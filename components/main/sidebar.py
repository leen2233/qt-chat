
import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from chat_types import ChatType
from components.ui.iconed_button import IconedButton
from components.ui.rounded_avatar import RoundedAvatar
from styles import Colors
from utils import gv
from utils.time import format_timestamp


class Divider(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(8)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("border-radius: 4px; background-color: #262624;")


class Sidebar(QtWidgets.QWidget):
    sidebar_closed = QtCore.Signal(str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.setObjectName("sidebar")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("""#sidebar {background-color: #1f1e1d;border-radius: 14px;}""")
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        gv.signal_manager.selected_chat_changed.connect(self.change_chat)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        info = QtWidgets.QLabel("User Info")
        info.setStyleSheet("font-size: 16px; color: white;")
        close_button = QtWidgets.QPushButton(qta.icon("mdi.close", color="white", size=(40, 40)), "")
        close_button.setIconSize(QtCore.QSize(30, 30))
        close_button.setStyleSheet("background: transparent; border: none;")
        close_button.clicked.connect(self.close)
        close_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(info)
        header_layout.addStretch()
        header_layout.addWidget(close_button)

        user_info_layout = QtWidgets.QHBoxLayout()
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        user_info_layout.setSpacing(10)

        username_time_layout = QtWidgets.QVBoxLayout()
        username_time_layout.setContentsMargins(0, 0, 0, 0)
        username_time_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        username_time_layout.setSpacing(0)

        chat = gv.get("selected_chat")

        self.name = QtWidgets.QLabel(chat.user.display_name if chat else "")
        self.name.setStyleSheet("font-size: 20px; color: white;")
        self.time = QtWidgets.QLabel(format_timestamp(chat.updated_at) if chat else "")
        if chat:
            if chat.user.is_online:
                self.time.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 14px")
            else:
                self.time.setStyleSheet("color: grey; font-size: 14px")
        username_time_layout.addWidget(self.name)
        username_time_layout.addWidget(self.time)

        self.avatar = RoundedAvatar(avatar_url=chat.user.avatar if chat else "", size=(60, 60))
        user_info_layout.addWidget(self.avatar)
        user_info_layout.addLayout(username_time_layout)

        phone_info_layout = QtWidgets.QHBoxLayout()
        phone_info_layout.setContentsMargins(10, 0, 0, 0)
        phone_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        phone_info_layout.setSpacing(20)
        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon("ri.contacts-book-2-fill", color="white").pixmap(40, 40))
        phone_number_description_layout = QtWidgets.QVBoxLayout()
        phone_number_description_layout.setSpacing(0)
        self.phone_number = QtWidgets.QLabel(chat.user.email if chat else "")
        self.phone_number.setStyleSheet("font-size: 14px; color: white")
        self.phone_number.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        description = QtWidgets.QLabel("Email")
        description.setStyleSheet("font-size: 10px; color: grey")
        phone_number_description_layout.addWidget(self.phone_number)
        phone_number_description_layout.addWidget(description)

        phone_info_layout.addWidget(icon)
        phone_info_layout.addLayout(phone_number_description_layout)

        username_info_layout = QtWidgets.QHBoxLayout()
        username_info_layout.setContentsMargins(10, 0, 0, 0)
        username_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        username_info_layout.setSpacing(20)
        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon("mdi6.information-outline", color="white").pixmap(40, 40))
        username_description_layout = QtWidgets.QVBoxLayout()
        username_description_layout.setSpacing(0)
        self.username = QtWidgets.QLabel("@" + chat.user.username if chat else "")
        self.username.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.username.setStyleSheet(f"font-size: 14px; color: {Colors.PRIMARY}")
        description = QtWidgets.QLabel("Username")
        description.setStyleSheet("font-size: 10px; color: grey")
        username_description_layout.addWidget(self.username)
        username_description_layout.addWidget(description)

        username_info_layout.addWidget(icon)
        username_info_layout.addLayout(username_description_layout)

        self.stats = QtWidgets.QVBoxLayout()
        self.stats.setSpacing(0)
        # if chat:
        #     if chat.stats.photos:
        #         self.stats.addWidget(
        #             IconedButton(
        #                 "mdi.google-photos",
        #                 f"{chat.stats.photos} Photos",
        #             )
        #         )
        #     if chat.stats.videos:
        #         self.stats.addWidget(IconedButton("fa5s.video", f"{chat.stats.videos} Videos"))
        #     if chat.stats.files:
        #         self.stats.addWidget(IconedButton("fa5.file-alt", f"{chat.stats.files} Files"))
        #     if chat.stats.links:
        #         self.stats.addWidget(IconedButton("fa5s.link", f"{chat.stats.links} Links"))
        #     if chat.stats.voices:
        #         self.stats.addWidget(IconedButton("ri.voiceprint-line", f"{chat.stats.voices} Voices"))

        actions = QtWidgets.QVBoxLayout()
        actions.setSpacing(2)
        actions.addWidget(
            IconedButton(
                "mdi.share",
                "Share this contact",
            )
        )
        actions.addWidget(IconedButton("mdi.square-edit-outline", "Edit this contact"))
        actions.addWidget(
            IconedButton(
                "mdi.delete",
                "Delete this contact",
            )
        )
        actions.addWidget(IconedButton("mdi.block-helper", "Block this user", color="red"))

        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(user_info_layout)
        self.main_layout.addWidget(Divider())
        self.main_layout.addLayout(phone_info_layout)
        self.main_layout.addLayout(username_info_layout)
        self.main_layout.addWidget(Divider())
        self.main_layout.addLayout(self.stats)
        self.main_layout.addWidget(Divider())
        self.main_layout.addLayout(actions)

        self.setFixedWidth(0)
        QtCore.QTimer.singleShot(0, self.show_animation)

    def change_chat(self, chat: ChatType):
        self.avatar.change_source(chat.user.avatar)
        self.name.setText(chat.user.username)
        self.time.setText(format_timestamp(chat.updated_at))

        if chat.user.is_online:
            self.time.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 14px")
        else:
            self.time.setStyleSheet("color: grey; font-size: 14px")

        self.phone_number.setText(chat.user.email)
        self.username.setText("@" + chat.user.username)
        while self.stats.count() > 0:
            item = self.stats.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # if chat.stats.photos:
        #     self.stats.addWidget(IconedButton("mdi.google-photos", f"{chat.stats.photos} Photos"))
        # if chat.stats.videos:
        #     self.stats.addWidget(
        #         IconedButton(
        #             "fa5s.video",
        #             f"{chat.stats.videos} Videos",
        #         )
        #     )
        # if chat.stats.files:
        #     self.stats.addWidget(
        #         IconedButton(
        #             "fa5.file-alt",
        #             f"{chat.stats.files} Files",
        #         )
        #     )
        # if chat.stats.links:
        #     self.stats.addWidget(
        #         IconedButton(
        #             "fa5s.link",
        #             f"{chat.stats.links} Links",
        #         )
        #     )
        # if chat.stats.voices:
        #     self.stats.addWidget(IconedButton("ri.voiceprint-line", f"{chat.stats.voices} Voices"))

    def close(self) -> bool:
        self.sidebar_closed.emit("closed")
        self.hide_animation(self.deleteLater)
        return True

    def show_animation(self):
        self.animation = QtCore.QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)  # Animation duration in milliseconds
        self.animation.setStartValue(0)
        self.animation.setEndValue(300)  # Final width
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)  # Smooth animation curve
        self.animation.start()

    def hide_animation(self, on_finished):
        self.animation = QtCore.QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(300)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)

        # Connect finished signal if callback provided
        if on_finished:
            self.animation.finished.connect(on_finished)

        self.animation.start()
