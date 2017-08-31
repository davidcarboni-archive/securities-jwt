import logging
import b3
import sleuth
import os

from flask import Flask, request, redirect, render_template, jsonify

from auth import check


# Config

debug = bool(os.getenv("FLASK_DEBUG")) or True
COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', None)


# Logging

logging.getLogger().setLevel(logging.DEBUG if debug else logging.WARNING)
log = logging.getLogger(__name__)

# App

app = Flask("python", static_folder='static', static_url_path='')
app.before_request(b3.start_span)
app.before_request(check.authorized)
app.after_request(b3.end_span)


@app.route('/')
def default():
    log.info("Helper redirect to /securities")
    return redirect("/securities")


@app.route('/securities')
def home():
    log.info("securities home page.")
    return render_template('index.html',
                           sign_in_url=service_url('sign-in'),
                           sign_out_url=service_url('sign-out'),
                           discharges_url=service_url('discharges'),
                           securities_url=service_url('securities'),
                           dispositions_url=service_url('dispositions'),
                           cookie_domain=COOKIE_DOMAIN)


@app.route('/cookie')
def cookie():
    log.info("Dumping cookie: " + request.cookies)
    return jsonify(request.cookies)


@app.route('/sign-in')
def unauthorised():
    return "Not authorised, dude."


def service_url(service):
    if service == 'sign-in':
        return os.getenv("SIGN_IN_URL", "/sign-in")
    elif service == 'sign-out':
        return os.getenv("SIGN_OUT_URL", "/sign-out")
    elif service == 'discharges':
        return os.getenv("DISCHARGES_URL", "/discharges")
    elif service == 'securities':
        return os.getenv("SECURITIES_URL", "/securities")
    elif service == 'dispositions':
        return os.getenv("DISPOSITIONS_URL", "/dispositions")


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
