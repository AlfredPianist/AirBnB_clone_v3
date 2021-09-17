#!/usr/bin/python3
"""The controller for the api"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST') if not None else '0.0.0.0'
    HBNB_MYSQL_PORT = getenv('HBNB_MYSQL_PORT') if not None else '5000'

    app.run(host=HBNB_MYSQL_HOST,
            port=HBNB_MYSQL_PORT,
            threaded=True,
            debug=True)
