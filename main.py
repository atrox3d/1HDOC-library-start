from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
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

all_books = []


@app.route('/')
@log_decorator
def home():
    return render_template('index.html')


@app.route("/add", methods=["GET", "POST"])
@log_decorator
def add():
    logger.info(request.form)
    logger.info(request.method)
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        logger.info(f"{title}, {author}, {rating}")
        all_books.append(dict(title=title, author=author, rating=rating))
        for book in all_books:
            logger.info(str(book))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True, host=util.network.get_ipaddress())
