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

from .http import HTTPClient
from .route import Route
from typing import Dict, Optional, Tuple
from ..utils.utils import is_valid_bearer_token, is_valid_basic_token, COLLECTION_PATH, errors_manager, is_valid_id_4
from ..errors.errors import InvalidBasicToken, InvalidBearerToken, InvalidUniqueIDVersion

class Collection:
    """
    Represent Collection Client used by collection user

    Arguments:
        http: a HTTP client class
        subscription_key: a string

    Returns:
        None
    """

    def __init__(self, http: HTTPClient,  subscription_key: str)->None:
        self.subscription_key = subscription_key
        self.http = http

    async def create_access_token(self, authorization: str)-> Tuple:
        """
        Method to create access token for collection user

        Arguments:
            authorization: a string

        Return:
            Tuple : (boolean, data)
        """

        if is_valid_basic_token(authorization):

            headers = {'Authorization':authorization, 'Ocp-Apim-Subscription-Key':self.subscription_key}
            
            response = await self.http.request(Route('POST', 
            COLLECTION_PATH['create_access_token'][Route.ENV[self.http.isLive]],
            self.http.isLive,
            headers))

            if response.status == 200:
                #want to return a true cause anything can happen, just for a check purpose
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBasicToken('Invalid Basic Token Type given')

    async def get_account_balance(self, authorization: str, target: str)->Tuple:
        """
        Method to get balance for collection user

        Arguments:
            authorization: string
            target: string

        Return
            Tuple : (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET', 
                COLLECTION_PATH['get_account_balance'][Route.ENV[self.http.isLive]],
                self.http.isLive,
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def get_account_balance_in(self, currency: str, authorization: str, target: str)->Tuple:
        """
        Method to get balance in specific currency for collection user

        Arguments:
            currency: string
            authorization: string
            target: string

        Return:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET', 
                COLLECTION_PATH['get_account_balance_in'][Route.ENV[self.http.isLive]].format(currency=currency),
                self.http.isLive,
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
            
        
    async def get_basic_user_info(self, msisdn: str, authorization: str, target: str)-> Tuple:
        """
        Method to get basic user info without consent for collection user

        Arguments:
            msisdn: string
            authorization: string
            target: string
            
        Retruns:
            Tuple : (boolean, data)
        """
        if is_valid_bearer_token(authorization):
            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET',
                COLLECTION_PATH['get_basic_info'][Route.ENV[self.http.isLive]].format(MSISDN=msisdn),
                self.http.isLive,
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def ask_user_info(self, authorization: str, target: str) -> Tuple:
        """
        Method to get user info with consent for collection user

        Arguments:
            authorization: string
            target : string
        
        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):
            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET',
                COLLECTION_PATH['get_user_info'][Route.ENV[self.http.isLive]],
                self.http.isLive, 
                headers))
            
            if response.status == 200:
                return(True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def request_to_pay(self, authorization: str, uuid: str, target: str, body: Dict, callback: Optional[str]=None) -> Tuple:
        """
        Method to request a payment for collection user

        Arguments:
            authorization: string
            uuid: string
            target: string
            body: dictionary
            callback [optional]: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            #check if uuid is valid and raise error if not
            self.http.uuid_checker(uuid)
            
            #callback url is optional, check if parsed and replace the key to avoid any error if not
            callkey = 'X-Callback-Url'
            if callback is None:
                callback = "No callback url given"
                callkey = "No-callback-Url"

            headers = {'Authorization':authorization, 
                'X-Target-Environment':target, 
                'Ocp-Apim-Subscription-Key':self.subscription_key,
                'X-Reference-Id':uuid,
                'Content-Type':'application/json',
                callkey:callback
                }
            
            response = await self.http.request(Route('POST', 
                COLLECTION_PATH['request_to_pay'][Route.ENV[self.http.isLive]],
                self.http.isLive, 
                headers, 
                body))

            if response.status == 202:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
    
    async def get_withdraw_status(self, authorization: str, uuid: str, target : str = 'sandbox') -> Tuple:
        """
        Method to get a withdrawal status for collection user

        Arguments:
            authorization: string
            uuid: string
            target: string
        
        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):
            
            self.http.uuid_checker(uuid)

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET', 
                COLLECTION_PATH['withdraw_status'][Route.ENV[self.http.is_Live]].format(referenceId=uuid),
                self.http.is_Live,
                headers))
            
            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
    

    async def withdraw(self, authorization: str, uuid: str, target: str, body: Dict, callback: Optional[str]=None) -> Tuple:
        """
        Method to withdraw money for collection user

        Arguments:
            authorization: string
            uuid: string
            target: srting
            body: dictionary
            callback [optional]: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            #check if uuid is valid and raise error if not
            self.http.uuid_checker(uuid)
            
            #callback url is optional, check if parsed and replace the key to avoid any error if not
            callkey = 'X-Callback-Url'
            if callback is None:
                callback = "No callback url given"
                callkey = "No-callback-Url"

            headers = {'Authorization':authorization, 
                'X-Target-Environment':target, 
                'Ocp-Apim-Subscription-Key':self.subscription_key,
                'X-Reference-Id':uuid,
                'Content-Type':'application/json',
                callkey:callback
                }
            
            response = await self.http.request(Route('POST', 
                COLLECTION_PATH['withdraw'][Route.ENV[self.http.isLive]],
                self.http.isLive, 
                headers, 
                body))

            if response.status == 202:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')

    async def isActive(self, account: str, account_type: Optional[str]='msisdn', authorization : Optional[str]=None, target : str = 'sandbox') -> Tuple:
        """
        Method to check if an account is active for a collection user

        Arguments:
            account: string
            account_type [optional default set to 'msisdn']: string
            authorization: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """

        headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

        response = await self.http.request(Route('GET',
            COLLECTION_PATH['is_active'][Route.ENV[self.http.isLive]].format(accountHolderIdType=account_type, accountHolderId=account),
            self.http.is_Live,
            headers))
        
        if response.status == 200:
            return (True, self.http.data)
        else:
            errors_manager(response, self.http.data)

    