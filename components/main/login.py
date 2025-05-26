from PySide6 import QtWidgets
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt

from lib.conn import Conn
from styles import Colors


class Login(QtWidgets.QMainWindow):
    def __init__(self, host, port, parent=None):
        super().__init__(parent=parent)

        self.conn = Conn(host, port)
        self.conn.connected_callback = self.on_connect
        self.conn.disconnected_callback = self.on_disconnect

        self.setStyleSheet("""
            QMainWindow{ background-color: #262624; color: #ffffff; }
        """)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(10)

        tab_container = QtWidgets.QFrame()
        tab_container.setFixedHeight(30)
        tab_container.setFixedWidth(200)
        tab_container.setStyleSheet("border-radius: 10px; border: 1px solid grey ")

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

        self.main_layout.addWidget(tab_container)

        self.stacked_widget = QtWidgets.QStackedWidget()

        login_widget = self.create_login_form()
        self.stacked_widget.addWidget(login_widget)

        # Sign up form
        signup_widget = self.create_signup_form()
        self.stacked_widget.addWidget(signup_widget)

        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addStretch()

        self.slide_animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.conn.start()

    def create_login_form(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        title = QtWidgets.QLabel("Veia")
        title.setFixedHeight(50)
        title.setFixedWidth(200)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: white; text-align: center")

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px")
        self.username_input.setFixedHeight(30)
        self.username_input.setFixedWidth(200)
        self.username_input.setTextMargins(10, 0, 10, 0)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setStyleSheet("color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px")
        self.password_input.setFixedHeight(30)
        self.password_input.setFixedWidth(200)
        self.password_input.setTextMargins(10, 0, 10, 0)

        login_button = QtWidgets.QPushButton("Log In")
        login_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: white; border-radius: 10px")
        login_button.setFixedHeight(30)
        login_button.setFixedWidth(200)
        login_button.clicked.connect(self.on_login_submit)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        return widget

    def create_signup_form(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        title = QtWidgets.QLabel("Veia")
        title.setFixedHeight(50)
        title.setFixedWidth(200)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; color: white; text-align: center")

        self.signup_username_input = QtWidgets.QLineEdit()
        self.signup_username_input.setPlaceholderText("Username")
        self.signup_username_input.setStyleSheet("color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px")
        self.signup_username_input.setFixedHeight(30)
        self.signup_username_input.setFixedWidth(200)
        self.signup_username_input.setTextMargins(10, 0, 10, 0)

        self.signup_email_input = QtWidgets.QLineEdit()
        self.signup_email_input.setPlaceholderText("Email")
        self.signup_email_input.setStyleSheet("color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px")
        self.signup_email_input.setFixedHeight(30)
        self.signup_email_input.setFixedWidth(200)
        self.signup_email_input.setTextMargins(10, 0, 10, 0)

        self.signup_password_input = QtWidgets.QLineEdit()
        self.signup_password_input.setPlaceholderText("Password")
        self.signup_password_input.setStyleSheet("color: white; background-color: #262626; border: 1px solid grey; border-radius: 10px")
        self.signup_password_input.setFixedHeight(30)
        self.signup_password_input.setFixedWidth(200)
        self.signup_password_input.setTextMargins(10, 0, 10, 0)

        signup_button = QtWidgets.QPushButton("Sign Up")
        signup_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: white; border-radius: 20px; border-radius: 10px")
        signup_button.setFixedHeight(30)
        signup_button.setFixedWidth(200)
        signup_button.clicked.connect(self.on_signup_submit)

        layout.addWidget(title)
        layout.addWidget(self.signup_username_input)
        layout.addWidget(self.signup_email_input)
        layout.addWidget(self.signup_password_input)
        layout.addWidget(signup_button)

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

        if index > self.stacked_widget.currentIndex():
            # Slide left
            start_geometry = QRect(current_geometry.x() + current_geometry.width(),
                                 current_geometry.y(),
                                 current_geometry.width(),
                                 current_geometry.height())
        else:
            start_geometry = QRect(current_geometry.x() - current_geometry.width(),
                                 current_geometry.y(),
                                 current_geometry.width(),
                                 current_geometry.height())

        self.stacked_widget.setCurrentIndex(index)

        self.stacked_widget.setGeometry(start_geometry)

        self.slide_animation.setStartValue(start_geometry)
        self.slide_animation.setEndValue(current_geometry)
        self.slide_animation.start()

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

    def on_connect(self):
        print("connected")

    def on_disconnect(self):
        print("disconnected")

    def closeEvent(self, event) -> None:
        self.conn.stop()
        return super().closeEvent(event)
