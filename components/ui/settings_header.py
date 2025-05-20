import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from styles import Colors


class Header(QWidget):
    close_clicked = Signal()
    back_clicked = Signal()

    def __init__(self, title: str, show_back: bool = False, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(f"background-color: {Colors.BACKGROUND_LIGHT}; border-radius: 10px;")
        self.setFixedHeight(50)
        header_layout = QHBoxLayout(self)
        if show_back:
            back_button = QPushButton(qta.icon("mdi.arrow-left", color="white", size=(18, 18)), "")
            back_button.setIconSize(QSize(25, 25))
            back_button.setStyleSheet("background-color: #262624; border: none; background-color: transparent")
            back_button.setCursor(Qt.CursorShape.PointingHandCursor)
            back_button.clicked.connect(self.handle_back)
            header_layout.addWidget(back_button)

        self.header_label = QLabel(title)
        self.header_label.setStyleSheet("color: white; font-size: 18px")
        close_button = QPushButton(qta.icon("mdi.close", color="white", size=(18, 18)), "")
        close_button.setIconSize(QSize(25, 25))
        close_button.setStyleSheet("border: none; background-color: transparent")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(self.handle_close)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(close_button)

    def handle_close(self):
        self.close_clicked.emit()

    def handle_back(self):
        self.back_clicked.emit()
