#!/usr/bin/python3
"""Main file for the Fabman API library.
"""
import sys
import requests
import logging
import time
from typing import Optional

logger: logging.Logger = logging.getLogger(__name__)
logging_format = logging.Formatter('%(asctime)s::%(name)s::%(levelname)s: %(message)s)')

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(logging_format)

logger.addHandler(stdout_handler)
logger.setLevel(logging.INFO)
                                   

class Fabman:
    """Main Fabman class. All interaction with the library should be done through this class.
    """
    def __init__(self, api_token: str) -> None:
        self.__api_token: str = api_token
        self.__base_url: str = 'https://fabman.io/api/v1'
    
    def __get(self, path, params=None) -> dict:
        """Performs a GET request to the Fabman API.
        """
        url = self.__base_url + path
        headers = {'Authorization': 'Bearer ' + self.__api_token}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception('Invalid API token')
        elif response.status_code == 404:
            raise Exception('Not found')
        elif response.status_code == 429:
            logger.warning("Rate limit exceeded. Retrying in 60 seconds.")
            time.sleep(60)  # TODO: investigate 429 message from fabman to see if it includes a retry-after header
            return self.__get(path, params)
        return response.json()
    
    def __post(self, path, data=None):
        """Performs a POST request to the Fabman API.
        """
        url = self.__base_url + path
        headers = {'Authorization': 'Bearer ' + self.__api_token}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception('Invalid API token')
        elif response.status_code == 404:
            raise Exception('Not found')
        elif response.status_code == 429:
            logger.warning("Rate limit exceeded. Retrying in 60 seconds.")
            time.sleep(60)  # TODO: investigate 429 message from fabman to see if it includes a retry-after header
            return self.__post(path, data)
        return response.json()
        
    def get_api_token(self) -> str:
        """Returns the API token.
        """
        return self.__api_token
    
    def get_user_me(self) -> dict:
        """Returns a json object of the user being represented by the API key.
        Primarily used for a sanity check for the connection to the api, but can 
        also be used to get meaningful stats from the current API-authenticated user

        Returns:
            dict: JSON dictionary of the authenticated user.
        """
        return self.__get('/user/me')
    
    def get_accounts(self, limit=50, orderBy='name', order='asc', **kwargs):
        url_path = f'/accounts?limit={limit}&orderBy={orderBy}&order={order}'
        valid_kwargs = ['offset', 'embed', 'q', 'eq', 'trial', 'countryCode', 'deleted']
        args = ''
        for key in kwargs:
            if key not in valid_kwargs:
                raise KeyError(key)
            args += f"&key={kwargs[key]}"
        return self.__get(url_path)
    
    def get_account(self, id: str, embed: Optional[str]=None) -> dict:
        url_path = f'/accounts/{id}'
        if embed and embed not in ['spaces', 'paymentInfo']:
            raise KeyError(embed)
        elif embed:
            url_path += f'?embed={embed}'
        return self.__get(url_path)
    
    def get_account_payment_info(self, id: str) -> dict:
        return self.__get(f'/accounts/{id}/payment-info')
    
    def get_api_keys(self, limit:int=50, offset:int=0, account:int=-1, embed='') -> dict:
        url_path = f'/api-keys?limit={limit}'
        if offset != 0:
            url_path += f'&offset={offset}'
        if account >= 0:
            url_path += f'&account={account}'
        if embed != '' and embed in ['member']:
            url_path += f'&embed={embed}'
        elif embed != '':
            raise KeyError(embed)
        return self.__get(url_path)
    
    def get_api_by_id(self, id: int, embed='') -> dict:
        raise NotImplementedError('Though documented, Fabman returns 404 not found on this endpoint.')
    
    def get_api_token_by_id(self, id: int) -> dict:
        raise NotImplementedError('Though documented, Fabman returns 404 not found on this endpoint.')
    
            
            
    