#!/usr/bin/python3
"""Main file for the Fabman API library.
"""
import sys
import requests
import logging
import time

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
    def __init__(self, api_token=None) -> None:
        self.__api_token = api_token
        self.__base_url = 'https://fabman.io/api/v1'
    
    def __get(self, path, params=None):
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
        
    def get_api_token(self) -> str:
        """Returns the API token.
        """
        return self.__api_token
    