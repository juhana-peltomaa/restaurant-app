from os import getenv
from flask import Flask
from extensions import csrf


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

csrf.init_app(app)

import routes  # nopep8


if __name__ == "__main__":
    app.run()
