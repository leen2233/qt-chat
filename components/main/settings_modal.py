import qtawesome as qta
from PySide6 import QtCore
from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QCursor, QFontDatabase
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from components.ui.settings_header import Header
from styles import Colors


class SettingsItem(QWidget):
    clicked = Signal()

    def __init__(self, icon_name, text, value):
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
        self.icon.setPixmap(qta.icon(icon_name, color="white").pixmap(24, 24))
        self.text = QLabel(text)
        self.text.setStyleSheet("color: white; font-size: 14px")
        self.current_value = QLabel(value)
        self.current_value.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 14px")
        self.main_layout.addWidget(self.icon)
        self.main_layout.addWidget(self.text)
        self.main_layout.addStretch()
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
                f"background-color: #30302e; border-radius: 5px; color: white; font-family: {family}"
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


class SettingsModal(QFrame):
    font_applied = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("floatingPanel")
        self.setStyleSheet("""
            #floatingPanel {
                background-color: #262624;
                border-radius: 10px;
                border: 1px solid #3C3C3C;
            }
        """)
        self.setVisible(True)
        self.setMinimumHeight(600)
        self.setMinimumWidth(300)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.header = Header("Settings")
        self.header.close_clicked.connect(self.close)

        fonts_button = SettingsItem("mdi.format-font", "Fonts", "Default")
        fonts_button.clicked.connect(self.open_font_settings)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(fonts_button)
        self.main_layout.addStretch()

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
