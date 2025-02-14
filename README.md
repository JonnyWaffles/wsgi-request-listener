# WSGI Listener

## Request/Response Inspection for WSGI Web Applications
WSGI listener middleware for WSGI Web Applications inspired by the
original wsgi-request-logger by Philipp Klaus and L. C. Rees.

Provides hooks during the request and response cycle by adding an extra level of indirection.

Instead of directly logging the response, this middleware provides an
interface to easily inspect the request and response. The default
behavior logs the response similarly to the original project. However, now
additional listeners can be added to both the request and response cycle.
The request and response body content is part of the interface.

Project Homepage: https://github.com/JonnyWaffles/wsgi-listener
Original project's Homepage: https://github.com/pklaus/wsgi-request-logger

Easily add loggers, emailers, event systems, etc, with the `request_listeners` and `response_listener` hooks.

#### Installation
todo: Ship to pypi
Simply install this Python module via

    pip install wsgi-listener

#### Usage
To add this middleware to your WSGI `application` with the default response logger named `wsgilistener` in Apache format.
```python
from wsgi_listener import WSGIListenerMiddleware

    
def application(environ, start_response):
    response_body = 'The request method was %s' % environ['REQUEST_METHOD']
    response_body = response_body.encode('utf-8')
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response('200 OK', response_headers)
    return [response_body]


loggingapp = WSGIListenerMiddleware(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    http = make_server('', 8080, loggingapp)
    http.serve_forever()
```
#### Custom handlers
The interface for the Request listeners is:
```python
from abc import ABC, abstractmethod

class AbstractBaseRequestListener(ABC):
    @abstractmethod
    def handle(self, environ: dict, request_body: bytes, **kwargs) -> None:
        """Defines the interface for Request listeners.

        Args:
            environ: The WSGI envion dictionary
            request_body: The bytes content of the request, if any
            **kwargs: Optional hook for additional data
        """
```
and the interface for Response listeners is:
```python
from abc import ABC, abstractmethod

class AbstractBaseResponseListener(ABC):
    @abstractmethod
    def handle(self, status_code: int, environ: dict, content_length: int, response_body: bytes,
               processing_time: float, **kwargs) -> None:
        """Defines the interface for Response listeners.

        Args:
            status_code: HTTP status code as integer
            environ: WSGI environ dictionary
            content_length: Number of bytes returned as int
            response_body: The response content, if any
            processing_time: The time in miliseconds to process the request
            **kwargs: Extensible hook
        """
```
Simply instantiate your hooks and add them during init or with the `add_listener` methods.

#### The Authors

This WSGI middleware was originally developed under the name [wsgilog](https://pypi.python.org/pypi/wsgilog/) by  **L. C. Rees**.
It was forked by **Philipp Klaus** in 2013 to build a WSGI middleware for request logging rather than exception handling and logging,
and then forked again by **Jonny Fuller** in 2019 to add the additional layer of indirection.  


#### License

This software, *wsgi-listener*, is published under a *3-clause BSD license*.

#### Developers' Resources

* The [WSGI](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) - Web Server Gateway Interface - is defined in [PEP 333](http://www.python.org/dev/peps/pep-0333/) with an update for Python 3 in [PEP 3333](http://www.python.org/dev/peps/pep-3333/).

#### General References

* PyPI's [listing of wsgi-request-logger](https://pypi.python.org/pypi/wsgi-request-logger)
* This fork source code is hosted at Github (todo determine url)
* The original source code for this Python module is [hosted on Github](https://github.com/pklaus/wsgi-request-logger).
* A blog post with more background information and usage examples:
  [wsgi-request-logger – Logging HTTP Requests With Any WSGI Web Application like Flask, Bottle or Django](https://blog.philippklaus.de/2013/06/wsgi-request-logger-logging-http-requests-with-any-wsgi-web-application-like-flask-bottle-or-django/)
