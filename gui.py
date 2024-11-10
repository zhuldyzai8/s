import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout,QStackedWidget,QLineEdit
from PyQt5.QtCore import Qt


class AdminLoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Admin Login')
        self.setGeometry(0, 0, 1820, 980)

        # Вход и другие элементы для логина (например, текстовые поля, кнопки) можно добавить сюда, если нужно

        # Здесь сразу откроется главный интерфейс
        self.main_interface()

    def bottom_navigation(self):
        # Нижнее меню
        bottom_layout = QHBoxLayout()
        btn_kold = QPushButton("Қолданушылар")
        btn_kitap = QPushButton("Кітаптар")
        btn_otzyv = QPushButton("Пікірлер")

        # Связывание кнопок с соответствующими страницами
        btn_kold.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.kold_page))
        btn_kitap.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.kitap_page))
        btn_otzyv.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.otzyv_page))

        # Добавление кнопок в нижнее меню
        bottom_layout.addWidget(btn_kold)
        bottom_layout.addWidget(btn_kitap)
        bottom_layout.addWidget(btn_otzyv)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)

        # Стиль для нижнего меню и кнопок
        bottom_widget.setStyleSheet("background-color: #f9f8f2; border-top: 2px solid #ccc;")
        for button in [btn_kold, btn_kitap, btn_otzyv]:
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

        return bottom_widget

    def main_interface(self):
        # Основной интерфейс
        self.stacked_widget = QStackedWidget()

        # Страницы
        self.kold_page = self.create_kold_page()
        self.kitap_page = self.create_kitap_page()
        self.otzyv_page = self.create_otzyv_page()

        # Добавление страниц в StackedWidget
        self.stacked_widget.addWidget(self.kold_page)
        self.stacked_widget.addWidget(self.kitap_page)
        self.stacked_widget.addWidget(self.otzyv_page)

        # Нижнее меню навигации
        bottom_widget = self.bottom_navigation()

        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(bottom_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_kold_page(self):
        kold_page = QWidget()

        # Create table widget for users
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Username', 'Role'])

        # Fetch users from the API
        self.fetch_users()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        kold_page.setLayout(layout)
        return kold_page

    def fetch_users(self):
        # Send GET request to fetch users from Flask API
        try:
            response = requests.get('http://localhost:5000/get_users')
            if response.status_code == 200:
                users = response.json()
                self.update_user_table(users)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching users: {e}")

    def update_user_table(self, users):
        # Update the table with user data
        self.table_widget.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(user['username']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(user['role']))

    def create_kitap_page(self):
        kitap_page = QWidget()
        label = QLabel("Книги", kitap_page)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        kitap_page.setLayout(layout)
        return kitap_page

    def create_otzyv_page(self):
        otzyv_page = QWidget()
        label = QLabel("Отзывы", otzyv_page)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        otzyv_page.setLayout(layout)
        return otzyv_page
class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пайдаланушылар тізімі")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Пайдаланушылар тізімін көрсету үшін кесте
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        # Пайдаланушыларды алу үшін батырма
        self.refreshButton = QPushButton("Пайдаланушыларды жаңарту")
        self.refreshButton.clicked.connect(self.refresh_users)
        self.layout.addWidget(self.refreshButton)

        self.setLayout(self.layout)

    def refresh_users(self):
        # Flask серверіне сұраныс жіберу
        try:
            response = requests.get("http://127.0.0.1:5000/users")
            data = response.json()
            users = data.get('users', [])

            # Кестені жаңарту
            self.tableWidget.setRowCount(len(users))
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Аты", "Рөлі"])

            for row, user in enumerate(users):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(user['id'])))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(user['username']))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(user['role']))

        except requests.exceptions.RequestException as e:
            print(f"Қате орын алды: {e}")

class BookWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кітаптарды енгізу")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Кітаптарды көрсету үшін кесте
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        # Кітап қосу үшін мәтін өрістері
        self.titleInput = QLineEdit(self)
        self.titleInput.setPlaceholderText("Кітаптың атауы")
        self.layout.addWidget(self.titleInput)

        self.authorInput = QLineEdit(self)
        self.authorInput.setPlaceholderText("Автор")
        self.layout.addWidget(self.authorInput)

        self.genreInput = QLineEdit(self)
        self.genreInput.setPlaceholderText("Жанры")
        self.layout.addWidget(self.genreInput)

        # Кітапты қосу үшін батырма
        self.addBookButton = QPushButton("Кітап қосу")
        self.addBookButton.clicked.connect(self.add_book)
        self.layout.addWidget(self.addBookButton)

        # Пайдаланушылар тізімін жаңарту үшін батырма
        self.refreshButton = QPushButton("Кітаптар тізімін жаңарту")
        self.refreshButton.clicked.connect(self.refresh_books)
        self.layout.addWidget(self.refreshButton)

        self.setLayout(self.layout)
        self.refresh_books()  # Қосылғанда автоматты түрде жаңарту

    def add_book(self):
        # Flask серверіне кітап қосу үшін сұраныс
        title = self.titleInput.text()
        author = self.authorInput.text()
        genre = self.genreInput.text()

        if not title or not author or not genre:
            print("Барлық өрістерді толтырыңыз")
            return

        book_data = {"title": title, "author": author, "genre": genre}

        try:
            response = requests.post("http://127.0.0.1:5000/add_book", json=book_data)
            data = response.json()
            if data['status'] == 'success':
                print(data["message"])
                self.refresh_books()  # Кітап қосылғаннан кейін жаңарту
                self.titleInput.clear()
                self.authorInput.clear()
                self.genreInput.clear()
            else:
                print("Кітап қосу сәтсіз аяқталды")
        except requests.exceptions.RequestException as e:
            print(f"Қате орын алды: {e}")

    def refresh_books(self):
        # Flask серверінен кітаптар тізімін алу
        try:
            response = requests.get("http://127.0.0.1:5000/books")
            data = response.json()
            books = data.get('books', [])

            self.tableWidget.setRowCount(len(books))
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Атауы", "Автор", "Жанры"])

            for row, book in enumerate(books):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(book['id'])))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(book['title']))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(book['author']))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(book['genre']))

        except requests.exceptions.RequestException as e:
            print(f"Қате орын алды: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminLoginWindow()
    window.show()
    sys.exit(app.exec_())
