from PySide6 import QtWidgets


class Message(QtWidgets.QWidget):
    def __init__(self, message, author, time):
        super().__init__()
        self.message = message
        self.author = author
        self.time = time
        self.setMaximumWidth(200)
        self.layout = QtWidgets.QHBoxLayout(self)

        self.text = QtWidgets.QLabel("test message")
        self.layout.addWidget(self.text)


class ChatBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { background-color: #2a2f3b; color: #ffffff; }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.messages_container = QtWidgets.QVBoxLayout(self)
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))
        self.messages_container.addWidget(Message("test message", "leen", "18:30"))

        self.chat_input = QtWidgets.QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.setFixedHeight(50)
        self.chat_input.setTextMargins(10, 10, 10, 10)

        self.layout.addLayout(self.messages_container)
        self.layout.addWidget(self.chat_input)
