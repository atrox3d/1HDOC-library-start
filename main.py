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

logger = logging.getLogger(__name__)
get_root_logger()

app = Flask(__name__)

# all_books = []
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title} - {self.author} - {self.rating}>'


db.create_all()


@app.route('/')
@log_decorator
def home():
    return render_template('index.html')


@app.route("/add", methods=["GET", "POST"])
@log_decorator
def add():
    if request.method == "POST":
        # all_books.append(form_dict)
        # logger.info("list all_books")
        # for book in all_books:
        #     logger.info(str(book))
        form_dict = request.form.to_dict()
        logger.info(f"add {form_dict}")
        book = Book(**form_dict)
        logger.info(f'add book: {book}')
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True, host=util.network.get_ipaddress())
