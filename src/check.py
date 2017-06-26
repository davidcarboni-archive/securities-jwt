import os
import logging
from flask import request, make_response, redirect
import requests

log = logging.getLogger(__name__)

SIGN_IN_URL = os.getenv("SIGN_IN_URL", "/sign-in/")
log.info("Sign in URL is " + SIGN_IN_URL)


def request_jwt(session_id):
    if session_id:
        response = requests.get("http://auth:5000/token/" + session_id)
        if response.status_code == 200 and response.json():
            log.debug("Retrieved JWT for session " + session_id)
            return response.json().get("token")


def validate_token(jwt):
    # TODO Validate token
    return True


def authorized(f):
    def wrapper():
        log.info(request.headers)

        # Preference order is header, cookie, session ID
        bearer = request.headers.get('Bearer')
        cookie = request.cookies.get('Bearer')
        session = request.cookies.get('Bearer-session')
        if bearer:
            log.debug("Got JWT from Bearer header")
        elif cookie:
            log.debug("Got JWT from cookie")
        elif session:
            log.debug("Got session ID from cookie")

        # Get the token, if available
        jwt = bearer or cookie or request_jwt(session)

        if jwt and validate_token(jwt):
            log.info("Token is: " + jwt)
            return f()
        else:
            log.info("No token identified. Redirecting to " + SIGN_IN_URL)
            response = redirect(SIGN_IN_URL)
            response.set_cookie('service', 'securities')
            return response

    return wrapper
