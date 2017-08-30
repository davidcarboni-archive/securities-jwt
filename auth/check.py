import logging

import os
import requests
from flask import request, redirect

from . import Keys, Token

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

SIGN_IN_URL = os.getenv("SIGN_IN_URL", "/sign-in")
COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', None)

log.info("Sign in URL is " + SIGN_IN_URL)
log.info("Cookie domain is " + str(COOKIE_DOMAIN))


def authorized():
    # Preference order is header, cookie, session ID
    token = _get_header_token() or request.cookies.get('jwt')
    log.debug("JWT is " + str(token))
    if not token:
        return _unauthorised()
    if not token.verify(token, Keys.list_public_keys()):
        return _unauthorised()
    # Continue with request processing


def _unauthorised():
    # Bounce the user to auth
    log.info("Not authenticated")
    log.info("Cookie is: " + str(request.cookies))
    log.info("Setting cookie for domain: " + str(COOKIE_DOMAIN))
    response = redirect(SIGN_IN_URL)
    response.set_cookie("service", "securities", domain=COOKIE_DOMAIN)
    log.info("Redirecting to: " + SIGN_IN_URL)
    return response


def _get_header_token():
    authorization = request.headers.get('Authorization')
    if authorization:
        parts = authorization.split(" ")
        if len(parts) == 2 and parts[0] == "Bearer":
            return parts[1]

