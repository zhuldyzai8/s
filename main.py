import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QAction, QWidget, QPushButton, QHBoxLayout, QStackedWidget, QLineEdit, QDialog,QComboBox,QTableWidget,QTableWidgetItem
from PyQt5 import QtWidgets
from models import db, User  # Импортируем все необходимые модели
from gui import AdminLoginWindow
import requests

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("Book Tracker")
        self.setGeometry(0, 0, 1820, 980)
        self.setStyleSheet("background-color: #f9f8f2;")

        # Логотип
        self.logo_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\User\\Desktop\\book_tracker\\images\\nook.jpg")
        scaled_pixmap = pixmap.scaled(900, 900, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Приветствие
        greeting_label = QLabel("Добро пожаловать в Book Tracker! Начни отслеживать свои книги.")
        greeting_label.setFont(QFont("Arial", 16))
        greeting_label.setAlignment(Qt.AlignCenter)

        # Установка начального макета
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(greeting_label)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Таймер для показа основного интерфейса через 3 секунды
        QTimer.singleShot(3000, self.show_main_interface)
    
    def create_bottom_navigation(self):
        # Нижнее меню
        bottom_layout = QHBoxLayout()
        btn_home = QPushButton("Главная")
        btn_books = QPushButton("Мои книги")
        btn_account = QPushButton("Мой аккаунт")
        btn_history = QPushButton("История чтения")

        # Связывание кнопок с соответствующими страницами
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        btn_books.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.books_page))
        btn_account.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.account_page))
        btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.history_page))

        # Добавление кнопок в нижнее меню
        bottom_layout.addWidget(btn_home)
        bottom_layout.addWidget(btn_books)
        bottom_layout.addWidget(btn_history)
        bottom_layout.addWidget(btn_account)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(bottom_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Стиль для нижнего меню и кнопок
        bottom_widget.setStyleSheet("background-color: #f9f8f2; border-top: 2px solid #ccc;")
        for button in [btn_home, btn_books, btn_account, btn_history]:
            button.setStyleSheet(""" 
                QPushButton {
                    background-color: #999900;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 16px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #b3b300;
                }
                QPushButton:pressed {
                    background-color: #808000;
                }
            """)

    def show_main_interface(self):
        # Это уже не нужно создавать новое окно main_interface, используем текущее.
        self.stacked_widget = QStackedWidget()

        # Страницы
        self.home_page = self.create_home_page()
        self.books_page = self.create_books_page()
        self.account_page = self.create_account_page()
        self.history_page = self.create_history_page()

        # Добавление страниц в StackedWidget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.books_page)
        self.stacked_widget.addWidget(self.account_page)
        self.stacked_widget.addWidget(self.history_page)

        # Нижнее меню навигации
        self.create_bottom_navigation()

        # Показ главного интерфейса
        self.show()

    def create_books_page(self):
        books_page = QWidget()
        label = QLabel("Мои книги", books_page)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        books_page.setLayout(layout)
        return books_page

    def create_account_page(self):
        account_page = QWidget()
        layout = QVBoxLayout()

       # Заголовок страницы
        label = QLabel("Мой аккаунт", account_page)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    # Кнопка для открытия окна входа
        login_button = QPushButton("Войти", self)
        login_button.setStyleSheet("background-color: #999900; color: white; font-size: 16px; border-radius: 5px;")
        login_button.clicked.connect(self.open_login_form)

        # Добавляем кнопку в лейаут
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        account_page.setLayout(layout)
        return account_page


    def create_history_page(self):
        history_page = QWidget()
        label = QLabel("История чтения", history_page)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        history_page.setLayout(layout)
        return history_page
    def open_login_form(self):
     login_form = LoginWindow(self)  # Жаңа форма құру
     login_form.show()  # Модальді түрде ашу

    def create_home_page(self):
        # Главная страница с поиском и рекомендациями
        home_page = QWidget()
        main_layout = QVBoxLayout()

        # Поле поиска
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск книг по названию, автору или жанру")
        search_input.setFixedSize(300, 40)
        search_button = QPushButton("Поиск")
        search_button.setFixedSize(100, 40)
        search_button.setStyleSheet("background-color: #999900; color: #fff; padding: 8px;")
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # Рекомендуемые книги
        recommended_label = QLabel("Рекомендуемые книги")
        recommended_label.setFont(QFont("Arial", 14))
        recommended_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(recommended_label)

        # Пример кнопок для рекомендованных книг
        recommended_books_layout = QHBoxLayout()
        for i in range(3):
            book_button = QPushButton(f"Книга {i + 1}")
            book_button.setStyleSheet("background-color: #999900; color: #fff; padding: 8px;")
            recommended_books_layout.addWidget(book_button)
        main_layout.addLayout(recommended_books_layout)

        # Кнопка перехода в "Мои книги"
        my_books_button = QPushButton("Перейти в Мои книги")
        my_books_button.setFont(QFont("Arial", 12))
        my_books_button.setStyleSheet("background-color: #999900; color: #fff; padding: 10px;")
        my_books_button.setFixedSize(200, 50)
        my_books_button.setCursor(Qt.PointingHandCursor)
        my_books_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.books_page))
        main_layout.addWidget(my_books_button, alignment=Qt.AlignCenter)

        home_page.setLayout(main_layout)
        return home_page


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Вход')
        self.setGeometry(100, 100, 400, 200)

        # Создаем виджеты
        self.role_label = QLabel("Роль:", self)
        self.role_input = QComboBox(self)
        self.role_input.addItems(["admin", "user"]) 

        self.username_label = QLabel("Имя пользователя:", self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Пароль:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Прячем введенный пароль

        self.login_button = QPushButton('Войти', self)
        self.register_button = QPushButton('Регистрация', self)

        # Настройка макета
        layout = QVBoxLayout()
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        # Создаем центральный виджет и устанавливаем его в окно
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем кнопки к методам
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.open_register_form)

    def login(self):
        role = self.role_input.currentText()
        username = self.username_input.text()
        password = self.password_input.text()

    def check_credentials(self):
        role = self.role_input.currentText()
        username = self.username_input.text()
        password = self.password_input.text()

        # Егер логин және пароль дұрыс болса
        if role=="admin" and username == "admin" and password == "1111":  # Бұл жерде тексеру оңай түрде берілген
            self.open_admin_gui()

    def open_admin_gui(self):
        self.admin_gui = AdminLoginWindow()  # AdminLoginWindow терезесін ашады
        self.admin_gui.show()  # Admin GUI терезесін көрсету
        self.close()  # Логин терезесін жабу


    def open_register_form(self):
        self.register_form = RegisterWindow(self)  # Создаем объект окна регистрации
        self.register_form.show()  # Отображаем окно регистрации
        
class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Регистрация')
        self.setGeometry(100, 100, 400, 200)

        # Виджеты для ввода данных
        self.role_label = QLabel("Роль:", self)
        self.role_input = QComboBox(self)
        self.role_input.addItems(["admin", "user"])

        self.username_label = QLabel("Имя пользователя:", self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Пароль:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)


        self.register_button = QPushButton('Зарегистрироваться', self)

        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_input)
        layout.addWidget(self.register_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем кнопку регистрации
        self.register_button.clicked.connect(self.register)

    def register(self):
        role = self.role_input.currentText()  # Получаем выбранную рол
        username = self.username_input.text()
        password = self.password_input.text()

        # Добавление пользователя в базу данных
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        print(f"Пользователь {username} зарегистрирован как {role}")
        self.close() 

class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кітаптар тізімі")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Кітаптар тізімін көрсету үшін кесте
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        # Кітаптар тізімін жаңарту үшін батырма
        self.refreshButton = QPushButton("Кітаптар тізімін жаңарту")
        self.refreshButton.clicked.connect(self.refresh_books)
        self.layout.addWidget(self.refreshButton)

        self.setLayout(self.layout)

    def refresh_books(self):
    # Flask серверінен кітаптар тізімін алу
           response = requests.get("http://127.0.0.1:5000/books")
           data = response.json()  # Парсинг JSON
           self.tableWidget.setRowCount(len(data))  # Қатар санын өзгерту
           for row, book in enumerate(data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(book['title']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(book['author']))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(book['genre']))

      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())