# import os
# import requests
#
# """Retrieves the list of known signature public keys.
#
#     This doesn't attempt to do anything clever.
#     At this stage we're just trying to establish a simple interface.
# """
#
# KEYS_URL = os.getenv("KEYS_URL", "http://auth:5000/keys")
#
#
# def list_public_keys():
#     return requests.get(KEYS_URL).json()
