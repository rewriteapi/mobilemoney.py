"""
The MIT License (MIT)
Copyright (c) 2022-present rewriteapi
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations
from typing import Optional, Any, Dict, TYPE_CHECKING, Union, List, Tuple


from aiohttp import ClientResponse, ClientWebSocketResponse
from requests import Response

_ResponseType = Union[ClientResponse, Response]

__all__ = (
    'MomoException',
    'HTTPException',
    'Unauthorized',
    'MomoServerError',
    'InvalidData',
    'InvalidUniqueIDVersion',
    'Conflict',
    'NotFound',
    'InvalidBasicToken',
    'InvalidBearerToken'
)

def _flatten_error_dict(d: Dict[str, Any], key: str = '') -> Dict[str, str]:
    items: List[Tuple[str, str]] = []
    for k, v in d.items():
        new_key = key + '.' + k if key else k

        if isinstance(v, dict):
            try:
                _errors: List[Dict[str, Any]] = v['_errors']
            except KeyError:
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, ' '.join(x.get('message', '') for x in _errors)))
        else:
            items.append((new_key, v))

    return dict(items)

class MomoException(Exception):
    """Base exception class for MobileMoney.py
    Ideally speaking, this could be caught to handle any exceptions raised from this library.
    """

    pass
class HTTPException(MomoException):
    """Exception that's raised when an HTTP request operation fails.
    Attributes
    ------------
    response: :class:`aiohttp.ClientResponse`
        The response of the failed HTTP request. This is an
        instance of :class:`aiohttp.ClientResponse`. In some cases
        this could also be a :class:`requests.Response`.
    text: :class:`str`
        The text of the error. Could be an empty string.
    status: :class:`int`
        The status code of the HTTP request.
    code: :class:`int`
        The MTN specific error code for the failure.
    """

    def __init__(self, response: _ResponseType, message: Optional[Union[str, Dict[str, Any]]]):
        self.response: _ResponseType = response
        self.status: int = response.status  # type: ignore # This attribute is filled by the library even if using requests
        self.code: int
        self.text: str
        if isinstance(message, dict):
            self.code = message.get('code', 0)
            base = message.get('message', '')
            errors = message.get('errors')
            self._errors: Optional[Dict[str, Any]] = errors
            if errors:
                errors = _flatten_error_dict(errors)
                helpful = '\n'.join('In %s: %s' % t for t in errors.items())
                self.text = base + '\n' + helpful
            else:
                self.text = base
        else:
            self.text = message or ''
            self.code = 0

        fmt = '{0.status} {0.reason} (error code: {1})'
        if len(self.text):
            fmt += ': {2}'

        super().__init__(fmt.format(self.response, self.code, self.text))
    pass

class Unauthorized(HTTPException):
    """Exception that's raised for when status code 401 occurs.
    Subclass of :exc:`HTTPException`
    """
    pass
class MomoServerError(HTTPException):
    """Exception that's raised for when a 500 range status code occurs.
    Subclass of :exc:`HTTPException`.
    """
    pass
class InvalidData(HTTPException):
    """Exception that's raised for when a 400 range status code occurs.
    Subclass of :exc:`HTTPException`.
    """
    pass
class NotFound(HTTPException):
    """Exception that's raised for when a 404 range status code occurs.
    Subclass of :exc:`HTTPException`.
    """
    pass
class Conflict(HTTPException):
    """Exception that's raised for when a 409 range status code occurs.
    Subclass of :exc:`HTTPException`.
    """
    pass
class InvalidUniqueIDVersion(Exception):
    """Exception that's raised for when UUID is not a valid version 4.
    Subclass of :exc:`Exception`
    """
    pass
class InvalidBasicToken(Exception):
    """Exception that's raised for a invalid Basic token type.
    Subclass of :exc:`Exception`
    """
    pass
class InvalidBearerToken(Exception):
    """Exception that's raised for a invalid Bearer token type.
    Subclass of :exc:`Exception`
    """
    pass