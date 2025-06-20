import sys
from typing import Optional

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QSettings, Qt, Signal

import env
from chat_types import MessageType
from components.main.chat_list import ChatList
from components.main.chatbox import ChatBox
from components.main.login import Login
from components.main.settings_modal import SettingsModal
from components.main.sidebar import Sidebar
from lib.config import ConfigManager
from lib.conn import Conn
from utils.action_handler import ActionHandler


class ChatApp(QtWidgets.QMainWindow):
    show_login_window = Signal()
    search_results_received = Signal(list)
    fetched_chats = Signal(list)
    fetched_messages = Signal(list)
    new_message = Signal(MessageType)
    message_deleted = Signal(str)
    message_edited = Signal(dict)
    on_logout = Signal()

    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.settings = QSettings("Veia Sp.", "Veia")
        self.refresh_token = settings.value("refresh_token")
        self.access_token = settings.value("access_token")
        self.conn = Conn(env.HOST, env.PORT, self.access_token)
        self.conn.connected_callback = self.on_connect
        self.conn.disconnected_callback = self.on_disconnect
        self.conn.on_message_callback = self.on_message

        self.user = None
        self.connected = False
        self.chats = []

        self.selected_chat = None
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
        self.chat_list.send_data.connect(self.send_data)

        # Main chat area
        self.chat_area = ChatBox()
        self.chat_area.sidebar_toggled_signal.connect(self.toggle_sidebar)
        self.chat_area.message_sent.connect(self.send_message)
        self.chat_area.message_edited.connect(self.edit_message)
        self.chat_area.message_deleted.connect(self.delete_message)

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
        self.new_message.connect(self.chat_area.add_message)
        self.on_logout.connect(self.logout)
        self.message_deleted.connect(self.chat_area.delete_message)
        self.message_edited.connect(self.chat_area.edit_message)
        self.conn.start()

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
        for chat in self.chats:
            if chat.id == chat_id:
                self.selected_chat = chat
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
        self.settings_modal = SettingsModal(parent=self.central_widget, user=self.user)
        self.settings_modal.font_applied.connect(self.apply_font)
        self.settings_modal.logout_triggered.connect(self.logout)
        self.settings_modal.send_data.connect(self.send_data)
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

    def send_message(self, data: dict):
        if self.selected_chat:
            data["chat_id"] = self.selected_chat.id
            data = {"action": "new_message", "data": data}
            self.send_data(data)
        else:
            print("No chat selected")

    def edit_message(self, data: dict):
        data = {"action": "edit_message", "data": data}
        self.send_data(data)

    def delete_message(self, message_id: str):
        data = {'action': 'delete_message', "data": {"message_id": message_id}}
        self.send_data(data)

    def send_data(self, data):
        self.conn.send_data(data)

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

    def on_authenticate(self, data: dict):
        data_to_send = {"action": "get_chats"}
        self.conn.send_data(data_to_send)
        print(data)
        self.user = data.get("data", {}).get('user', {})
        print(self.user)

    def closeEvent(self, event) -> None:
        self.conn.stop()
        return super().closeEvent(event)


if __name__ == "__main__":
    settings = QSettings("Veia Sp.", "Veia")
    refresh_token = settings.value("refresh_token")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    def show_main_window():
        main_window = ChatApp()
        main_window.show()

    def show_login_window():
        login_window = Login(env.HOST, env.PORT)
        login_window.show()

    if refresh_token:
        window = ChatApp()
        window.show_login_window.connect(show_login_window)
    else:
        login_window = Login(env.HOST, env.PORT)
        login_window.login_successful.connect(show_main_window)
        window = login_window

    window.show()
    sys.exit(app.exec())
