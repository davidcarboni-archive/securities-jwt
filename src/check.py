import logging

import os
import requests
from flask import request, redirect

from src import Keys, Token

log = logging.getLogger(__name__)

SIGN_IN_URL = os.getenv("SIGN_IN_URL", "/sign-in")
TOKEN_URL = os.getenv("TOKEN_URL", "http://auth:5000/token")
COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', None)
log.info("Sign in URL is " + SIGN_IN_URL)


def authorized():
    # Preference order is header, cookie, session ID
    token = _get_header_token() or _get_cookie_token()
    log.debug("Token is " + str(token))
    if not Token.verify(token, Keys.list_public_keys()):
        response = redirect(SIGN_IN_URL)
        response.set_cookie("service", "securities", domain=COOKIE_DOMAIN)
        #return response


def _get_header_token():
    authorization = request.headers.get('Authorization')
    if authorization:
        parts = authorization.split(" ")
        if len(parts) == 2 and parts[0] == "Bearer":
            log.debug("Token from header is: " + parts[1])
            return parts[1]


def _get_cookie_token():
    session_id = request.cookies.get('jwt-session')
    if session_id:
        url = TOKEN_URL.strip("/") + "/" + session_id
        log.debug("Getting token from: " + url)
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            log.debug("Retrieved JWT for session " + session_id)
            return response.json().get("token")
        #TODO: catch any errors
