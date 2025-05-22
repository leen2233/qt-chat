import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor

from chat_types import MessageType
from styles import Colors, build_reply_to_label_style, context_menu_style


class HighlightableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._base_color = QColor(0, 0, 0, 0)
        self._current_color = QColor(self._base_color)

        self.setAutoFillBackground(True)
        self._update_stylesheet()

        self._animation = QtCore.QPropertyAnimation(self, b"highlight_color")
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)

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
        if self._animation.state() == QtCore.QAbstractAnimation.State.Running:
            self._animation.stop()

        if highlight_color is None:
            highlight_color = QColor(201, 100, 66, 100)

        self._animation.setDuration(duration // 2)  # Half duration for highlighting
        self._animation.setStartValue(self._current_color)
        self._animation.setEndValue(highlight_color)

        self.second_animation = QtCore.QPropertyAnimation(self, b"highlight_color")
        self.second_animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
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

    def __init__(self, message: MessageType, previous, next):
        super().__init__()
        self.message_type = message
        self.message = message.text
        self.author = message.sender
        self.time = message.time
        self.is_mine = message.sender == "me"

        self.previous = self.author == previous
        self.next = self.author == next

        self.set_width = False

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("border-radius: 20px; padding: 0px; margin: 0px")
        # self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        top_margin = 2 if self.previous else 10
        bottom_margin = 2 if self.next else 10
        self.main_layout.setContentsMargins(4, top_margin, 4, bottom_margin)
        # self.main_layout.setContentsMargins(10, 5, 10, 5)

        self.message_box = QtWidgets.QWidget()
        self.message_box.setMinimumWidth(10)
        self.message_box.setMaximumWidth(600)  # Maximum width for any message

        top_border_radius = "20px"
        bottom_border_radius = "0px"
        if self.previous:
            top_border_radius = "5px"
        if self.next:
            bottom_border_radius = "5px"

        if self.is_mine:
            self.message_box.setStyleSheet(
                f"background-color: {Colors.USER_MESSAGE_BUBBLE}; border-radius: 20px; padding: 10px; border-bottom-right-radius: {bottom_border_radius}; border-top-right-radius: {top_border_radius}"
            )
            self.main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            self.message_box.setStyleSheet(
                f"background-color: {Colors.OTHER_MESSAGE_BUBBLE}; border-radius: 20px; padding: 10px;border-bottom-left-radius: {bottom_border_radius}; border-top-left-radius: {top_border_radius}"
            )
            self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.message_layout = QtWidgets.QVBoxLayout(self.message_box)
        self.message_layout.setContentsMargins(0, 0, 0, 0)
        self.message_layout.setSpacing(0)

        if message.reply_to:
            self.reply_to_label = QtWidgets.QPushButton(f" {message.reply_to.text[:100]}")
            self.reply_to_label.setMaximumHeight(80)
            self.reply_to_label.setObjectName("reply_to_label")
            if self.is_mine:
                self.reply_to_label.setStyleSheet(build_reply_to_label_style(is_mine=True))
            else:
                self.reply_to_label.setStyleSheet(build_reply_to_label_style())
            self.reply_to_label.setContentsMargins(0, 0, 0, 0)
            self.reply_to_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.reply_to_label.clicked.connect(lambda: self.message_highlight.emit(message.reply_to.id))
            self.message_layout.addWidget(self.reply_to_label)

        self.text_and_time_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)

        self.text = QtWidgets.QTextEdit()
        self.text.setPlainText(self.message)
        self.text.setMaximumWidth(590)
        self.text.setStyleSheet("font-size: 12px; padding: 5px; margin: 0; padding-right: 0;")
        self.text.setReadOnly(True)

        self.time_status_layout = QtWidgets.QHBoxLayout()
        self.time_status_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.time_status_layout.setSpacing(0)
        self.time_status_layout.setContentsMargins(0, 0, 0, 0)

        self.time_label = QtWidgets.QLabel(self.time)
        self.time_label.setStyleSheet(
            f"font-size: 10px; color: {'white' if self.is_mine else 'grey'}; padding: 0; margin: 0; position: absolute; left: 10px;"
        )
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setContentsMargins(0, 0, 0, 0)

        self.time_status_layout.addWidget(self.time_label)

        if self.author == "me":
            self.status = QtWidgets.QLabel()
            pixmap = None
            if self.message_type.status == MessageType.Status.SENDING:
                icon = qta.icon("mdi.clock-outline", color=Colors.TEXT_PRIMARY)
                pixmap = icon.pixmap(18, 18)
            elif self.message_type.status == MessageType.Status.SENT:
                icon = qta.icon("mdi.check", color=Colors.TEXT_PRIMARY)
                pixmap = icon.pixmap(20, 20)
            elif self.message_type.status == MessageType.Status.READ:
                icon = qta.icon("mdi.check-all", color=Colors.TEXT_PRIMARY)
                pixmap = icon.pixmap(20, 20)
            if pixmap:
                self.status.setPixmap(pixmap)
                self.status.setFixedWidth(20)
                self.status.setStyleSheet("padding: 0px; margin: 0px;")
                # self.status.setAlignment(Qt.AlignRight)
                self.status.setContentsMargins(0, 0, 0, 0)

                self.time_status_layout.addWidget(self.status)

        self.text_and_time_layout.addWidget(self.text)
        self.text_and_time_layout.addLayout(self.time_status_layout)

        self.message_layout.addLayout(self.text_and_time_layout)

        self.main_layout.addWidget(self.message_box)

        QTimer.singleShot(50, self.adjust_sizes)

    def adjust_sizes(self):
        # adjust QTextInput height and width
        doc_height = int(self.text.document().size().height())
        doc_width = int(self.text.document().idealWidth() + 20)
        new_height = int(max(doc_height + 10, 40))  # Adjust between min and max
        self.text.setMinimumHeight(new_height)
        self.text.setMaximumWidth(doc_width)

        # self.text.setStyleSheet("border: 1px solid red")
        # adjust message box width
        message_box_width = min(doc_width + self.time_status_layout.sizeHint().width() + 20, 600)
        self.message_box.setMaximumWidth(message_box_width)
        # adjust time and status thing
        print(self.width())
        if doc_height > 30 and doc_width > (self.width() - 50):  # more than one line and one line is full
            self.time_status_layout.removeWidget(self.time_label)
            self.time_label.setParent(self.text)
            self.time_label.setFixedWidth(self.time_label.width())
            if self.author == "me":
                self.time_status_layout.removeWidget(self.status)
                self.status.setParent(self.text)
                # self.status.setFixedWidth(self.status.width() + 20)

            cursor = self.text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor_rect = self.text.cursorRect(cursor)

            time_label_width = self.time_label.sizeHint().width()
            if cursor_rect.x() < self.message_box.width() - 100:
                if self.author == "me":
                    x = self.message_box.width() - time_label_width - 35
                else:
                    x = self.message_box.width() - time_label_width - 15
                y = cursor_rect.y() + cursor_rect.height() - 5

                self.time_label.move(x, y)
                self.time_label.show()
                if self.author == "me":
                    self.status.move(x + time_label_width, y)
                    self.status.show()

                self.message_box.setMinimumHeight(doc_height + 10)
            else:
                x = self.message_box.width() - time_label_width - 10
                y = cursor_rect.y() + cursor_rect.height() + 10

                self.time_label.move(x, y)
                self.time_label.show()
                self.message_box.setMinimumHeight(doc_height + 30)
        if not self.set_width:
            if self.text.width() < 530:
                self.text_and_time_layout.setDirection(QtWidgets.QBoxLayout.Direction.LeftToRight)
                self.time_status_layout.setContentsMargins(0, 13, 10, 0)
            else:
                self.time_status_layout.setContentsMargins(0, 0, 10, 10)
            self.set_width = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if event.size().width() < 600:
            self.adjust_sizes()

    def mouseDoubleClickEvent(self, event):
        self.reply_clicked.emit(self.message_type)

    def update_previous_next(self, previous=None, next=None):
        if previous:
            self.previous = previous
        if next:
            self.next = next
        top_margin = 2 if self.previous else 10
        bottom_margin = 2 if self.next else 10
        self.main_layout.setContentsMargins(4, top_margin, 4, bottom_margin)

    # def paintEvent(self, event):
    # if not self.set_width:
    #     if self.text.width() < 530:
    #         self.text_and_time_layout.setDirection(QtWidgets.QBoxLayout.Direction.LeftToRight)
    #         self.time_status_layout.setContentsMargins(0, 13, 10, 0)
    #     else:
    #         self.time_status_layout.setContentsMargins(0, 0, 10, 10)
    #     self.set_width = True

    # painter = QtGui.QPainter(self)
    # # Create a path for the bubble with tail
    # path = QtGui.QPainterPath()
    # rect = self.rect()

    # bubble_rect = QRect(rect)

    # minus_height = 10
    # if self.next:
    #     minus_height = 2

    # if self.is_mine:
    #     tail_points = [
    #         QPoint(self.width() + 20 - 20, bubble_rect.height() - minus_height),
    #         QPoint(self.width() + 20 - 30, bubble_rect.height() - minus_height),
    #         QPoint(self.width() + 20 - 30, bubble_rect.height() - (10 + minus_height)),
    #     ]
    # else:
    #     # Add tail on the left
    #     tail_points = [
    #         QPoint(10, bubble_rect.height() - (10 + minus_height)),
    #         QPoint(10, bubble_rect.height() - minus_height),
    #         QPoint(0, bubble_rect.height() - minus_height),
    #     ]

    # # Add the tail to the path
    # path.moveTo(tail_points[0])
    # path.lineTo(tail_points[1])
    # path.lineTo(tail_points[2])
    # path.lineTo(tail_points[0])

    # # Fill the bubble
    # painter.setPen(Qt.PenStyle.NoPen)
    # if self.is_mine:
    #     painter.setBrush("#202324")
    # else:
    #     painter.setBrush("#30302e")
    # painter.drawPath(path)

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
