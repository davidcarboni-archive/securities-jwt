import logging

import jwt

"""Retrieves the list of known signature public keys.

    This doesn't attempt to do anything clever.
    At this stage we're just trying to establish a simple interface.
"""

log = logging.getLogger(__name__)


def verify(token, keys):
    log.debug("Checking token " + str(token))
    if token:
        header = jwt.get_unverified_header(token)
        log.debug("token header " + str(header))
        key_id = header.get("kid")
        log.debug("Key ID is: " + str(key_id))
        for key_entry in keys:
            log.debug("testing against key " + str(key_entry))
            if key_entry.get("id") == key_id:
                log.debug("Key is " + str(key_entry.get("key")))
                claims = jwt.decode(token, key_entry.get("key"), algorithms=['ES256'])
                log.debug("Got it - decoding: " + str(claims))
                return claims
