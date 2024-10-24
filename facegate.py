from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QFileDialog, QMessageBox
import sys, os, json, psutil, threading, time
from proc_block import MainWindow
from detect_face import encode_faces, detect_faces
from PyQt6.QtGui import QMovie

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Основной стек для смены лейаутов
        self.stacked_layout = QStackedLayout()

        # Инициализация экранов
        self.init_login_ui()      # Экран авторизации
        self.init_registration_ui()  # Экран регистрации

        # Настройка окна
        self.setWindowTitle('Face Gate')
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
        button_layout = QVBoxLayout()
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

        # Подключаем кнопку GateID к распознаванию лиц
        gate_id_button.clicked.connect(self.gateid_login_user)

    # Функция логина
    def login_user(self):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
            if users != None:
                if self.login_input.text() != '' and self.password_input.text() != '' and users[self.login_input.text()] == self.password_input.text():
                    with open("current_user.json", "w") as f:
                        json.dump(self.login_input.text(), f)
                    mainWindow = MainWindow()
                    self.close()
                    stop_event.set()
                    thread.join()
                    mainWindow.show()
                else:
                    print("no same entries")
            else:
                print("no entries")
        except json.decoder.JSONDecodeError:
            print("err")

    #Функция логина по GateID
    def gateid_login_user(self):
        self.stacked_layout.setCurrentIndex(2)
        encode_faces()
        name = detect_faces()
        with open("current_user.json", "w") as f:
            json.dump(name, f)
        if name:
            mainWindow = MainWindow()
            self.close()
            stop_event.set()
            thread.join()
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
        button_layout = QVBoxLayout()
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

        mainWindow = MainWindow()
        with open("current_user.json", "w") as f:
            f.write(self.username_input.text())
        self.close()
        mainWindow.show()
        
    def load_processes_to_block(self):
        """Читает список процессов из procs.json"""
        try:
            with open('procs.json', 'r') as f:
                processes_to_block = json.load(f)
            return processes_to_block
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл procs.json не найден или поврежден.")
            return []
        
    def block_processes(self, processes_to_block):
        """Завершает процессы с именами, которые есть в списке"""
        for proc in psutil.process_iter(['name']):
            try:
                # Получаем имя процесса
                proc_name = proc.info['name']
                # Если процесс есть в списке для блокировки
                if proc_name in processes_to_block:
                    print(f"Завершаем процесс: {proc_name} (PID: {proc.pid})")
                    proc.terminate()  # Посылаем сигнал на завершение
                    proc.wait(timeout=3)  # Ожидаем завершение процесса
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def infinite_block(self, stop_event):
        processes_to_block = self.load_processes_to_block()
        if processes_to_block:
            # Завершаем процессы
            while not stop_event.is_set():
                self.block_processes(processes_to_block)
                time.sleep(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    stop_event = threading.Event()
    thread = threading.Thread(target=window.infinite_block, args=(stop_event,))
    thread.start()
    sys.exit(app.exec())