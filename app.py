import os
import logging
from flask import Flask, request, render_template, jsonify
from src import check


# Logging

debug = bool(os.getenv("FLASK_DEBUG"))
logging_level = logging.DEBUG if debug else logging.WARNING
logging.basicConfig(level=logging_level)
log = logging.getLogger(__name__)


# App

app = Flask("python", static_folder='static', static_url_path='')


@app.route('/')
@check.authorized
def default():
    return render_template('index.html')


if __name__ == "__main__":
    log.info("FLASK_DEBUG is " + str(debug))
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=debug,
        threaded=True
    )
