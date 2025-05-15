from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal


class TextEdit(QtWidgets.QTextEdit):
    enterPressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        # Check if Enter key is pressed
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Check if Shift is held down
            if event.modifiers() & Qt.ShiftModifier:
                # Insert a newline when Shift+Enter is pressed
                super().keyPressEvent(event)
            else:
                # Emit signal when Enter is pressed without Shift
                self.enterPressed.emit()
                event.accept()  # Consume the event
        else:
            # For all other keys, use the default behavior
            super().keyPressEvent(event)
