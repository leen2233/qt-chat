import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor


class IconedButton(QtWidgets.QWidget):
    clicked = Signal()

    def __init__(self, icon_name, text, color="white", height=45, margin=0):
        super().__init__()
        self.setFixedHeight(height)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(f"margin: {margin}px")

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(20, 0, 10, 0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setSpacing(25)

        self.hover_color = "#333333"
        self.normal_color = "transparent"
        self.margin = margin

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(qta.icon(icon_name, color=color).pixmap(24, 24))
        self.text = QtWidgets.QLabel(text)
        self.text.setStyleSheet(f"color: {color}; font-size: 14px")
        self.main_layout.addWidget(self.icon)
        self.main_layout.addWidget(self.text)

    def update_background(self, color):
        """Update the background color using palette"""
        self.setStyleSheet(f"background-color: {color}; border-radius: 14px; margin: {self.margin}px")

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
