from PySide6 import QtWidgets
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSettings, Qt, Signal

from lib.conn import Conn
from styles import Colors


class Login(QtWidgets.QMainWindow):
    login_successful = Signal()
    on_login = Signal(dict)

    def __init__(self, host, port, settings_instance: str, parent=None):
        super().__init__(parent=parent)
        self.settings_instance = settings_instance

        self.conn = Conn(host, port)
        self.conn.connected_callback = self.on_connect
        self.conn.disconnected_callback = self.on_disconnect
        self.conn.on_message_callback = self.on_message

        self.setStyleSheet("""
            QMainWindow{ background-color: #262624; color: #ffffff; }
        """)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)

        title = QtWidgets.QLabel("Veia")
        title.setStyleSheet("font-size: 30px; color: white; margin-bottom: 20px;")

        tab_container = QtWidgets.QFrame()
        tab_container.setFixedHeight(30)
        tab_container.setFixedWidth(200)
        tab_container.setStyleSheet("border-radius: 10px; border: 1px solid grey;")

        tab_layout = QtWidgets.QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        self.login_btn = QtWidgets.QPushButton("Login")
        self.login_btn.setFixedHeight(28)
        self.login_btn.setFixedWidth(99)
        self.signin_btn = QtWidgets.QPushButton("Sign Up")
        self.signin_btn.setFixedHeight(28)
        self.signin_btn.setFixedWidth(99)

        self.active_style = f"background-color: {Colors.PRIMARY}; color: white; border: none"

        self.inactive_style = "background-color: #262624; color: white; border: none"

        self.login_btn.setStyleSheet(self.active_style)
        self.signin_btn.setStyleSheet(self.inactive_style)

        self.login_btn.clicked.connect(lambda: self.switch_tab(0))
        self.signin_btn.clicked.connect(lambda: self.switch_tab(1))

        tab_layout.addWidget(self.login_btn)
        tab_layout.addWidget(self.signin_btn)

        self.stacked_widget = QtWidgets.QStackedWidget()

        login_widget = self.create_login_form()
        self.stacked_widget.addWidget(login_widget)

        # Sign up form
        signup_widget = self.create_signup_form()
        self.stacked_widget.addWidget(signup_widget)

        self.main_layout.addStretch()
        self.main_layout.addWidget(title)
        self.main_layout.setAlignment(title, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(tab_container)
        self.main_layout.setAlignment(tab_container, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.setAlignment(self.stacked_widget, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch()

        self.slide_animation = QPropertyAnimation(self.stacked_widget, b"geometry") # type: ignore
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.conn.start()

    def create_login_form(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setSpacing(10)

        self.login_error_message = QtWidgets.QLabel()
        self.login_error_message.setStyleSheet("color: red; font-size: 12px;")
        self.login_error_message.setVisible(False)

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(
            "color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px"
        )
        self.username_input.setFixedHeight(30)
        self.username_input.setFixedWidth(200)
        self.username_input.setTextMargins(10, 0, 10, 0)
        self.login_username_error = QtWidgets.QLabel()
        self.login_username_error.setStyleSheet("color: red; font-size: 12px;")
        self.login_username_error.setVisible(False)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setStyleSheet(
            "color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px"
        )
        self.password_input.setFixedHeight(30)
        self.password_input.setFixedWidth(200)
        self.password_input.setTextMargins(10, 0, 10, 0)
        self.login_password_error = QtWidgets.QLabel()
        self.login_password_error.setStyleSheet("color: red; font-size: 12px;")
        self.login_password_error.setVisible(False)

        login_button = QtWidgets.QPushButton("Log In")
        login_button.setStyleSheet(
            f"background-color: {Colors.PRIMARY}; color: white; border-radius: 10px; margin-top: 20px"
        )
        login_button.setFixedHeight(50)
        login_button.setFixedWidth(200)
        login_button.clicked.connect(self.on_login_submit)

        layout.addWidget(self.login_error_message)
        layout.addWidget(self.username_input)
        layout.addWidget(self.login_username_error)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_password_error)
        layout.addWidget(login_button)

        return widget

    def create_signup_form(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setSpacing(10)

        self.signup_error_message = QtWidgets.QLabel()
        self.signup_error_message.setStyleSheet("color: red; font-size: 12px;")
        self.signup_error_message.setVisible(False)

        self.signup_username_input = QtWidgets.QLineEdit()
        self.signup_username_input.setPlaceholderText("Username")
        self.signup_username_input.setStyleSheet(
            "color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px"
        )
        self.signup_username_input.setFixedHeight(30)
        self.signup_username_input.setFixedWidth(200)
        self.signup_username_input.setTextMargins(10, 0, 10, 0)
        self.signup_username_error = QtWidgets.QLabel()
        self.signup_username_error.setStyleSheet("color: red; font-size: 12px;")
        self.signup_username_error.setVisible(False)

        self.signup_email_input = QtWidgets.QLineEdit()
        self.signup_email_input.setPlaceholderText("Email")
        self.signup_email_input.setStyleSheet(
            "color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px"
        )
        self.signup_email_input.setFixedHeight(30)
        self.signup_email_input.setFixedWidth(200)
        self.signup_email_input.setTextMargins(10, 0, 10, 0)
        self.signup_email_error = QtWidgets.QLabel()
        self.signup_email_error.setStyleSheet("color: red; font-size: 12px;")
        self.signup_email_error.setVisible(False)

        self.signup_password_input = QtWidgets.QLineEdit()
        self.signup_password_input.setPlaceholderText("Password")
        self.signup_password_input.setStyleSheet(
            "color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px"
        )
        self.signup_password_input.setFixedHeight(30)
        self.signup_password_input.setFixedWidth(200)
        self.signup_password_input.setTextMargins(10, 0, 10, 0)
        self.signup_password_error = QtWidgets.QLabel()
        self.signup_password_error.setStyleSheet("color: red; font-size: 12px;")
        self.signup_password_error.setVisible(False)

        signup_button = QtWidgets.QPushButton("Sign Up")
        signup_button.setStyleSheet(
            f"background-color: {Colors.PRIMARY}; color: white; border-radius: 20px; border-radius: 10px; margin-top: 20px;"
        )
        signup_button.setFixedHeight(50)
        signup_button.setFixedWidth(200)
        signup_button.clicked.connect(self.on_signup_submit)

        layout.addWidget(self.signup_error_message)
        layout.addWidget(self.signup_username_input)
        layout.addWidget(self.signup_username_error)
        layout.addWidget(self.signup_email_input)
        layout.addWidget(self.signup_email_error)
        layout.addWidget(self.signup_password_input)
        layout.addWidget(self.signup_password_error)
        layout.addWidget(signup_button)

        self.on_login.connect(self.login)

        return widget

    def switch_tab(self, index):
        if self.stacked_widget.currentIndex() == index:
            return

        if index == 0:  # Login tab
            self.login_btn.setStyleSheet(self.active_style)
            self.signin_btn.setStyleSheet(self.inactive_style)
        else:  # Sign up tab
            self.login_btn.setStyleSheet(self.inactive_style)
            self.signin_btn.setStyleSheet(self.active_style)

        current_geometry = self.stacked_widget.geometry()

        self.stacked_widget.setCurrentIndex(index)

        self.stacked_widget.setGeometry(current_geometry)

    def on_login_submit(self):
        username = self.username_input.text()
        password = self.password_input.text()
        body = {"action": "login", "data": {"username": username, "password": password}}
        self.conn.send_data(body)

    def on_signup_submit(self):
        username = self.signup_username_input.text()
        email = self.signup_email_input.text()
        password = self.signup_password_input.text()
        body = {"action": "sign_up", "data": {"username": username, "email": email, "password": password}}
        self.conn.send_data(body)

    def login(self, data):
        access_token = data.get("data", {}).get("access")
        refresh_token = data.get("data", {}).get("refresh")

        settings = QSettings("Veia Sp.", self.settings_instance)
        settings.setValue("access_token", access_token)
        settings.setValue("refresh_token", refresh_token)

        self.login_successful.emit()
        self.destroy()

    def on_message(self, data):
        if data.get("success"):
            self.on_login.emit(data)

        else:
            errors = data.get("data", {})
            if data.get("action") == "login":
                if errors.get("message"):
                    self.login_error_message.setText(errors.get("message"))
                    self.login_error_message.setVisible(True)
                else:
                    self.login_error_message.setText("")
                    self.login_error_message.setVisible(False)
                if errors.get("username"):
                    self.login_username_error.setText(errors.get("username"))
                    self.login_username_error.setVisible(True)
                else:
                    self.login_username_error.setText("")
                    self.login_username_error.setVisible(False)
                if errors.get("password"):
                    self.login_password_error.setText(errors.get("password"))
                    self.login_password_error.setVisible(True)
                else:
                    self.login_password_error.setText("")
                    self.login_password_error.setVisible(False)
            else:
                if errors.get("message"):
                    self.signup_error_message.setText(errors.get("message"))
                    self.signup_error_message.setVisible(True)
                else:
                    self.signup_error_message.setText("")
                    self.signup_error_message.setVisible(False)
                if errors.get("username"):
                    self.signup_username_error.setText(errors.get("username"))
                    self.signup_username_error.setVisible(True)
                else:
                    self.signup_username_error.setText("")
                    self.signup_username_error.setVisible(False)
                if errors.get("email"):
                    self.signup_email_error.setText(errors.get("email"))
                    self.signup_email_error.setVisible(True)
                else:
                    self.signup_email_error.setText("")
                    self.signup_email_error.setVisible(False)
                if errors.get("password"):
                    self.signup_password_error.setText(errors.get("password"))
                    self.signup_password_error.setVisible(True)
                else:
                    self.signup_password_error.setText(errors.get("password"))
                    self.signup_password_error.setVisible(False)

    def on_connect(self):
        print("connected")

    def on_disconnect(self):
        print("disconnected")

    def closeEvent(self, event) -> None:
        self.conn.stop()
        return super().closeEvent(event)
