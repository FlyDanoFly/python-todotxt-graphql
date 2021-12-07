from ariadne.exceptions import HttpError, HttpBadRequestError

from data.user_data import user_data


"""
As part of my "keep it simple" design pattern, kinda cheat and use
a context getter for authentication. Very simple, just look for
a header like so:
    Authorization: Bearer secret-key

This is based ever so loosley on RFC6750:
    https://datatracker.ietf.org/doc/html/rfc6750

Use the hardcoded user_data.py to translate the secret-key
to user data and put that in the request, otherwise raise
a 401 exception.

It suits my immediate needs and isn't robust to more 
complicated authentication headers. Should those be needed
consider using this framework with a Flask or FastAPI app.

Quick note:
For a failed authentication it doesn't send the proper
    WWW-Authenticate: Bearer realm="Authorization Required"
header. Ariadne doesn't provide a clean way to add HTTP
headers short of overriding the WSGI server and my immediate
needs don't really need this to be super friendly and chatty
to other programs. Again consider joining this with another
framework of that is desired.
"""


AUTHENTICATION_HEADER = 'HTTP_AUTHORIZATION'
AUTHENTICATION_SCHEME = 'Bearer'


class HttpUnauthorizedError(HttpError):
    status = "401 Unauthorized"


def authenticate_and_get_context(environ):
    if AUTHENTICATION_HEADER not in environ:
        raise HttpUnauthorizedError('need header')

    authentication_parts = environ[AUTHENTICATION_HEADER].split()

    if len(authentication_parts) < 2:
        raise HttpBadRequestError()

    if authentication_parts[0].lower() != AUTHENTICATION_SCHEME.lower():
        raise HttpBadRequestError()

    authentication_key = authentication_parts[1]
    if authentication_key not in user_data:
        raise HttpUnauthorizedError('nono no')

    # If we got here, we have a valid header and token
    return {
        'request': environ,
        'user_data': user_data[authentication_key]
    }
