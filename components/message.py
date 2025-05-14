import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPoint, QRect, Qt, Signal

from chat_types import MessageType
from styles import context_menu_style, reply_to_label_style


class Message(QtWidgets.QWidget):
    reply_clicked = Signal(MessageType)

    def __init__(self, message: MessageType):
        super().__init__()
        self.message_type = message
        self.message = message.text
        self.author = message.sender
        self.time = message.time
        self.is_mine = message.sender == "me"

        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        # self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        # self.main_layout.setContentsMargins(10, 5, 10, 5)

        self.message_box = QtWidgets.QWidget()
        self.message_box.setMinimumWidth(10)
        self.message_box.setMaximumWidth(600)  # Maximum width for any message

        if self.is_mine:
            self.message_box.setStyleSheet(
                "background-color: #202324; border-radius: 10px; padding: 10px; border-bottom-right-radius: 0px"
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

        if message.reply_to:
            self.reply_to_label = QtWidgets.QPushButton(f" {message.reply_to[:100]}")
            self.reply_to_label.setMaximumHeight(80)
            self.reply_to_label.setObjectName("reply_to_label")
            self.reply_to_label.setStyleSheet(reply_to_label_style)
            self.reply_to_label.setContentsMargins(0, 0, 0, 0)
            self.reply_to_label.setCursor(Qt.PointingHandCursor)
            self.message_layout.addWidget(self.reply_to_label)

        self.text = QtWidgets.QLabel(self.message)
        self.text.setMaximumWidth(600)
        self.text.setWordWrap(True)
        # self.text.setStyleSheet("padding: 10px")
        # self.text.setContentsMargins(0, 0, 0, -10)
        # self.text.setWordWrap(True)

        self.time_label = QtWidgets.QLabel(self.time)
        self.time_label.setStyleSheet("font-size: 10px; color: grey;")
        self.time_label.setAlignment(Qt.AlignRight)
        self.time_label.setContentsMargins(0, -10, 0, 0)

        self.message_layout.addWidget(self.text)
        self.message_layout.addWidget(self.time_label)

        self.main_layout.addWidget(self.message_box)

    #     self.adjust_width_to_text()

    # def adjust_width_to_text(self):
    #     font_metrics = QtGui.QFontMetrics(self.text.font())

    #     lines = self.message.split("\n")
    #     widest_line_width = 0

    #     for line in lines:
    #         line_width = font_metrics.horizontalAdvance(line)
    #         widest_line_width = max(widest_line_width, line_width)

    #     padding = 60
    #     time_width = font_metrics.horizontalAdvance(self.time)

    #     desired_width = min(max(widest_line_width, time_width) + padding, 400)

    #     self.message_box.setMinimumWidth(min(desired_width, 100))

    #     size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    #     self.message_box.setSizePolicy(size_policy)

    #     self.message_box.adjustSize()

    def mouseDoubleClickEvent(self, event):
        self.reply_clicked.emit(self.message_type)

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
        self.setMinimumHeight(self.text.height() + 45)

    def contextMenuEvent(self, event):
        # self.setStyleSheet(
        #     "QWidget { background-color: white; border-radius: 10px; padding: 10px; border-bottom-right-radius: 0px}"
        # )
        context_menu = QtWidgets.QMenu(self)
        reply_action = context_menu.addAction(qta.icon("mdi.reply-outline", color="white"), "Reply")
        select_action = context_menu.addAction(qta.icon("mdi.selection-ellipse-arrow-inside", color="white"), "Select")
        pin_action = context_menu.addAction(qta.icon("mdi.pin-outline", color="white"), "Pin")
        copy_action = context_menu.addAction(qta.icon("mdi.content-copy", color="white"), "Copy Text")
        forward_action = context_menu.addAction(qta.icon("mdi.arrow-top-right-bold-outline", color="white"), "Forward")
        context_menu.addSeparator()
        delete_action = context_menu.addAction(qta.icon("mdi.trash-can-outline", color="white"), "Delete")

        context_menu.setStyleSheet(context_menu_style)
        action = context_menu.exec_(event.globalPos())
        if action == reply_action:
            self.reply_clicked.emit(self.message_type)
