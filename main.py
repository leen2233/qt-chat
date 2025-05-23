import os
import sys
from typing import Optional

from dotenv import load_dotenv
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt

from components.main.chat_list import ChatList
from components.main.chatbox import ChatBox
from components.main.settings_modal import SettingsModal
from components.main.sidebar import Sidebar
from data import CHAT_LIST
from lib.config import ConfigManager
from lib.conn import Conn

load_dotenv()

HOST = os.getenv("HOST", "")
PORT = int(os.getenv("PORT", "9090"))


class ChatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.conn = Conn(HOST, PORT)
        self.conn.connected_callback = self.on_connect
        self.conn.disconnected_callback = self.on_disconnect

        self.connected = False

        self.selected_chat = None
        self.sidebar_opened = False

        self.settings_modal = None

        # Main widget and layout
        self.setWindowTitle("Telegram-like App")
        self.setMouseTracking(True)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Create and set up splitter
        self.splitter = QtWidgets.QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)  # Prevent collapsing sections
        self.splitter.setHandleWidth(1)

        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow{ background-color: #262624; color: #ffffff; }
        """)

        # chat list1
        self.chat_list = ChatList()
        self.chat_list.chat_selected.connect(self.chat_selected)
        self.chat_list.settings_clicked.connect(self.open_settings)

        # Main chat area
        self.chat_area = ChatBox()
        self.chat_area.sidebar_toggled_signal.connect(self.toggle_sidebar)

        self.splitter.addWidget(self.chat_list)
        self.splitter.addWidget(self.chat_area)
        self.splitter.setSizes([250, 750])
        self.main_layout.addWidget(self.splitter)

        self.chat_area.chat_input.setFocus(Qt.FocusReason.MouseFocusReason)
        # Window settings
        self.resize(1000, 600)

        self.setup_shortcuts()
        self.chat_list.load_chats(CHAT_LIST)

        if self.config.get("ui", "font", ""):
            self.apply_font(self.config.get("ui", "font"))

        self.conn.start()

    def setup_shortcuts(self):
        ctrlTab = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Tab"), self)
        ctrlTab.activated.connect(self.select_next_chat)
        ctrlShiftTab = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+Tab"), self)
        ctrlShiftTab.activated.connect(self.select_previous_chat)

    def select_next_chat(self):
        for index, chat in enumerate(CHAT_LIST):
            if chat == self.selected_chat:
                if index == len(CHAT_LIST) - 1:
                    self.chat_selected(CHAT_LIST[0].id)
                else:
                    self.chat_selected(CHAT_LIST[index + 1].id)
                break

    def select_previous_chat(self):
        for index, chat in enumerate(CHAT_LIST):
            if chat == self.selected_chat:
                if index == 0:
                    self.chat_selected(CHAT_LIST[-1].id)
                else:
                    self.chat_selected(CHAT_LIST[index - 1].id)
                break

    def chat_selected(self, chat_id):
        chat_id = int(chat_id)
        for chat in CHAT_LIST:
            if chat.id == chat_id:
                self.selected_chat = chat
                self.chat_list.set_active_item_by_id(chat.id)
                self.chat_area.load_messages(chat.messages)
                self.chat_area.change_chat_user(chat)
                if self.sidebar_opened:
                    self.sidebar.change_chat(chat)

    def sidebar_closed(self, state):
        self.sidebar_opened = False
        self.chat_area.sidebar_toggle()

    def toggle_sidebar(self, state: bool):
        if state is True:
            self.sidebar = Sidebar(self.selected_chat)
            self.sidebar.sidebar_closed.connect(self.sidebar_closed)
            self.splitter.addWidget(self.sidebar)
            self.sidebar_opened = True
        else:
            self.sidebar_opened = False

            def remove_sidebar():
                self.sidebar.deleteLater()

            self.sidebar.hide_animation(on_finished=remove_sidebar)

    def open_settings(self):
        self.settings_modal = SettingsModal(parent=self.central_widget)
        self.settings_modal.font_applied.connect(self.apply_font)
        self.settings_modal.move_to_center()
        self.settings_modal.show()

    def apply_font(self, font_name):
        # Create a font with the selected name
        font = QtGui.QFont(font_name)

        self.config.set("ui", "font", font_name)

        # Apply to application (affects new widgets)
        app: Optional[QtWidgets.QApplication] = QtWidgets.QApplication.instance()  # type: ignore
        if app:
            app.setFont(font)

            # Apply to all existing widgets through stylesheet
            font_style = f"* {{ font-family: '{font_name}'; }}"
            app.setStyleSheet(app.styleSheet() + font_style)

            # Force update on existing widgets
            for widget in app.allWidgets():
                widget.setFont(font)
                if type(widget) is not QtWidgets.QListWidget:
                    widget.update()

            # Update the main window and all its children
            self.updateGeometry()
            self.update()

    def resizeEvent(self, event):
        """Handle window resize events to reposition the panel if needed"""
        super().resizeEvent(event)

        if self.settings_modal:
            self.settings_modal.move_to_center()

    def on_connect(self):
        self.chat_list.handle_connected()

    def on_disconnect(self):
        self.chat_list.handle_disconnected()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
