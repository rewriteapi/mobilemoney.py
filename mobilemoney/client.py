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

import asyncio
import datetime
import logging
from typing import Any, Optional, Dict, Tuple
import aiohttp


from .request.request import Request
from .utils.utils import get_reference_id, b64_encode
class Client:
    """
    client agent
    """

    def __init__(self) -> None:
        self.request = Request()
        self.http = self.request.http()

    def collection(self, subscription_key: str) -> Any:
        """
        Method to get the collection client

        Arguments:
            subscription_key: string
        
        Returns:
            Collection client : Collection
        """
        return self.request.collection(subscription_key, self.http)

    def disbursements(self, subscription_key: str)-> Any:
        """
        Method to get the Disbursements client

        Arguments:
            subscription_key: string
        
        Returns:
            Disbursements client : Disbursements
        """
        return self.request.disbursements(subscription_key, self.http)

    async def create_api_user(self, uuid: str, subscription_key: str, url_callback : Optional[str] = None)->bool:
        """
        Function in charge of creating API USER from wallet provider
        :parameter: uuid, subscription_key, url_callback [optional]
        :return: True or False 
        :return type: bool
        """
        return await self.http.create_api_user(uuid, subscription_key,url_callback)

    async def get_api_user(self, uuid: str, subscription_key: str) -> Tuple:
        """
        Function in charge of getting API USER from wallet provider
        :parameter: uuid, subscription_key
        :return: (boolean, user)
        :return type: Tuple
        """
        return await self.http.get_api_user(uuid, subscription_key)

    async def create_api_key(self, uuid: str, subscription_key: str) -> Tuple:
        """
        Function in charge of creating API KEY from wallet provider
        :parameter: uuid, subscription_key
        :return:(boolean, API KEY)
        :return type: Tuple
        """
        return await self.http.create_api_key(uuid, subscription_key)

    def get_reference_id(self)-> str:
        """
        Function to create UUID version 4
        Arguments:
            None

        Returns:
            UUID: string
        """
        return get_reference_id()

    def is_sandbox(self) -> None:
        """method to turn on sandbpx environement

        CAUTION
        -------------------
        Make sure to call this function firstly before any request or you will make request to live environment
        """
        self.http.is_sandbox()

    def basic_token(self, apiuser: str, apikey: str) -> str:
        """Method to create basic token from API USER & API KEY"""

        data =  f'{apiuser}:{apikey}'
        encoded = b64_encode(data)
        return f"Basic {encoded}"

    def bearer_token(self, token: str)-> str:
        """Method to convert access token to Bearer token"""

        return f"Bearer {token}"
