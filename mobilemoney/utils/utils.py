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

import json
from typing import Any, Dict, Union, TYPE_CHECKING, Optional
import base64
from urllib.parse import urlencode
import uuid
import aiohttp
from ..errors.errors import *



from aiohttp import ClientResponse, ClientWebSocketResponse
from requests import Response

_ResponseType = Union[ClientResponse, Response]

def encode_params(params: Any):
    
    if type(params) is not Dict:
        params = Dict(params)
    
    return urlencode(params)

def _to_json(obj: Any) -> str:
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=True)

_from_json = json.loads

def b64_encode(data: str)->str:
    """This function encode data to base64"""

    data_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(data_bytes)
    data_encoded = base64_bytes.decode('ascii')

    return data_encoded

def is_valid_bearer_token(token: str)->bool:
    if token.startswith('Bearer '):
        return True
    else:
        return False

def is_valid_basic_token(token: str)->bool:
    if token.startswith('Basic '):
        return True
    else:
        return False

async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')

    try:
        if response.headers['content-type'] == 'application/json;charset=utf-8' or response.headers['content-type'] == 'application/json':
            return _from_json(text)
    except KeyError:
        pass

    return text

def get_reference_id()->str:
    """A method helping api user to get X-Reference-id
        Arguement : None
        Return : UUID 
        Return type : str
    """
    unique_id = uuid.uuid4()
    return str(unique_id)

def is_valid_id_4(unique_id: str)->bool:
    """A method checking if X-Reference-id is a valid UUID version 4
        parameter : X-Reference-id
        Return type : bool
    """
    try:
        id_convert_test = uuid.UUID(unique_id, version=4)
    except ValueError:
        return False
    return str(id_convert_test) == unique_id

def errors_manager(response: _ResponseType, data: Optional[Union[str, Dict[str, Any]]] = "")-> None:

    print(response)
    print(data)

    if response.status == 400:
        raise InvalidData(response, data)
    elif response.status == 409:
        raise Conflict(response, data)
    elif response.status == 500:
        raise MomoServerError(response, data)
    elif response.status == 401:
        raise Unauthorized(response, data)
    elif response.status == 404:
        raise NotFound(response, data)
    else:
        raise HTTPException(response, data)

PATH = {
    "create_apiuser":{
        "sandbox":"/v1_0/apiuser",
        "live":"/provisioning/v1_0/apiuser"
    },
    "get_apiuser":{
        "sandbox":"/v1_0/apiuser/{uuid}",
        "live":""
    },
    "create_apikey":{
        "sandbox":"/v1_0/apiuser/{apiuser}/apikey",
        "live":""
    }
}

COLLECTION_PATH = {
    "create_access_token":{
        "sandbox":"/collection/token/",
        "live":"/collection/token/"
    },
    "get_account_balance":{
        "sandbox":"/collection/v1_0/account/balance",
        "live":"/collection/v1_0/account/balance"
    },
    "get_account_balance_in":{
        "sandbox":"/collection/v1_0/account/balance/{currency}",
        "live":"/collection/v1_0/account/balance/{currency}"
    },
    "get_basic_info":{
        "sandbox":"/collection/v1_0/accountholder/msisdn/{MSISDN}/basicuserinfo",
        "live":"/collection/v1_0/accountholder/msisdn/{MSISDN}/basicuserinfo"
    },
    "get_user_info":{
        "sandbox":"/collection/oauth2/v1_0/userinfo",
        "live":"/collection/oauth2/v1_0/userinfo"
    },
    "request_to_pay":{
        "sandbox":"/collection/v1_0/requesttopay",
        "live":"/collection/v1_0/requesttopay"
    },
    "withdraw":{
        "sandbox":"/collection/v2_0/requesttowithdraw",
        "live":"/collection/v2_0/requesttowithdraw"
    },
    "withdraw_status":{
        "sandbox":"/collection/v1_0/requesttowithdraw/{referenceId}",
        "live":"/collection/v1_0/requesttowithdraw/{referenceId}"
    },
    "is_active":{
        "sandbox":"/collection/v1_0/accountholder/{accountHolderIdType}/{accountHolderId}/active",
        "live":"/collection/v1_0/accountholder/{accountHolderIdType}/{accountHolderId}/active"
    }
}

DISBURSEMENTS_PATH = {
    "create_access_token":{
        "sandbox":"/disbursement/token/",
        "live":"/disbursement/token/"
    },
    "get_account_balance":{
        "sandbox":"/disbursement/v1_0/account/balance",
        "live":"/disbursement/v1_0/account/balance"
    },
    "get_account_balance_in":{
        "sandbox":"/disbursement/v1_0/account/balance/{currency}",
        "live":"/disbursement/v1_0/account/balance/{currency}"
    },
    "get_basic_info":{
        "sandbox":"/disbursement/v1_0/accountholder/msisdn/{MSISDN}/basicuserinfo",
        "live":"/disbursement/v1_0/accountholder/msisdn/{MSISDN}/basicuserinfo"
    },
    "get_user_info":{
        "sandbox":"/disbursement/oauth2/v1_0/userinfo",
        "live":"/disbursement/oauth2/v1_0/userinfo"
    },
    "is_active":{
        "sandbox":"/disbursement/v1_0/accountholder/{accountHolderIdType}/{accountHolderId}/active",
        "live":"/disbursement/v1_0/accountholder/{accountHolderIdType}/{accountHolderId}/active"
    },
    "get_transfer_status":{
        "sandbox":"/disbursement/v1_0/transfer/{referenceId}",
        "live":"/disbursement/v1_0/transfer/{referenceId}"
    },
    "deposit":{
        "sandbox":"/disbursement/v2_0/deposit",
        "live":"/disbursement/v2_0/deposit"
    },
    "transfer":{
        "sandbox":"/disbursement/v1_0/transfer",
        "live":"/disbursement/v1_0/transfer"
    },
    "refund":{
        "sandbox":"/disbursement/v2_0/refund",
        "live":"/disbursement/v2_0/refund"
    },
    "get_transfer_status":{
        "sandbox":"/disbursement/v1_0/transfer/{referenceId}",
        "live":"/disbursement/v1_0/transfer/{referenceId}"
    },
    "get_refund_status":{
        "sandbox":"/disbursement/v1_0/refund/{referenceId}",
        "live":"/disbursement/v1_0/refund/{referenceId}"
    }
}