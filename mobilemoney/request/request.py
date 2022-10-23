

from .http import HTTPClient
from .collection import Collection
from .disbursements import Disbursements


class Request:
    def __init__(self):
        self.__http = HTTPClient()
        self.__collection = None
        self.__disbursement = None

    def http(self) -> HTTPClient:
        """
        Method to get the HTTP client

        Arguments:
            None
        
        Returns:
            HTTP client : HTTPClient
        """

        return self.__http
    def collection(self, subscription_key: str,  http : HTTPClient) -> Collection:
        """
        Method to get the collection client

        Arguments:
            subscription_key: string
            http: HTTPClient
        
        Returns:
            Collection client : Collection
        """
        self.__collection = Collection(http, subscription_key)
        return self.__collection
    def disbursements(self, subscription_key: str, http: HTTPClient) -> Disbursements:
        """
        Method to get the Disbursements client

        Arguments:
            subscription_key: string
            http: HTTPClient
        
        Returns:
            Disbursements client : Disbursements
        """

        self.__disbursement = Disbursements(http, subscription_key)
        return self.__disbursement
