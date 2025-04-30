from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer


class TypingIndicator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.message_box = QtWidgets.QWidget()
        self.message_box.setMinimumWidth(80)
        self.message_box.setMaximumWidth(600)  # Maximum width for any message
        self.message_box.setStyleSheet("background-color: #30302e; border-radius: 10px; padding: 10px")
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.message_layout = QtWidgets.QVBoxLayout(self.message_box)
        self.message_layout.setContentsMargins(0, 0, 0, 0)
        self.message_layout.setSpacing(0)
        self.text = QtWidgets.QLabel("typing")
        self.text.setStyleSheet("color: white;")
        self.message_layout.addWidget(self.text)
        self.main_layout.addWidget(self.message_box)

        # Create a timer for animation
        self.dots = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        self.hide()  # Initially hidden

    def start(self):
        self.dots = 1
        self.text.setText("typing.")
        self.show()  # Make sure the widget is visible
        self.timer.start(500)  # Update every 500ms

    def stop(self):
        self.timer.stop()
        self.hide()

    def update_dots(self):
        if self.dots <= 3:
            self.dots += 1
        else:
            self.dots = 1
        self.text.setText("typing" + "." * self.dots)
