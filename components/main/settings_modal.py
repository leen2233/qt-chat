import qtawesome as qta
import requests
from PySide6 import QtCore
from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QCursor, QFontDatabase
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import env
from components.ui.rounded_avatar import RoundedAvatar
from components.ui.settings_header import Header
from styles import Colors


class SettingsItem(QWidget):
    clicked = Signal()

    def __init__(self, icon_name, text, value=None, color="white"):
        super().__init__()
        self.setFixedHeight(40)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("margin: 0 10px")

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(15, 0, 10, 0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setSpacing(0)

        self.hover_color = "#333333"
        self.normal_color = "transparent"

        self.icon = QLabel()
        self.icon.setPixmap(qta.icon(icon_name, color=color).pixmap(24, 24))
        self.text = QLabel(text)
        self.text.setStyleSheet(f"color: {color}; font-size: 14px")
        self.main_layout.addWidget(self.icon)
        self.main_layout.addWidget(self.text)
        self.main_layout.addStretch()

        if value:
            self.current_value = QLabel(value)
            self.current_value.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 14px")
            self.main_layout.addWidget(self.current_value)

    def update_background(self, color):
        """Update the background color using palette"""
        self.setStyleSheet(f"background-color: {color}; border-radius: 14px; margin: 0 10px")

    def enterEvent(self, event):
        """Handle mouse enter event"""
        self.update_background(self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event"""
        self.update_background(self.normal_color)
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        self.clicked.emit()
        super().mousePressEvent(event)


class FontSettings(QFrame):
    close_clicked = Signal()
    font_applied = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.selected_font = None

        self.setObjectName("fontsSettings")
        self.setStyleSheet("""
            #fontsSettings {
                background-color: #262624;
                border-radius: 10px;
                border: 1px solid #3C3C3C;
            }
        """)
        self.setVisible(True)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        if parent:
            self.setMinimumHeight(parent.height())
            self.setMinimumWidth(parent.width())

        self.header = Header("Font Settings", show_back=True)
        self.header.close_clicked.connect(self.close_clicked.emit)
        self.header.back_clicked.connect(self.back)

        self.items_layout = QVBoxLayout()
        self.items_layout.setContentsMargins(20, 0, 20, 0)

        self.font_size_label = QLabel("Font Family")
        self.font_size_label.setStyleSheet("color: #FFFFFF; font-size: 20px")

        self.font_list = QListWidget()
        self.font_list.setSpacing(2)
        self.font_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.font_list.setStyleSheet("background-color: #30302e; border-radius: 5px")
        self.font_list.itemClicked.connect(self.on_font_selected)

        self.actions_layout = QHBoxLayout()
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(10)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedHeight(30)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.setStyleSheet(
            "background-color: transparent; border: 1px solid grey; color: white; border-radius: 10px"
        )
        self.cancel_button.clicked.connect(self.back)

        self.apply_button = QPushButton("Apply")
        self.apply_button.setFixedHeight(30)
        self.apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_button.setStyleSheet(
            f"background-color: {Colors.PRIMARY}; border: 1px solid {Colors.PRIMARY}; color: white; border-radius: 10px"
        )
        self.apply_button.clicked.connect(self.apply_font)

        self.actions_layout.addWidget(self.cancel_button)
        self.actions_layout.addWidget(self.apply_button)

        self.items_layout.addWidget(self.font_size_label)
        self.items_layout.addWidget(self.font_list)
        self.items_layout.addLayout(self.actions_layout)

        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.items_layout)
        self.main_layout.addStretch()

    def load_fonts(self):
        self.font_list.clear()
        font_db = QFontDatabase()
        writing_system = QFontDatabase.WritingSystem.Any
        families = font_db.families(writing_system)
        for family in families:
            item_widget = QLabel(family)
            item_widget.setStyleSheet(
                f"background-color: #30302e; border-radius: 5px; color: white; font-family: {family};"
            )
            item_widget.setObjectName("font-item")
            item_widget.setFont(family)
            item = QListWidgetItem(self.font_list)
            item.setSizeHint(item_widget.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, family)
            self.font_list.setItemWidget(item, item_widget)

    def show(self):
        parent_rect = self.parent().rect()
        start_pos = QPoint(parent_rect.width(), 0)
        end_pos = QPoint(0, 0)
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(250)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        self.animation.finished.connect(self.load_fonts)

    def back(self):
        parent_rect = self.parent().rect()
        start_pos = QPoint(0, 0)
        end_pos = QPoint(parent_rect.width(), 0)
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(250)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        self.animation.finished.connect(self.deleteLater)

    def apply_font(self):
        if self.selected_font:
            self.font_applied.emit(self.selected_font)
            self.back()

    def on_font_selected(self, item):
        font_family = item.data(Qt.ItemDataRole.UserRole)
        self.font_size_label.setFont(font_family)
        self.font_size_label.setStyleSheet(self.font_size_label.styleSheet() + f";font-family: {font_family}")
        self.header.header_label.setFont(font_family)
        self.header.header_label.setStyleSheet(self.header.header_label.styleSheet() + f";font-family: {font_family}")
        self.cancel_button.setFont(font_family)
        self.apply_button.setFont(font_family)
        self.selected_font = font_family


class EditProfile(QFrame):
    close_clicked = Signal()
    send_data = Signal(dict)

    def __init__(self, parent=None, user: dict = {}):
        super().__init__(parent=parent)
        self.selected_font = None
        self.user = user
        self.avatar_path = None

        self.setObjectName("fontsSettings")
        self.setStyleSheet("""
            #fontsSettings {
                background-color: #262624;
                border-radius: 10px;
                border: 1px solid #3C3C3C;
            }
        """)
        self.setVisible(True)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        if parent:
            self.setMinimumHeight(parent.height())
            self.setMinimumWidth(parent.width())

        self.header = Header("Font Settings", show_back=True)
        self.header.close_clicked.connect(self.close_clicked.emit)
        self.header.back_clicked.connect(self.back)

        self.items_layout = QVBoxLayout()
        self.items_layout.setContentsMargins(20, 0, 20, 0)

        avatar_layout = QHBoxLayout()
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar = RoundedAvatar(self.user.get("avatar"))
        self.avatar.setStyleSheet("background-color: red")
        change_avatar_button = QPushButton("Change")
        # change_avatar_button.setFixedHeight(30)
        # change_avatar_button.setFixedWidth(80)
        change_avatar_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                border: 1px solid #555;
                border-radius: 5px;
                color: white;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
        """)
        change_avatar_button.clicked.connect(self.select_avatar)
        avatar_layout.addWidget(self.avatar)
        avatar_layout.addWidget(change_avatar_button)

        full_name_label = QLabel("Full Name")
        full_name_label.setStyleSheet("color: white")
        self.full_name_input = QLineEdit(text=self.user.get("full_name"), placeholderText="Full Name")
        self.full_name_input.setFixedHeight(30)
        self.full_name_input.setStyleSheet("background-color: #30302e; border-radius: 10px; border: 0.5px solid grey; color: white; padding-left: 6px;")
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: white")
        self.username_input = QLineEdit(text=self.user.get("username"), placeholderText="Username")
        self.username_input.setFixedHeight(30)
        self.username_input.setStyleSheet("background-color: #30302e; border-radius: 10px; border: 0.5px solid grey; color: white; padding-left: 6px;")
        bio_label = QLabel("Bio")
        bio_label.setStyleSheet("color: white")
        self.bio_input = QTextEdit(documentTitle="Bio", plainText=self.user.get("bio"), placeholderText="Write about yourself")
        self.bio_input.setFixedHeight(60)
        self.bio_input.setStyleSheet("background-color: #30302e; border-radius: 10px; border: 0.5px solid grey; color: white; padding: 6px;")

        self.actions_layout = QHBoxLayout()
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(10)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedHeight(30)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.setStyleSheet(
            "background-color: transparent; border: 1px solid grey; color: white; border-radius: 10px"
        )
        self.cancel_button.clicked.connect(self.back)

        self.apply_button = QPushButton("Save")
        self.apply_button.setFixedHeight(30)
        self.apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_button.setStyleSheet(
            f"background-color: {Colors.PRIMARY}; border: 1px solid {Colors.PRIMARY}; color: white; border-radius: 10px"
        )
        self.apply_button.clicked.connect(self.save)

        self.actions_layout.addWidget(self.cancel_button)
        self.actions_layout.addWidget(self.apply_button)

        self.items_layout.addLayout(avatar_layout)
        self.items_layout.addWidget(full_name_label)
        self.items_layout.addWidget(self.full_name_input)
        self.items_layout.addWidget(username_label)
        self.items_layout.addWidget(self.username_input)
        self.items_layout.addWidget(bio_label)
        self.items_layout.addWidget(self.bio_input)
        self.items_layout.addLayout(self.actions_layout)

        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.items_layout)
        self.main_layout.addStretch()

    def show(self):
        parent_rect = self.parent().rect()
        start_pos = QPoint(parent_rect.width(), 0)
        end_pos = QPoint(0, 0)
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(250)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def back(self):
        parent_rect = self.parent().rect()
        start_pos = QPoint(0, 0)
        end_pos = QPoint(parent_rect.width(), 0)
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(250)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        self.animation.finished.connect(self.deleteLater)

    def save(self):
        avatar_url = None
        if self.avatar_path:
            with open(self.avatar_path, 'rb') as f:
                files = {"file": f}
                if env.IMAGE_HOST:
                    response = requests.post(env.IMAGE_HOST, files=files)
                    if response.status_code == 200:
                        avatar_url = response.json().get("url")
                    else:
                        print("[IMAGE UPLOAD ERRROR]", response.text)
                else:
                    print("[please set IMAGE_HOST at env]")

        data = {
            "action": "update_user",
            "data": {
                "full_name": self.full_name_input.text(),
                "username": self.username_input.text(),
                "bio": self.bio_input.toPlainText(),
                "avatar": avatar_url
            }
        }
        self.send_data.emit(data)

    def select_avatar(self):
        """Open file dialog to select new avatar"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg *.gif *.bmp)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                new_avatar_path = selected_files[0]
                print("selected avatar", new_avatar_path)
                self.avatar.change_source(new_path=new_avatar_path)
                self.avatar_path = new_avatar_path


class SettingsModal(QFrame):
    font_applied = Signal(str)
    logout_triggered = Signal()
    send_data = Signal(dict)

    def __init__(self, parent=None, user: dict={}):
        super().__init__(parent=parent)
        self.user = user

        self.setObjectName("floatingPanel")
        self.setStyleSheet("""
            #floatingPanel {
                background-color: #262624;
                border-radius: 10px;
                border: 1px solid #3C3C3C;
            }
        """)
        self.setVisible(True)
        self.setMinimumHeight(400)
        self.setMinimumWidth(300)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 10)

        self.header = Header("Settings")
        self.header.close_clicked.connect(self.close)

        user_data_layout = QHBoxLayout()
        user_data_layout.setContentsMargins(20, 10, 20, 10)

        avatar = RoundedAvatar(user.get("avatar"))
        username_email_layout = QVBoxLayout()
        username_email_layout.setSpacing(0)

        username = QLabel(user.get("username"))
        username.setStyleSheet("color: white; font-size: 17px")
        email = QLabel(user.get("email"))
        email.setStyleSheet("color: #ababab; font-size: 12px")

        username_email_layout.addWidget(username)
        username_email_layout.addWidget(email)
        edit_button = QPushButton(qta.icon("mdi.square-edit-outline", color="white"), "")
        edit_button.setFixedWidth(30)
        edit_button.setFixedHeight(30)
        edit_button.setStyleSheet("background-color: #333; border: none; border-radius: 5px")
        edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        edit_button.clicked.connect(self.open_edit_profile_settings)

        user_data_layout.addWidget(avatar)
        user_data_layout.addLayout(username_email_layout)
        user_data_layout.addStretch()
        user_data_layout.addWidget(edit_button)

        fonts_button = SettingsItem("mdi.format-font", "Fonts", "Default")
        fonts_button.clicked.connect(self.open_font_settings)
        logout_button = SettingsItem("mdi.logout-variant", "Logout", color="#cc3f3f")
        logout_button.clicked.connect(self.logout)

        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(user_data_layout)
        self.main_layout.addWidget(fonts_button)
        self.main_layout.addStretch()
        self.main_layout.addWidget(logout_button)

    def show(self):
        parent_rect = self.parent().rect()
        start_pos = QPoint((parent_rect.width() // 2 - self.width() // 2), parent_rect.height())
        end_pos = QPoint(
            (parent_rect.width() // 2 - self.width() // 2), (parent_rect.height() // 2 - self.height() // 2)
        )
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(250)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def close(self) -> bool:
        parent_rect = self.parent().rect()
        start_pos = QPoint(
            (parent_rect.width() // 2 - self.width() // 2), (parent_rect.height() // 2 - self.height() // 2)
        )
        end_pos = QPoint((parent_rect.width() // 2 - self.width() // 2), parent_rect.height())
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(250)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()
        return True

    def move_to_center(self):
        parent_rect = self.parent().rect()
        start_pos = QPoint(
            (parent_rect.width() // 2 - self.width() // 2), (parent_rect.height() // 2 - self.height() // 2)
        )
        self.move(start_pos)

    def open_font_settings(self):
        frame = FontSettings(self)
        frame.close_clicked.connect(self.close)
        frame.font_applied.connect(lambda font: self.font_applied.emit(font))
        frame.show()

    def open_edit_profile_settings(self):
        frame = EditProfile(self, user=self.user)
        frame.close_clicked.connect(self.close)
        frame.send_data.connect(lambda data: self.send_data.emit(data))
        frame.show()

    def logout(self):
        self.logout_triggered.emit()
