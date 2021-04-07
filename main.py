from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
import util.network
import util.params
from util.logging import(
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
    pass


@app.route("/add")
@log_decorator
def add():
    pass


if __name__ == "__main__":
    app.run(debug=True, host=util.network.get_ipaddress())

