from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QFileDialog
import sys, os, json
from proc_block import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Основной стек для смены лейаутов
        self.stacked_layout = QStackedLayout()

        # Инициализация экранов
        self.init_login_ui()      # Экран авторизации
        self.init_registration_ui()  # Экран регистрации

        # Настройка окна
        self.setWindowTitle('Окно авторизации')
        self.setGeometry(100, 100, 300, 200)
        self.setLayout(self.stacked_layout)

    # Экран авторизации
    def init_login_ui(self):
        # Лейаут для авторизации
        login_layout = QVBoxLayout()

        # Метка для логина
        login_label = QLabel('Username:')
        self.login_input = QLineEdit()

        # Метка для пароля
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопки
        login_button = QPushButton('Login')
        gate_id_button = QPushButton('Gate ID')
        register_button = QPushButton('Register')

        # Макет для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(gate_id_button)
        button_layout.addWidget(register_button)

        # Добавляем виджеты в лейаут
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addLayout(button_layout)

        # Создаем виджет для экрана авторизации
        login_widget = QWidget()
        login_widget.setLayout(login_layout)

        # Добавляем виджет в стек
        self.stacked_layout.addWidget(login_widget)

        # Подключаем кнопку регистрации для смены лейаута
        register_button.clicked.connect(self.switch_to_registration)
        login_button.clicked.connect(self.login_user)

    def login_user(self):
        mainWindow = MainWindow()
        self.close()
        mainWindow.show()

    # Экран регистрации
    def init_registration_ui(self):
        # Лейаут для регистрации
        registration_layout = QVBoxLayout()

        # Поля для ввода username, пароля и повторения пароля
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        password_label = QLabel('Password:')
        self.password_input_reg = QLineEdit()
        self.password_input_reg.setEchoMode(QLineEdit.EchoMode.Password)

        repeat_password_label = QLabel('Repeat password:')
        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопка для импорта профиля
        import_profile_button = QPushButton('Import profile')
        import_profile_button.clicked.connect(self.import_profile)

        # Кнопка регистрации
        register_button_reg = QPushButton('Register')
        register_button_reg.clicked.connect(self.register)

        # Макет для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(import_profile_button)
        button_layout.addWidget(register_button_reg)

        # Добавляем виджеты в лейаут
        registration_layout.addWidget(username_label)
        registration_layout.addWidget(self.username_input)
        registration_layout.addWidget(password_label)
        registration_layout.addWidget(self.password_input_reg)
        registration_layout.addWidget(repeat_password_label)
        registration_layout.addWidget(self.repeat_password_input)
        registration_layout.addLayout(button_layout)

        # Создаем виджет для экрана регистрации
        registration_widget = QWidget()
        registration_widget.setLayout(registration_layout)

        # Добавляем виджет в стек
        self.stacked_layout.addWidget(registration_widget)

    # Переключение на экран регистрации
    def switch_to_registration(self):
        self.stacked_layout.setCurrentIndex(1)

    # Метод для импорта профиля
    def import_profile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберите файл профиля', '', 'Profile Files (*.json *.xml)')
        if file_name:
            print(f"Импорт профиля из: {file_name}")

    # Метод для создания лейаута-заглушки
    def create_placeholder_layout(self):
        placeholder_layout = QVBoxLayout()
        placeholder_label = QLabel('Пользователь зарегистрирован. Это заглушка.')
        placeholder_layout.addWidget(placeholder_label)

        placeholder_widget = QWidget()
        placeholder_widget.setLayout(placeholder_layout)
        
        return placeholder_widget

    # Метод для регистрации
    def register(self):
        username = self.username_input.text().strip()  # Убираем пробелы по краям
        password = self.password_input_reg.text().strip()
        repeat_password = self.repeat_password_input.text().strip()

        # Проверка на пустой логин и пароль
        if not username:
            print("Логин не может быть пустым!")
            return
        if not password:
            print("Пароль не может быть пустым!")
            return
        if password != repeat_password:
            print("Пароли не совпадают!")
            return

        # Проверка, существует ли файл users.json
        if os.path.exists('users.json') and os.path.getsize('users.json') > 0:
            with open('users.json', 'r') as file:
                try:
                    users = json.load(file)  # Читаем данные, если файл корректный
                except json.JSONDecodeError:
                    users = {}  # Если файл пуст или поврежден, создаем новый словарь
        else:
            users = {}

        # Проверка на уникальность логина
        if username in users:
            print("Пользователь с таким логином уже существует!")
            return

        # Добавление нового пользователя
        users[username] = password

        # Запись в файл users.json
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)

        # Получаем виджет с лейаутом-заглушкой
        placeholder_widget = self.create_placeholder_layout()

        # Добавляем заглушку в стек и устанавливаем ее активной
        self.stacked_layout.addWidget(placeholder_widget)
        self.stacked_layout.setCurrentWidget(placeholder_widget)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
