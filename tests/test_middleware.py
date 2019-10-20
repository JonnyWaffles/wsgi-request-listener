from wsgiref.util import setup_testing_defaults

from .context import WSGIListenerMiddleware, DefaultResponseListener, DefaultRequestListener


def app(environ, start_fn):
    start_fn('200 OK', [('Content-Type', 'text/plain')])
    yield "Hello World!\n"


def start_response(status_code, headers):
    return status_code, headers


def test_middleware():
    environ = {}
    setup_testing_defaults(environ)
    wrapped_app = WSGIListenerMiddleware(app)
    rv = wrapped_app(environ, start_response)
    assert next(rv) == "Hello World!\n"

