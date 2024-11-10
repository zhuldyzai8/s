from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Настройка приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_tracker.db'  # Используем SQLite для тестов
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели

# Модель для пользователя с ролью
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user") 

    def __repr__(self):
        return f'<User {self.username}>'

# Модель для книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    description = db.Column(db.Text)
    total_pages = db.Column(db.Integer)
    file_url = db.Column(db.String(200))

    admin = db.relationship('User', backref='added_books')

# Модель для связи пользователя с книгой
class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  # Келесі кестеге сілтеме
    downloaded = db.Column(db.Boolean, default=False)
    progress = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='Читаю')

# Модель для отзывов
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Модель для истории чтения
class ReadingHistory(db.Model):
    __tablename__ = 'reading_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    pages_read = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с пользователем и книгой
    user = db.relationship('User', backref='reading_history')
    book = db.relationship('Book', backref='reading_history')

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание всех таблиц в базе данных
    app.run(debug=True)
