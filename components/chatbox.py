from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt


class Message(QtWidgets.QWidget):
    def __init__(self, message, author, time, is_mine=False):
        super().__init__()
        self.message = message
        self.author = author
        self.time = time
        self.is_mine = is_mine

        # self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        # self.main_layout.setContentsMargins(10, 5, 10, 5)

        self.message_box = QtWidgets.QWidget()
        self.message_box.setMinimumWidth(10)
        self.message_box.setMaximumWidth(600)  # Maximum width for any message

        if is_mine:
            self.message_box.setStyleSheet("background-color: #202324; border-radius: 10px; padding: 10px")
            self.main_layout.setAlignment(Qt.AlignRight)
        else:
            self.message_box.setStyleSheet("background-color: #30302e; border-radius: 10px; padding: 10px")
            self.main_layout.setAlignment(Qt.AlignLeft)

        self.message_layout = QtWidgets.QVBoxLayout(self.message_box)
        self.message_layout.setContentsMargins(0, 0, 0, 0)
        self.message_layout.setSpacing(0)

        self.text = QtWidgets.QLabel(self.message)
        # self.text.setWordWrap(True)

        self.time_label = QtWidgets.QLabel(self.time)
        self.time_label.setStyleSheet("font-size: 10px; color: grey;")
        self.time_label.setAlignment(Qt.AlignRight)
        self.time_label.setContentsMargins(0, -10, 0, 0)

        self.message_layout.addWidget(self.text)
        self.message_layout.addWidget(self.time_label)

        self.main_layout.addWidget(self.message_box)

        self.adjust_width_to_text()

    def adjust_width_to_text(self):
        font_metrics = QtGui.QFontMetrics(self.text.font())

        lines = self.message.split("\n")
        widest_line_width = 0

        for line in lines:
            line_width = font_metrics.horizontalAdvance(line)
            widest_line_width = max(widest_line_width, line_width)

        padding = 60
        time_width = font_metrics.horizontalAdvance(self.time)

        desired_width = min(max(widest_line_width, time_width) + padding, 400)

        self.message_box.setMinimumWidth(min(desired_width, 100))

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.message_box.setSizePolicy(size_policy)

        self.message_box.adjustSize()


class ChatBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { background-color: #262624; color: #ffffff; }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for messages
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        # Container for messages
        self.messages_widget = QtWidgets.QWidget()
        self.messages_container = QtWidgets.QVBoxLayout(self.messages_widget)
        self.messages_container.setAlignment(Qt.AlignBottom)
        self.messages_container.setContentsMargins(0, 0, 0, 20)
        self.messages_container.addStretch()

        self.scroll_area.setWidget(self.messages_widget)

        self.add_message("test message", "another", "18:30", False)
        self.add_message(
            "test message1, looooooooooooooooooooooooooooong messssssssssssssssssssssssssssage.",
            "another",
            "18:31",
            True,
        )
        self.add_message("test message reply tc......s", "another", "18:32", False)

        # Input area
        self.input_part = QtWidgets.QHBoxLayout()

        self.chat_input = QtWidgets.QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.setFixedHeight(50)
        self.chat_input.setTextMargins(10, 10, 10, 10)
        self.chat_input.setStyleSheet("background-color: #30302e; border-radius: 10px; border: 0.5px solid grey")
        self.chat_input.returnPressed.connect(self.send_my_message)

        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.setFixedSize(50, 50)  # Set a fixed size for the button
        self.send_button.setStyleSheet(
            "background-color: #c96442; color: white; border-radius: 25px; font-weight: bold;"
        )
        self.send_button.clicked.connect(self.send_my_message)

        self.input_part.addWidget(self.chat_input)
        self.input_part.addWidget(self.send_button)

        # Add components to main layout
        self.layout.addWidget(self.scroll_area)
        self.layout.addLayout(self.input_part)

    def add_message(self, text, author, message_time, is_mine):
        message = Message(text, author, message_time, is_mine)
        self.messages_container.insertWidget(self.messages_container.count() - 1, message)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

        return message

    def send_my_message(self):
        text = self.chat_input.text()
        if text.strip():
            self.add_message(text, "me", "now", True)
            self.chat_input.setText("")
