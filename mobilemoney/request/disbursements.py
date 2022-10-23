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

from typing import Dict, Tuple, Optional

from ..errors.errors import InvalidBasicToken, InvalidBearerToken

from ..utils.utils import errors_manager, is_valid_basic_token, is_valid_bearer_token, DISBURSEMENTS_PATH
from .http import HTTPClient
from .route import Route


class Disbursements:
    """
    Represent Disbursement Client used by disbursement user

    Arguments:
        http: a HTTP client class
        subscription_key: a string

    Returns:
        None
    """
    def __init__(self, http: HTTPClient, subscripyion_key: str)->None:
        self.http = http
        self.subscripyion_key = subscripyion_key

    async def create_access_token(self, authorization: str) -> Tuple:
        """
        Method to create access token for Disbursements user

        Arguments:
            authorization: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_basic_token(authorization):
            headers = {"Authorization":authorization, "Ocp-Apim-Subscription-Key":self.subscripyion_key}
            response = await self.http.request(Route('POST', 
                DISBURSEMENTS_PATH['create_access_token'][Route.ENV[self.http.isLive]],
                self.http.isLive, 
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBasicToken('Invalid Basic Token Type given')

    async def get_account_balance(self, authorization: str, target: str)->Tuple:
        """
        Method to get account balance for Disbursement user

        Arguments:
            authorization: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """
        if is_valid_bearer_token(authorization):

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET', 
                DISBURSEMENTS_PATH['get_account_balance'][Route.ENV[self.http.isLive]],
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
        Method to get balance in specific currency for disbursement user

        Arguements:
            currency: string
            authorization: string
            target:string
        
        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET', 
                DISBURSEMENTS_PATH['get_account_balance_in'][Route.ENV[self.http.isLive]].format(currency=currency),
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
        Method to get basic user info without consent for disbursement user

        Arguments:
            msisdn: string
            authorization: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """
        if is_valid_bearer_token(authorization):
            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET',
                DISBURSEMENTS_PATH['get_basic_info'][Route.ENV[self.http.isLive]].format(MSISDN=msisdn),
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
        Method to get user info with consent for disbursement user

        Arguments:
            authorization: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):
            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET',
                DISBURSEMENTS_PATH['get_user_info'][Route.ENV[self.http.isLive]],
                self.http.isLive, 
                headers))
            
            if response.status == 200:
                return(True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def get_deposit_status(self, uuid: str, authorization: str, target: str) -> Tuple:
        """
        Method to get transfer status for disbursement user

        Arguments:
            uuid: string
            authorization: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            self.http.uuid_checker(uuid)

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET', 
                DISBURSEMENTS_PATH['get_tranfer_status'][Route.ENV[self.http.isLive]].format(referenceId=uuid),
                self.http.isLive, 
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            InvalidBearerToken('Invalid Bearer Token Type given')
         
    async def deposit(self, uuid: str, authorization: str, target:str, body: Dict, url_callback: Optional[str]= None) -> Tuple:
        """
        Method to deposit for disbursement user 

        Arguments:
            uuid: string
            authorization: string
            target: string
            body: dictionary
            url_callback [optional]: string

        Returns:
            Tuple: (boolean, data)
        """
        
        if is_valid_bearer_token(authorization):

            self.http.uuid_checker(uuid)

            callkey = 'X-Callback-Url'
            if url_callback is None:
                url_callback = "No callback url given"
                callkey = "No-callback-Url"

            headers = {
                'Authorization':authorization, 
                'X-Target-Environment':target, 
                'Ocp-Apim-Subscription-Key':self.subscription_key,
                'X-Reference-Id':uuid,
                'Content-Type':'application/json',
                callkey:url_callback
            }

            response = await self.http.request(Route('POST', 
                DISBURSEMENTS_PATH['deposit'][Route.ENV[self.http.isLive]],
                headers, 
                body))
            
            if response.status == 202:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)

        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def transfer(self, uuid: str, authorization: str, target:str, body: Dict, url_callback: Optional[str]= None) -> Tuple:
        """
        Method to transfer for disbursement user 

        Arguments:
            uuid: string
            authorization: string
            target: string
            body: dictionary
            url_callback [optional]: string

        Returns:
            Tuple: (boolean, data)
        """
        
        if is_valid_bearer_token(authorization):

            self.http.uuid_checker(uuid)

            callkey = 'X-Callback-Url'
            if url_callback is None:
                url_callback = "No callback url given"
                callkey = "No-callback-Url"

            headers = {
                'Authorization':authorization, 
                'X-Target-Environment':target, 
                'Ocp-Apim-Subscription-Key':self.subscription_key,
                'X-Reference-Id':uuid,
                'Content-Type':'application/json',
                callkey:url_callback
            }

            response = await self.http.request(Route('POST', 
                DISBURSEMENTS_PATH['transfer'][Route.ENV[self.http.isLive]],
                headers, 
                body))
            
            if response.status == 202:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)

        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def refund(self, uuid: str, authorization: str, target:str, body: Dict, url_callback: Optional[str]= None) -> Tuple:

        """
        Method to transfer for disbursement user 

        Arguements:
            uuid: string
            authorization: string
            target: string
            body: dictionary
            url_callback [optional]: string

        Returns:
            Tuple: (boolean, data)
        """
        
        if is_valid_bearer_token(authorization):

            self.http.uuid_checker(uuid)

            callkey = 'X-Callback-Url'
            if url_callback is None:
                url_callback = "No callback url given"
                callkey = "No-callback-Url"

            headers = {
                'Authorization':authorization, 
                'X-Target-Environment':target, 
                'Ocp-Apim-Subscription-Key':self.subscription_key,
                'X-Reference-Id':uuid,
                'Content-Type':'application/json',
                callkey:url_callback
            }

            response = await self.http.request(Route('POST', 
                DISBURSEMENTS_PATH['refund'][Route.ENV[self.http.isLive]],
                headers, 
                body))
            
            if response.status == 202:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)

        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def get_transfer_status(self, uuid: str, authorization: str, target: str) -> Tuple:
        """
        Method to get transfer status for disbursement user

        Arguments:
            uuid: string
            authorization: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            self.http.uuid_checker(uuid)

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}
            
            response = await self.http.request(Route('GET',
                DISBURSEMENTS_PATH['get_transfer_status'][Route.ENV[self.http.isLive]].format(referenceId=uuid),
                self.http.isLive, 
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
     
    async def get_refund_status(self, uuid: str, authorization: str, target: str) -> Tuple:
        """
        Method to get transfer status for disbursement user

        Arguments:
            uuid: string
            authorization: string
            target: string
        
        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):

            self.http.uuid_checker(uuid)

            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}
            
            response = await self.http.request(Route('GET',
                DISBURSEMENTS_PATH['get_refund_status'][Route.ENV[self.http.isLive]].format(referenceId=uuid),
                self.http.isLive, 
                headers))

            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
    async def isActive(self, account: str, authorization : str, account_type: Optional[str]='msisdn',  target : str = 'sandbox') -> Tuple:
        """
        Method to check if an account is active for a disbursement user

        Arguements:
            account: string
            authorization: string
            account_type [optional default set to 'msisdn']: string
            target: string

        Returns:
            Tuple: (boolean, data)
        """

        if is_valid_bearer_token(authorization):
            headers = {'Authorization':authorization, 'X-Target-Environment':target, 'Ocp-Apim-Subscription-Key':self.subscription_key}

            response = await self.http.request(Route('GET',
                DISBURSEMENTS_PATH['is_active'][Route.ENV[self.http.isLive]].format(accountHolderIdType=account_type, accountHolderId=account),
                self.http.is_Live,
                headers))
            
            if response.status == 200:
                return (True, self.http.data)
            else:
                errors_manager(response, self.http.data)
        else:
            raise InvalidBearerToken('Invalid Bearer Token Type given')
        
