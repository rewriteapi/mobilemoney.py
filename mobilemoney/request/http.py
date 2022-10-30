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
import aiohttp
import json
from typing import ClassVar, Tuple, Union, Dict, Any, Optional
from ..utils import utils
from ..errors.errors import Conflict, MomoException, HTTPException, Unauthorized, MomoServerError, InvalidData, InvalidUniqueIDVersion
from .route import Route
"""
Note : Authorization is api user ID and api key
"""




class HTTPClient:
    """Represent the HTTP client"""

    def __init__(
        self,
        connector: Optional[aiohttp.BaseConnector] = None,
        ) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.connector: aiohttp.BaseConnector = connector,
        self.__session: aiohttp.ClientSession = None
        user_agent =  'MobileMoney python version'
        self.user_agent = user_agent
        self.isLogged = False
        self.isLive = True
        self.data: Optional[Union[Dict[str, Any], str]] = None

    async def login(self)-> None:
        if not self.isLogged:
            self.__session = aiohttp.ClientSession()
            self.isLogged = True
            
            
    async def logout(self)-> None:
        if self.isLogged:
            await self.__session.close()
            self.isLogged = False 
            

    def is_sandbox(self)-> None:
        """Function to turn the library from live to sandbox environment
        Caution : Make sure to activate this before any request if you are not in live
        """
        self.isLive = False

    def uuid_checker(self, uuid: str)-> None:
        """
        Function in charge of checking UUID version and raise error if False
        :parameter: uuid
        """
        if not utils.is_valid_id_4(uuid):
            raise InvalidUniqueIDVersion("Invalid UUID version 4")


    async def request(
        self,
        route: Route    
        )-> aiohttp.ClientResponse:

        await self.login()
        method = route.method
        url = route.url

        #creating headers and adding our user agent for potential statistic or analyse later
        #hope MTN store it lmao
        route.headers['User-Agent'] = self.user_agent

        #response: Optional[aiohttp.ClientResponse] = None
        
        try:
            if route.body is not None:
                body = json.dumps(route.body[0])  
            else:
                body = json.dumps(route.body)
        except KeyError:
            body = json.dumps(route.body)
        
        try:
            async with self.__session.request(method, url, data=body, headers=route.headers) as response:
                self.data = await utils.json_or_text(response)
                await self.logout()
                return response


        except Exception as e:
            print(f'Something wrong when sending request to mtn : {e}')
        
        await self.logout()

    async def create_api_user(self, uuid: str, subscription_key: str, url_callback : Optional[str] = None)->bool:
        """
        Function in charge of creating API USER from wallet provider
        :parameter: uuid, subscription_key
        :return: True or False 
        :return type: bool
        """


        self.uuid_checker(uuid)

        headers = {
            "X-Reference-Id":uuid,
            "Ocp-Apim-Subscription-Key":subscription_key,
            "Content-Type":"application/json"
        }

        if url_callback is None :
            url_callback = 'string'

        body = {
            "providerCallbackHost":url_callback
        }
        
        response: Optional[aiohttp.ClientResponse] = None
        response = await self.request(Route('POST',
        utils.PATH['create_apiuser'][Route.ENV[self.isLive]], 
        self.isLive,
        headers, 
        body))

        #if done 
        if response.status == 201:
            return True
        else:
            utils.errors_manager(response, self.data)

    async def get_api_user(self, uuid: str, subscription_key: str) -> Tuple:
        """
        Function in charge of getting API USER from wallet provider
        :parameter: uuid, subscription_key
        :return: (boolean, user)
        :return type: Tuple
        """
        self.uuid_checker(uuid)

        headers = {
            "Ocp-Apim-Subscription-Key":subscription_key
        }
        response: Optional[aiohttp.ClientResponse] = None
        response =  await self.request(Route('GET', 
        utils.PATH['get_apiuser'][Route.ENV[self.isLive]].format(uuid=uuid), 
        self.isLive,
        headers
        ))

        #if done
        if response.status == 200:
            return (True, self.data)
        else:
            utils.errors_manager(response, self.data)

    async def create_api_key(self, uuid: str, subscription_key: str) -> Tuple:
        """
        Function in charge of creating API KEY from wallet provider
        :parameter: uuid, subscription_key
        :return:(boolean, API KEY)
        :return type: Tuple
        """
        self.uuid_checker(uuid)

        headers = {
            "Ocp-Apim-Subscription-Key":subscription_key
        }
        response: Optional[aiohttp.ClientResponse] = None
        response =  await self.request(Route('POST', 
        utils.PATH['create_apikey'][Route.ENV[self.isLive]].format(apiuser=uuid),
        self.isLive, 
        headers
        ))
        if response.status == 201:
            return (True, self.data)
        else:
            utils.errors_manager(response, self.data)
    



