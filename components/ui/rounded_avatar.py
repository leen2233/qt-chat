from typing import Tuple

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from utils.media import check_media_if_exists, get_absolute_path


class RoundedAvatar(QtWidgets.QWidget):
    def __init__(self, avatar_url, size: Tuple[int, int] = (40, 40), name: str = "", parent=None):
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.setStyleSheet("background-color: transparent;")
        self.given_size = size
        self.nm = QNetworkAccessManager()
        self.name = name
        self.url = avatar_url

        self.avatar = QtWidgets.QLabel(self)
        self.avatar.setFixedSize(size[0], size[1])
        self.avatar.setScaledContents(True)  # Important for proper scaling
        self.avatar.setStyleSheet("background-color: transparent;")

        if avatar_url:
            file_path = check_media_if_exists(avatar_url.split("/")[-1])
            print(file_path)
            if file_path:
                pixmap = QPixmap(file_path)
                size = self.avatar.width()
                rounded = self.create_rounded_pixmap(pixmap, size)
                if self.avatar:
                    self.avatar.setPixmap(rounded)
            else:
                self.nm.finished.connect(self.on_image_loaded)
                url = QUrl(avatar_url)
                request = QNetworkRequest(url)
                self.nm.get(request)
                self.set_default_avatar()

        else:
            # Default placeholder for avatar
            self.set_default_avatar()

    def set_default_avatar(self):
        initials = self.get_initials(self.name)
        if initials:
            color = self.get_avatar_color(initials)

            pixmap = QPixmap(self.given_size[0], self.given_size[1])
            pixmap.fill(QColor(color))

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.GlobalColor.white)
            font = QFont()
            font.setBold(True)
            font.setPointSize(int(self.given_size[1] * 0.3))
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, initials)
            painter.end()

            rounded = self.create_rounded_pixmap(pixmap, self.given_size[0])
        else:
            pixmap = QPixmap(self.given_size[0], self.given_size[1])
            pixmap.fill(QColor("#808080"))  # Gray placeholder

            # Create rounded placeholder
            rounded = self.create_rounded_pixmap(pixmap, self.given_size[0])
        self.avatar.setPixmap(rounded)

    def create_rounded_pixmap(self, original_pixmap, size):
        """Create a rounded version of the pixmap"""
        # Create a new transparent pixmap of the desired size
        rounded = QPixmap(size, size)
        rounded.fill(Qt.GlobalColor.transparent)

        # Create a painter to draw on the new pixmap
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create a circular path
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)

        # Set the clipping path
        painter.setClipPath(path)

        # Draw the original pixmap onto the new one, scaled to fit
        scaled_pixmap = original_pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        # Calculate centering if aspect ratio isn't 1:1
        x_offset = (scaled_pixmap.width() - size) / 2 if scaled_pixmap.width() > size else 0
        y_offset = (scaled_pixmap.height() - size) / 2 if scaled_pixmap.height() > size else 0

        painter.drawPixmap(-x_offset, -y_offset, scaled_pixmap)

        # Draw a border
        painter.setPen(QtGui.QPen(QColor("#444444"), 1))
        painter.drawEllipse(0, 0, size - 1, size - 1)  # -1 to fit border inside the pixmap

        painter.end()
        return rounded

    def on_image_loaded(self, reply):
        """Handle when an avatar image is loaded from network"""
        if not str(reply.error()) == "NetworkError.NoError":
            print(f"Error loading avatar: {reply.errorString()}")
            reply.deleteLater()
            return

        data = reply.readAll()
        # Load the image data
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        file_path = get_absolute_path(self.url.split("/")[-1])
        with open(file_path, "wb") as f:
            f.write(data)

        if pixmap.isNull():
            print("Failed to load avatar image")
            reply.deleteLater()
            return

        # Create circular pixmap
        size = self.avatar.width()
        rounded = self.create_rounded_pixmap(pixmap, size)

        # Set the pixmap to the label
        if self.avatar:
            self.avatar.setPixmap(rounded)
            reply.deleteLater()

    def change_source(self, new_url=None, new_path=None, new_name: str=""):
        self.name = new_name
        self.set_default_avatar()
        if new_url:
            file_path = check_media_if_exists(new_url.split("/")[-1])
            self.url = new_url
            if file_path:
                pixmap = QPixmap(file_path)
                size = self.avatar.width()
                rounded = self.create_rounded_pixmap(pixmap, size)
                if self.avatar:
                    self.avatar.setPixmap(rounded)
            else:
                url = QUrl(new_url)
                request = QNetworkRequest(url)
                self.nm.get(request)

        elif new_path:
            pixmap = QPixmap(new_path)
            size = self.avatar.width()
            rounded = self.create_rounded_pixmap(pixmap, size)
            if self.avatar:
                self.avatar.setPixmap(rounded)

    def get_initials(self, text):
        if text:
            text = text.strip().split(" ")
            if len(text) == 1:
                return text[0][0].upper()
            else:
                return f"{text[0][0].upper()}{text[1][0].upper()}"
        return ""

    def get_avatar_color(self, letters: str):
        avatarColors = [
            '#5A8DEE', '#39C36E', '#F4B400', '#E040FB', '#FF6E40',
            '#00BCD4', '#FF8A65', '#7E57C2', '#26A69A', '#EC407A',
        ]
        return avatarColors[ord(letters[0]) % len(avatarColors)]
