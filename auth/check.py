# import os
# import logging
# from flask import request, redirect
#
# log = logging.getLogger(__name__)
#
# SIGN_IN_URL = os.getenv("SIGN_IN_URL", "/sign-in?service=securities")
# log.info("Sign in URL is " + SIGN_IN_URL)
#
#
# def authorized(f):
#     log.info(request.headers)
#     def wrapper():
#         jwt = request.headers.get('Bearer')
#         if jwt:
#             log.info("Got JWT")
#             return f()
#         else:
#             log.info("No JWT")
#             log.info("Redirecting to " + SIGN_IN_URL)
#             return redirect(SIGN_IN_URL)
#
#         return f()
#     return wrapper
