"""
|||||||||||||||||||||||||
|СЕРТИФИЦИРОВАННАЯ СВАГА|
|ВЫДАНО: НАЗАРКИНУ Р.Д. |
|||||||||||||||||||||||||

SSSSSSSSS      WWW           WWW         AAA            GGGGGG
SSS            WWW           WWW      AAA   AAA      GGG      GGG
SSS            WWW           WWW      AAA   AAA      GGG
SSSSSSSSS      WWW           WWW      AAA   AAA      GGG
      SSS      WWW    WWW    WWW      AAAAAAAAA      GGG   GGGGG
      SSS      WWW    WWW    WWW      AAA   AAA      GGG      GGG
      SSS       WWW   WWW   WWW       AAA   AAA      GGG      GGG
SSSSSSSSS        WWWWWW WWWWWW        AAA   AAA         GGGGGG

"""

import sys, json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QMainWindow
from PyQt6.QtGui import QIcon, QFont
from facegate import FaceGate
from loginlayout import Login

class User:
    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

    def create_user(self):
        with open("credentials.json", "w") as f:
            data = {"login": self.login, "password": self.password, "email": self.email}
            json.dump(data, f)
            print("Пользователь успешно создан!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример входа")
        self.setGeometry(50, 50, 500, 500)
        self.setWindowIcon(QIcon('icon.png')) # Замените icon.png на путь к вашему иконтеку
        self.setStyleSheet("background-color: #00c77b")
        loginWidget = QWidget()
        login = Login()
        loginLayout = login.layout()
        loginWidget.setLayout(loginLayout)
        self.setCentralWidget(loginWidget)

class Login():
        def layout():
            l = Login()
            buttonParams = """
                        background-color: #b3e6d5;
                        border-style: outset;
                        border-width: 1px;
                        border-radius: 15px;
                        border-color: transparent;
                        padding: 4px;
                    """
            label_login = QLabel("Логин")
            line_edit_login = QLineEdit()
            label_login.setStyleSheet("color: #b3e6d5")

            label_password = QLabel("Пароль")
            label_password.setStyleSheet("color: #b3e6d5")
            line_edit_password = QLineEdit()
            line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)

            checkBoxShowPassword = QCheckBox("Показать пароль")
            checkBoxShowPassword.stateChanged.connect(l.toggle_password_visibility())

            button_base_login = QPushButton("Войти по паролю")
            button_base_login.clicked.connect(l.on_enter_password)
            button_base_login.setStyleSheet(buttonParams)

            button_enter_facegate = QPushButton("Войти по GateID")
            button_enter_facegate.clicked.connect(l.on_enter_facegate)
            button_enter_facegate.setStyleSheet(buttonParams)

            button_register_user = QPushButton("Регистрация")
            button_register_user.clicked.connect(l.on_register_user)
            button_register_user.setStyleSheet(buttonParams)

            button_forgot_password = QPushButton("Забыли пароль?")
            button_forgot_password.clicked.connect(l.on_forgot_password)
            button_forgot_password.setStyleSheet(buttonParams)

            Layout = QVBoxLayout()
            Layout.addWidget(label_login)
            Layout.addWidget(line_edit_login)
            Layout.addWidget(label_password)
            Layout.addWidget(line_edit_password)
            Layout.addWidget(checkBoxShowPassword)
            Layout.addWidget(button_base_login)
            Layout.addWidget(button_enter_facegate)
            Layout.addWidget(button_register_user)
            Layout.addWidget(button_forgot_password)
            return Layout

        def on_enter_password():
            print("Вы нажали кнопку 'Войти по паролю'")
                
        def on_enter_facegate():
            print("Вы нажали кнопку 'Войти по FaceGate'")

        def on_forgot_password():
            print("Вы нажали кнопку 'Забыли пароль?'")

        def on_register_user():
            print("Регистрация")

        def toggle_password_visibility(state):
            l = Login()
            if state == 2:
                l.line_edit_password.setEchoMode(QLineEdit.EchoMode.Normal)
            else:
                l.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())