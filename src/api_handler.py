import json
import xml.dom.minidom

from dateparser import parse
from flask import request, Response

from . import routes_handler

valid_types = ['json', 'xml', 'text']
valid_expirations = ['in 1 hour', 'in 1 day',
                     'in 1 week', 'in 1 month', 'never']

content_type_headers = {
    'json': 'application/json',
    'xml': 'application/xml',
    'text': 'text/html; charset=utf-8',
}

default_payload = """{
    "success": true,
    "info": "This is a sample API response."
}"""


def new():
    """ Create a new Mock API route with a provided payload """

    # Read arguments
    type_ = request.form.get('type')
    body = request.form.get('payload')
    expire = request.form.get('expire')

    # Set type
    if type_ is None or type_ not in valid_types:
        type_ = detect_payload_type(body)

    # Set expiration
    if expire is None or expire not in valid_expirations:
        # Default is to never expire
        expiration_date = None
    else:
        # User has set a valid expiration
        expiration_date = parse(expire)

    # Generate a new route
    route = routes_handler.new(
        type_=type_,
        body=body if body != '' else None,
        expiration_date=expiration_date
    )

    return route


def serve(route):
    """ Serve a Mock API """

    resp = Response(route.body or default_payload)
    resp.headers['Content-Type'] = content_type_headers.get(
        route.type_) if route.body else content_type_headers['json']

    return resp


def detect_payload_type(input_):
    """ Automatically detect a string type """

    if is_json(input_):
        return 'json'
    elif is_xml(input_):
        return 'xml'

    return 'text'


def is_json(input_):
    """ Check if a string is Json """

    if input_ is None:
        return False

    try:
        json.loads(input_)
    except ValueError:
        return False

    return True


def is_xml(input_):
    """ Check if a string is XML """

    if input_ is None:
        return False

    try:
        xml.dom.minidom.parseString(input_)
    except xml.parsers.expat.ExpatError:
        return False

    return True
