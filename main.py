import argparse
import sys
from typing import Optional

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QSettings, Qt, Signal

import env
from chat_types import ChatType, MessageType
from components.main.chat_list import ChatList
from components.main.chatbox import ChatBox
from components.main.login import Login
from components.main.settings_modal import SettingsModal
from components.main.sidebar import Sidebar
from lib.config import ConfigManager
from lib.conn import Conn
from utils import gv  # gv standas for global variable, because can't use global
from utils.action_handler import ActionHandler


class ChatApp(QtWidgets.QMainWindow):
    show_login_window = Signal()
    search_results_received = Signal(list)
    fetched_chats = Signal(list)
    fetched_messages = Signal(list)
    new_message = Signal(MessageType, str)
    message_deleted = Signal(str)
    message_edited = Signal(dict)
    messages_read = Signal(list)
    on_logout = Signal()

    def __init__(self, settings_instance: str):
        super().__init__()
        self.config = ConfigManager()
        self.settings = QSettings("Veia Sp.", settings_instance)
        self.refresh_token = settings.value("refresh_token")
        self.access_token = settings.value("access_token")
        self.conn = Conn(env.HOST, env.PORT, self.access_token)
        self.conn.connected_callback = self.on_connect
        self.conn.disconnected_callback = self.on_disconnect
        self.conn.on_message_callback = self.on_message

        self.user: Optional[dict] = None
        self.connected = False
        self.chats = []

        self.selected_chat: Optional[ChatType] = None
        self.sidebar_opened = False

        self.settings_modal = None

        # Main widget and layout
        self.setWindowTitle("Veia")
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

        if self.config.get("ui", "font", ""):
            self.apply_font(self.config.get("ui", "font"))

        self.search_results_received.connect(self.chat_list.load_search_results)
        self.fetched_chats.connect(self.chat_list.load_chats)
        self.fetched_messages.connect(self.chat_area.load_messages)
        self.new_message.connect(self.on_new_message)
        self.on_logout.connect(self.logout)
        self.message_deleted.connect(self.chat_area.delete_message)
        self.message_edited.connect(self.chat_area.edit_message)
        self.messages_read.connect(self.chat_area.read_message)
        self.conn.start()
        gv.set_conn(self.conn)

    def setup_shortcuts(self):
        ctrlTab = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Tab"), self)
        ctrlTab.activated.connect(self.select_next_chat)
        ctrlShiftTab = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+Tab"), self)
        ctrlShiftTab.activated.connect(self.select_previous_chat)

    def select_next_chat(self):
        for index, chat in enumerate(self.chats):
            if chat == self.selected_chat:
                if index == len(self.chats) - 1:
                    self.chat_selected(self.chats[0].id)
                else:
                    self.chat_selected(self.chats[index + 1].id)
                break

    def select_previous_chat(self):
        for index, chat in enumerate(self.chats):
            if chat == self.selected_chat:
                if index == 0:
                    self.chat_selected(self.chats[-1].id)
                else:
                    self.chat_selected(self.chats[index - 1].id)
                break

    def chat_selected(self, chat_id):
        if self.selected_chat:
            print(self.selected_chat.id == chat_id)
        if self.selected_chat and chat_id == self.selected_chat.id:
            return
        print("heyyyo\n\n\n\n\n\n")
        for chat in self.chats:
            if chat.id == chat_id:
                self.selected_chat = chat
                gv.set("selected_chat", self.selected_chat)
                self.chat_list.set_active_item_by_id(chat.id)
                self.chat_area.change_chat_user(chat)
                if self.sidebar_opened:
                    self.sidebar.change_chat(chat)

                data = {"action": "get_messages", "data": {"chat_id": chat.id}}
                self.conn.send_data(data)

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
        self.settings_modal.logout_triggered.connect(self.logout)
        self.settings_modal.move_to_center()
        self.settings_modal.show()

    def logout(self):
        self.settings.setValue("refresh_token", None)
        self.settings.setValue("access_token", None)
        self.show_login_window.emit()
        self.destroy()

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

    def on_message(self, data):
        ActionHandler(data, self).handle()

    def on_new_message(self, message_item: MessageType, chat_id: str):
        if self.selected_chat and self.selected_chat.id == chat_id:
            self.chat_area.add_new_message(message_item)

    def on_authenticate(self, data: dict):
        data_to_send = {"action": "get_chats"}
        self.conn.send_data(data_to_send)
        self.user = data.get("data", {}).get('user', {})
        gv.set("user", self.user)

    def closeEvent(self, event) -> None:
        self.conn.stop()
        return super().closeEvent(event)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat Application')
    parser.add_argument('--instance', type=int, default=0,
                       help='Instance number for separate settings (default: 0)')
    args = parser.parse_args()

    settings_instance = "Veia"
    if args.instance > 0:
        settings_instance = f"Veia_{args.instance}"

    settings = QSettings("Veia Sp.", settings_instance)
    refresh_token = settings.value("refresh_token")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    def show_main_window():
        main_window = ChatApp(settings_instance)
        main_window.show()

    def show_login_window():
        login_window = Login(env.HOST, env.PORT, settings_instance)
        login_window.show()

    if refresh_token:
        window = ChatApp(settings_instance)
        window.show_login_window.connect(show_login_window)
    else:
        login_window = Login(env.HOST, env.PORT, settings_instance)
        login_window.login_successful.connect(show_main_window)
        window = login_window

    window.show()
    sys.exit(app.exec())
