from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Request,
)
from flask_sqlalchemy import SQLAlchemy

import util.network
import util.params
from util.logging import (
    get_root_logger,
    log_decorator
)
import logging

LOGGER = logging.getLogger(__name__)
get_root_logger()

LOGGER.info("create app")
app = Flask(__name__)

LOGGER.info("config SQLAlchemy")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

LOGGER.info("define Book class")
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title} - {self.author} - {self.rating}>'


LOGGER.info("create db")
db.create_all()


def add_book(form_dict):
    book = Book(**form_dict)
    LOGGER.info(f'add book: {book}')
    db.session.add(book)
    LOGGER.info("update db")
    db.session.commit()
    LOGGER.info("redirect to home")


@log_decorator
def get_all_books():
    return db.session.query(Book).all()


@log_decorator
def update_rating(book, rating):
    book.rating = rating
    db.session.commit()


@app.route('/')
@log_decorator
def home():
    books = get_all_books()
    return render_template('index.html', books=books)


@app.route("/add", methods=["GET", "POST"])
@log_decorator
def add():
    if request.method == "POST":
        form_dict = request.form.to_dict()
        LOGGER.info(f"form dict: {form_dict}")
        add_book(form_dict)
        return redirect(url_for('home'))
    else:
        LOGGER.info('render add')
        return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@log_decorator
def edit_rating(id):
    book = Book.query.get(id)
    if request.method == 'GET':
        return render_template('edit.html', book=book)
    else:
        LOGGER.info(f"selected book={book}")
        rating = request.form["rating"]
        LOGGER.info(f"new rating: '{rating}'")
        if rating:
            update_rating(book, rating)
        return redirect(url_for('home'))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@log_decorator
def delete(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, host=util.network.get_ipaddress())
