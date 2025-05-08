from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QPoint, QRect, Qt


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
            self.setStyleSheet(
                "QWidget { background-color: #202324; border-radius: 10px; padding: 10px; border-bottom-right-radius: 0px}"
            )
            self.main_layout.setAlignment(Qt.AlignRight)
        else:
            self.message_box.setStyleSheet(
                "background-color: #30302e; border-radius: 10px; padding: 10px;border-bottom-left-radius: 0px"
            )
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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # Create a path for the bubble with tail
        path = QtGui.QPainterPath()
        rect = self.rect()

        bubble_rect = QRect(rect)

        # Adjust rectangle to account for tail
        tail_width = 10
        tail_height = 15

        if self.is_mine:
            tail_points = [
                QPoint(self.width() + 20 - 20, bubble_rect.height() - 9),
                QPoint(self.width() + 20 - 30, bubble_rect.height() - 9),
                QPoint(self.width() + 20 - 30, bubble_rect.height() - 19),
            ]
        else:
            # Add tail on the left
            tail_points = [
                QPoint(10, bubble_rect.height() - 19),
                QPoint(10, bubble_rect.height() - 9),
                QPoint(0, bubble_rect.height() - 9),
            ]

        # Add the tail to the path
        path.moveTo(tail_points[0])
        path.lineTo(tail_points[1])
        path.lineTo(tail_points[2])
        path.lineTo(tail_points[0])

        # Fill the bubble
        painter.setPen(Qt.NoPen)
        if self.is_mine:
            painter.setBrush("#202324")
        else:
            painter.setBrush("#30302e")
        painter.drawPath(path)
