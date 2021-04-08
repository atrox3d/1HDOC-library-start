from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Request,
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
    form_dict = request.form.to_dict()
    logger.info(f"add {form_dict}")
    if request.method == "POST":
        all_books.append(form_dict)
        logger.info("list all_books")
        for book in all_books:
            logger.info(str(book))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True, host=util.network.get_ipaddress())
