import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPoint, QRect, Qt, Signal
from PySide6.QtGui import QColor

from chat_types import MessageType
from styles import context_menu_style, reply_to_label_style


class HighlightableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._base_color = QColor(0, 0, 0, 0)
        self._current_color = QColor(self._base_color)

        self.setAutoFillBackground(True)
        self._update_stylesheet()

        self._animation = QtCore.QPropertyAnimation(self, b"highlight_color")
        self._animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def _update_stylesheet(self):
        """Update the widget's stylesheet with the current color"""
        self.setStyleSheet(
            f"border-radius: 20px;"
            f"background-color: rgba({self._current_color.red()}, "
            f"{self._current_color.green()}, {self._current_color.blue()}, "
            f"{self._current_color.alpha() / 255.0});"
        )

    def get_highlight_color(self):
        return self._current_color

    def set_highlight_color(self, color):
        self._current_color = color
        self._update_stylesheet()

    highlight_color = QtCore.Property(QColor, get_highlight_color, set_highlight_color)

    def set_base_color(self, color):
        """Set the widget's base color"""
        if isinstance(color, str) and color.lower() == "transparent":
            self._base_color = QColor(0, 0, 0, 0)
        else:
            self._base_color = color if isinstance(color, QColor) else QColor(color)

        self._current_color = QColor(self._base_color)
        self._update_stylesheet()

    def highlight(self, duration=600, highlight_color=None):
        """
        Highlight the widget with an animation

        Args:
            duration: The total animation duration in milliseconds
            highlight_color: The color to transition to (defaults to semi-transparent dark gray)
        """
        if self._animation.state() == QtCore.QPropertyAnimation.Running:
            self._animation.stop()

        if highlight_color is None:
            highlight_color = QColor(201, 100, 66, 100)

        self._animation.setDuration(duration // 2)  # Half duration for highlighting
        self._animation.setStartValue(self._current_color)
        self._animation.setEndValue(highlight_color)

        self.second_animation = QtCore.QPropertyAnimation(self, b"highlight_color")
        self.second_animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.second_animation.setDuration(duration // 2)
        self.second_animation.setStartValue(highlight_color)
        self.second_animation.setEndValue(self._base_color)

        self._animation.finished.connect(lambda: QtCore.QTimer.singleShot(1000, self.start_close_animation))

        self._animation.start()

    def start_close_animation(self):
        self.second_animation.start()


class Message(HighlightableWidget):
    reply_clicked = Signal(MessageType)
    message_highlight = Signal(int)

    def __init__(self, message: MessageType):
        super().__init__()
        self.message_type = message
        self.message = message.text
        self.author = message.sender
        self.time = message.time
        self.is_mine = message.sender == "me"

        self.set_width = False

        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("border-radius: 20px")
        # self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        # self.main_layout.setContentsMargins(10, 5, 10, 5)

        self.message_box = QtWidgets.QWidget()
        self.message_box.setMinimumWidth(10)
        self.message_box.setMaximumWidth(570)  # Maximum width for any message

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
            self.reply_to_label = QtWidgets.QPushButton(f" {message.reply_to.text[:100]}")
            self.reply_to_label.setMaximumHeight(80)
            self.reply_to_label.setObjectName("reply_to_label")
            self.reply_to_label.setStyleSheet(reply_to_label_style)
            self.reply_to_label.setContentsMargins(0, 0, 0, 0)
            self.reply_to_label.setCursor(Qt.PointingHandCursor)
            self.reply_to_label.clicked.connect(lambda: self.message_highlight.emit(message.reply_to.id))
            self.message_layout.addWidget(self.reply_to_label)

        self.text_and_time_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)

        self.text = QtWidgets.QLabel(self.message)
        self.text.setWordWrap(True)

        self.time_label = QtWidgets.QLabel(self.time)
        self.time_label.setStyleSheet("font-size: 10px; color: grey;")
        self.time_label.setAlignment(Qt.AlignRight)
        self.time_label.setContentsMargins(0, 0, 0, 0)

        self.text_and_time_layout.addWidget(self.text)
        self.text_and_time_layout.addWidget(self.time_label)

        self.message_layout.addLayout(self.text_and_time_layout)

        self.main_layout.addWidget(self.message_box)

    def mouseDoubleClickEvent(self, event):
        self.reply_clicked.emit(self.message_type)

    def paintEvent(self, event):
        if not self.set_width:
            print("setting width")
            if self.text.width() < 530:
                print(self.text.text()[:30], self.width(), self.text.width())
                self.text_and_time_layout.setDirection(QtWidgets.QBoxLayout.Direction.LeftToRight)
                self.time_label.setContentsMargins(0, 13, 10, 0)
            else:
                self.time_label.setContentsMargins(0, 0, 10, 10)
            self.set_width = True

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

    def contextMenuEvent(self, event):
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
