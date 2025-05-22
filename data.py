from chat_types import ChatType, MessageType, StatType

CHAT_LIST = [
    ChatType(
        id=1,
        avatar="https://fastly.picsum.photos/id/689/200/200.jpg?hmac=2KHWG2UlfLNAWC1jiBz-LQ7b-TMOB4bcW-FVvdQ_7a4",
        name="John Doe",
        last_message="Hello!",
        time="online",
        phone_number="+99361234567",
        username="john244",
        stats=StatType(photos=10, videos=2, files=360, links=231, voices=2),
        messages=[
            MessageType(id=1, text="Hi there!", sender="me", time="10:00 AM", status=MessageType.Status.READ),
            MessageType(
                id=2,
                text="Hello!",
                sender="another",
                time="10:03 AM",
                reply_to=MessageType(id=1, text="Hi there!", sender="me", time="10:00 AM"),
            ),
            MessageType(
                id=3,
                text="""
            from PySide6.QtWidgets import QWidget, QApplication
            from PySide6.QtGui import QPainter, QFont, QFontMetrics, QTextLayout, QColor
            from PySide6.QtCore import QSize, Qt
            import sys

            class MessageWidget(QWidget):
                def __init__(self, text, time_str, max_width=300):
                    super().__init__()
                    self.text = text
                    self.time_str = time_str
                    self.max_width = max_width
                    self.font = QFont("Arial", 12)
                    self.time_font = QFont("Arial", 10)
                    self.padding = 5
                    self.lines = []
                    self.setMinimumSize(self.sizeHint())

                def sizeHint(self):
                    self._layout_text()
                    line_height = QFontMetrics(self.font).height()
                    total_lines = len(self.lines)
                    return QSize(self.max_width, total_lines * line_height + self.padding * 2)

                def _layout_text(self):
                    layout = QTextLayout(self.text, self.font)
                    layout.beginLayout()
                    self.lines = []
                    while True:
                        line = layout.createLine()
                        if not line.isValid():
                            break
                        line.setLineWidth(self.max_width - self.padding * 2)
                        self.lines.append(line)
                    layout.endLayout()
                    self.text_layout = layout

                def paintEvent(self, event):
                    painter = QPainter(self)
                    painter.setFont(self.font)
                    self._layout_text()
                    fm = QFontMetrics(self.font)
                    time_fm = QFontMetrics(self.time_font)
                    time_width = time_fm.horizontalAdvance(self.time_str)
                    line_height = fm.height()

                    y = self.padding
                    last_line = self.lines[-1]
                    last_start = last_line.textStart()
                    last_len = last_line.textLength()
                    last_text = self.text[last_start:last_start+last_len]
                    last_width = fm.horizontalAdvance(last_text)

                    for i, line in enumerate(self.lines):
                        start = line.textStart()
                        length = line.textLength()
                        text = self.text[start:start+length]
                        painter.drawText(self.padding, y + fm.ascent(), text)
                        y += line_height

                    # Handle time position
                    if last_text.strip() == "" or last_width + 5 + time_width > self.max_width - self.padding * 2:
                        # New line
                        time_x = self.width() - self.padding - time_width
                        time_y = y
                    else:
                        # Same line
                        time_x = self.padding + last_width + 5
                        time_y = y - line_height

                    painter.setFont(self.time_font)
                    painter.setPen(QColor(150, 150, 150))
                    painter.drawText(time_x, time_y + fm.ascent(), self.time_str)


            if __name__ == "__main__":
                app = QApplication(sys.argv)
                text = "This is a long message that spans\nmultiple lines to check the behavior.\n\nAnd ends with newline."
                time_str = "12:45"
                widget = MessageWidget(text, time_str)
                widget.show()
                sys.exit(app.exec())

            """,
                sender="me",
                time="10:05 AM",
                status=MessageType.Status.READ,
            ),
            MessageType(id=4, text="Pretty good, you?", sender="another", time="10:06 AM"),
            MessageType(id=5, text="Same here!", sender="me", time="10:07 AM"),
            MessageType(
                id=6,
                text="""But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?""",
                sender="another",
                time="10:07 AM",
            ),
            MessageType(
                id=6,
                text="""But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?""",
                sender="another",
                time="10:07 AM",
            ),
            MessageType(
                id=7,
                text="cool",
                sender="me",
                status=MessageType.Status.SENT,
                time="10:07 AM",
            ),
            MessageType(
                id=7,
                text="cool",
                reply_to=MessageType(
                    id=6,
                    text="""But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?""",
                    sender="another",
                    time="10:07 AM",
                ),
                sender="me",
                time="10:07 AM",
            ),
            MessageType(
                id=7,
                text="""Hey
hey
hey""",
                sender="another",
                time="10:07 AM",
            ),
        ],
    ),
    ChatType(
        id=2,
        avatar="https://fastly.picsum.photos/id/25/200/200.jpg?hmac=G4ZRBi0qdWfQJQs_yxNQr_LJJlf0V1_Pdj8Tp41xsJU",
        name="Jane Smith",
        last_message="Yeah it's awesome!",
        time="5 hours ago",
        phone_number="+99361234563",
        username="jane_smith",
        stats=StatType(photos=560, videos=20, files=254, links=825, voices=1),
        messages=[
            MessageType(id=8, text="Check this out!", sender="me", time="2:00 AM"),
            MessageType(id=9, text="Yeah it's awesome!", sender="another", time="2:05 AM"),
            MessageType(id=10, text="Got more to share?", sender="me", time="2:10 AM"),
            MessageType(id=11, text="Totally, later!", sender="another", time="2:15 AM"),
            MessageType(id=12, text="Can't wait!", sender="me", time="2:20 AM"),
        ],
    ),
    ChatType(
        id=3,
        avatar="https://fastly.picsum.photos/id/354/200/200.jpg?hmac=ykMwenrB5tcaT_UHlYwh2ZzAZ4Km48YOmwJTFCiodJ4",
        name="Alice Johnson",
        last_message="Hey!",
        time="just now",
        phone_number="+99361234565",
        username="alice.johnson",
        stats=StatType(photos=69, videos=34, links=360, voices=None, files=None),
        messages=[
            MessageType(id=13, text="Hey!", sender="another", time="10:30 AM"),
            MessageType(id=14, text="What's up?", sender="me", time="10:31 AM"),
            MessageType(id=15, text="Just chilling!", sender="another", time="10:32 AM"),
            MessageType(id=16, text="Nice, any plans?", sender="me", time="10:33 AM"),
            MessageType(id=17, text="Maybe a movie!", sender="me", time="10:34 AM"),
        ],
    ),
]
