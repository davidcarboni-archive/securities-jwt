from flask import Flask, g
from binascii import hexlify
import os

debug = False

HEADERS = ['X-B3-TraceId', 'X-B3-ParentSpanId', 'X-B3-SpanId', 'X-B3-Sampled', 'X-B3-Flags']


def log_values():
    """Get current tracing information
    :return: A dict containing "trace_id", "span_id" and "export" that can be used to build
    a log-line with Spring-Sleuth-like trace information.
    """
    # For now, we don't export any trace information to Zipkin, so "export" is always "false"
    b3 = b3_values()
    return {
        "trace_id": b3['X-B3-TraceId'],
        "span_id": b3['X-B3-SpanId'],
        "export": "false"
    }


def b3_values():
    """Get the full set of B3 values.
    :return: A dict containing the values "X-B3-TraceId", "X-B3-ParentSpanId", "X-B3-SpanId", "X-B3-Sampled" and
    "X-B3-Flags" for the current span.
    """
    return {
        'X-B3-TraceId': g.get('X-B3-TraceId'),
        'X-B3-ParentSpanId': g.get('X-B3-ParentSpanId'),
        'X-B3-SpanId': g.get('X-B3-SpanId'),
        'X-B3-Sampled': g.get('X-B3-Sampled'),
        'X-B3-Flags': g.get('X-B3-Flags'),
    }


def collect_request_headers(header_values):
    """Collects B3 headers and sets up values for this request as needed.
    The collected/computed values are stored on the application context g using the defined http header names as keys.
    :param header_values: The request headers
    """
    global debug

    # Collect (or generate) a trace ID
    setattr(g, 'X-B3-TraceId', header_values.get('X-B3-TraceId') or _generate_identifier())

    # Parent span, if present
    setattr(g, 'X-B3-ParentSpanId', header_values.get('X-B3-ParentSpanId'))

    # Collect (or set) the span ID
    setattr(g, 'X-B3-SpanId', header_values.get('X-B3-SpanId') or g.get('X-B3-TraceId'))

    # Collect the "sampled" flag, if present
    # We'll propagate the sampled value unchanged if it's set.
    # We're not currently recording traces so if it's present,
    # follow the standard and propagate it, otherwise it's ok to leave it out, rather than set it to "0".
    # This allows downstream services to make the decision if they want to.
    setattr(g, 'X-B3-Sampled', header_values.get('X-B3-Sampled'))

    # Set or update the debug setting
    # We'll set it to "1" if debug=True, otherwise we'll propagate it if present.
    setattr(g, 'X-B3-Flags', "1" if debug else header_values.get('X-B3-Flags'))


def add_request_headers(header_values):
    """ Adds the required headers to the given header dict.
    For the specification, see: https://github.com/openzipkin/b3-propagation
    :param header_values: The headers dict. Headers will be added to this as needed.
    """
    b3 = b3_values()
    # Propagate the trace ID
    header_values['X-B3-TraceId'] = b3['X-B3-TraceId']
    # New span for the outgoing request
    header_values['X-B3-SpanId'] = _generate_identifier()
    # Note the parent span as the current span
    header_values['X-B3-ParentSpanId'] = b3['X-B3-SpanId']
    # Propagate-if-set:
    if b3['X-B3-Sampled']:
        header_values['X-B3-Sampled'] = b3['X-B3-Sampled']
    if b3['X-B3-Flags']:
        header_values['X-B3-Flags'] = b3['X-B3-Flags']


def _generate_identifier():
    """
    Generates a new, random identifier in B3 format.
    :return: A 64-bit random identifier, rendered as a hex String.
    """
    bit_length = 64
    byte_length = int(bit_length / 8)
    identifier = os.urandom(byte_length)
    return hexlify(identifier).decode("ascii")


def check(b3, outbound):
    if b3['X-B3-TraceId'] != outbound['X-B3-TraceId']:
        print(" *** Trace ID mismatch")
    if b3['X-B3-SpanId'] and b3['X-B3-SpanId'] != outbound['X-B3-ParentSpanId']:
        print(" *** Parent pan ID isn't set correctly")
    if b3['X-B3-SpanId'] == outbound['X-B3-SpanId']:
        print(" *** Span ID hasn't been updated")
    if b3['X-B3-Sampled'] and b3['X-B3-Sampled'] != outbound['X-B3-Sampled']:
        print(" *** Sampling is incorrectly propagated")
    if b3['X-B3-Flags'] and b3['X-B3-Flags'] != outbound['X-B3-Flags']:
        print(" *** Debug is incorrectly propagated")

    log = log_values()
    print("[test," + log["trace_id"] + "," + log["span_id"] + "," + log["export"] + "]")
    print()


# with Flask("test").app_context():
#     print("New trace")
#     collect_request_headers({})
#     print(b3_values())
#     headers = {}
#     add_request_headers(headers)
#     print("Outbound request: " + str(headers))
#     check(b3_values(), headers)
#
#     print("New span in an existing trace")
#     collect_request_headers({
#         'X-B3-TraceId': g.get('X-B3-TraceId'),
#         'X-B3-SpanId': _generate_identifier(),
#     })
#     print(b3_values())
#     headers = {}
#     add_request_headers(headers)
#     print("Outbound request: " + str(headers))
#     check(b3_values(), headers)
#
#     print("New sub-span in an existing trace")
#     collect_request_headers({
#         'X-B3-TraceId': g.get('X-B3-TraceId'),
#         'X-B3-SpanId': _generate_identifier(),
#         'X-B3-ParentSpanId': _generate_identifier(),
#     })
#     print(b3_values())
#     headers = {}
#     add_request_headers(headers)
#     print("Outbound request: " + str(headers))
#     check(b3_values(), headers)
#
#     print("With debug")
#     debug = True
#     print(b3_values())
#     headers = {}
#     add_request_headers(headers)
#     print("Outbound request: " + str(headers))
#     check(b3_values(), headers)
