from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")

# Дерекқорды бастапқы ретте жасау
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    # Пайдаланушының аты бар-жоғын тексеру
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"status": "error", "message": "Бұл пайдаланушы аты бұрыннан бар."})

    # Жаңа пайдаланушыны қосу
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Пайдаланушы тіркелді!"})

@app.route('/admin_login', methods=['POST'])
def admin_login():
    role = "admin"
    username = "admin"
    password = "1111"

    # Тексеру үшін статикалық логин мен пароль
    return jsonify({"status": "success", "message": "Админге кіргеніңізді тексеру"}) 
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "role": user.role} for user in users]
    return jsonify({"users": users_list})

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "genre": book.genre} for book in books]
    return jsonify({"books": books_list})

@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')

        # Жаңа кітапты дерекқорға қосу
        new_book = Book(title=title, author=author, genre=genre)
        db.session.add(new_book)
        db.session.commit()

        return jsonify({"status": "success", "message": "Кітап қосылды!"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
