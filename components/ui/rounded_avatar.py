from typing import Tuple

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest


class RoundedAvatar(QtWidgets.QWidget):
    def __init__(self, avatar_url, size: Tuple[int, int] = (40, 40), parent=None):
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.setStyleSheet("background-color: transparent;")
        self.given_size = size
        self.nm = QNetworkAccessManager()

        self.avatar = QtWidgets.QLabel(self)
        self.avatar.setFixedSize(size[0], size[1])
        self.avatar.setScaledContents(True)  # Important for proper scaling
        self.avatar.setStyleSheet("background-color: transparent;")

        self.nm.finished.connect(self.on_image_loaded)
        url = QUrl(avatar_url)
        request = QNetworkRequest(url)
        self.nm.get(request)

        # Default placeholder for avatar
        self.set_default_avatar()

    def set_default_avatar(self):
        """Set a default placeholder for the avatar"""
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

        # Load the image data
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())

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

    def change_source(self, new_url):
        self.set_default_avatar()
        url = QUrl(new_url)
        request = QNetworkRequest(url)
        self.nm.get(request)
