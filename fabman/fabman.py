#!/usr/bin/python3
"""Main file for the Fabman API library.
"""

import requests

class Fabman:
    """Main Fabman class. All interaction with the library should be done through this class.
    """
    def __init__(self, api_token=None) -> None:
        self.__api_token = api_token
        
    def get_api_token(self) -> str:
        """Returns the API token.
        """
        return self.__api_token