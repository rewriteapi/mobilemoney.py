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
from typing import ClassVar, Optional, Any, Union, Dict as Dict

class Route:
    """Classe in charge or all different paths"""

    BASE : ClassVar[Dict[str, str]] = {
        'sandbox':'https://sandbox.momodeveloper.mtn.com',
        'live':'https://proxy.momoapi.mtn.com'
    }
    ENV : ClassVar[Dict[bool, str]] = {
        False:"sandbox",
        True:'live'
    }

    def __init__(self, method : str, path: str, production : bool, headers : Dict = None, body : Optional[Any] = None) -> None:
        self.method: str = method
        self.path: str = path
        self.production: bool = production
        self.body: str = body
        self.headers: str = headers
        self.url: str = self.BASE[self.ENV[self.production]] + self.path
