import logging
import b3
import sleuth
import os

from flask import Flask, request, redirect, render_template, jsonify

from auth import check

# App

app = Flask("python", static_folder='static', static_url_path='')

# Logging

debug = bool(os.getenv("FLASK_DEBUG"))
level = logging.DEBUG if debug else logging.WARNING
log = logging.getLogger(__name__)


@app.before_request
def before_request():
    b3.start_span()
    check.authenticated()

app.after_request(b3.end_span)


@app.route('/')
def default():
    log.info("Helper redirect to /securities")
    return redirect("/securities")


@app.route('/securities')
def home():
    log.info("securities home page.")
    return render_template('index.html')


@app.route('/cookie')
def home():
    log.info("Dumping cookie: " + request.cookies)
    return jsonify(request.cookies)


if __name__ == "__main__":

    # Port
    port = os.getenv("PORT", "5000")
    log.info("PORT is " + str(port))
    log.info("FLASK_DEBUG is " + str(debug))

    # Go!
    app.run(
        host="0.0.0.0",
        port=int(port),
        debug=debug,
        threaded=True
    )
