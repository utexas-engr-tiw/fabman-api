#!/usr/bin/python3
"""Main file for the Fabman API library.
"""
import sys
import requests
import logging
import time
from typing import Optional, List, Dict, Union, AnyStr

logger: logging.Logger = logging.getLogger(__name__)
logging_format = logging.Formatter(
    '%(asctime)s::%(name)s::%(levelname)s: %(message)s)')

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

    def __get(self, path, params=None) -> Union[Dict, List]:
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
            # TODO: investigate 429 message from fabman to see if it includes a retry-after header
            time.sleep(60)
            return self.__get(path, params)
        return response.json()

    def __post(self, path, data=None) -> Union[Dict, List]:
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
            # TODO: investigate 429 message from fabman to see if it includes a retry-after header
            time.sleep(60)
            return self.__post(path, data)
        return response.json()

    def get_api_token(self) -> Union[AnyStr, str, None]:
        """Returns the API token.
        """
        return self.__api_token

    def get_user_me(self) -> Union[Dict, List]:
        """Returns a json object of the user being represented by the API key.
        Primarily used for a sanity check for the connection to the api, but can 
        also be used to get meaningful stats from the current API-authenticated user

        Returns:
            dict: JSON dictionary of the authenticated user.
        """
        return self.__get('/user/me')

    def get_accounts(self, limit=50, orderBy='name', order='asc', **kwargs) -> Union[Dict, List]:
        """Returns a list of accounts

        Args:
            limit (int, optional): Numberof accounts to return. Defaults to 50.
            orderBy (str, optional): Field to order by. Can be 'name', 'id', 'plan', 'createdAt', 'trialEndDate'. Defaults to 'name'.
            order (str, optional): Order ascending or descending. Defaults to 'asc'.
            **kwargs: Additional arguments to filter the results. Valid arguments are 'offset', 'embed', 'q', 'eq', 'trial', 'countryCode', 'deleted'. Refer to the fabman API documentation for more information.

        Raises:
            KeyError: Raised when an incorrect value has been passed to one of the keyword arguments.
        Returns:
            List of Dict: List of accounts matching the query.
        """
        url_path = f'/accounts?limit={limit}&orderBy={orderBy}&order={order}'
        valid_kwargs = ['offset', 'embed', 'q',
                        'eq', 'trial', 'countryCode', 'deleted']
        if orderBy not in ['name', 'id', 'plan', 'createdAt', 'trialEndDate']:
            raise KeyError(orderBy)
        args = ''
        for key in kwargs:
            if key not in valid_kwargs:
                raise KeyError(key)
            if key == 'embed' and kwargs[key] != 'spaces':
                raise KeyError(kwargs[key])
            args += f"&key={kwargs[key]}"
        return self.__get(url_path)

    def get_account_by_id(self, id: str, embed: Optional[str] = None) -> Union[Dict, List]:
        """Returns a single account by the provided id

        Args:
            id (str, required): The id of the account to return.
            embed (str, optional): Embed additional information. Can be 'spaces' or 'paymentInfo'. Defaults to None.

        Raises:
            KeyError: Raised when an incorrect value has been passed to one of the keyword arguments.
        Returns:
            Dict: A single account matching the query.
        """
        url_path = f'/accounts/{id}'
        if embed and embed not in ['spaces', 'paymentInfo']:
            raise KeyError(embed)
        elif embed:
            url_path += f'?embed={embed}'
        return self.__get(url_path)

    def get_account_payment_info(self, id: str) -> Union[Dict, List]:
        """Get the payment information from a single account.

        Args:
            id (str): Id of the account to retrieve

        Returns:
            Union[Dict, List]: Dictionary of payment information
        """
        return self.__get(f'/accounts/{id}/payment-info')

    def get_api_keys(self, limit: int = 50, offset: int = 0, account: int = -1, embed: Optional[str] = None) -> Union[Dict, List]:
        """Generate a list of accounts holding current API Keys.

        Args:
            limit (int, optional): Number of accounts to return. Defaults to 50.
            offset (int, optional): Offset in the list of all accounts. Defaults to 0.
            account (int, optional): Give a specific account id. Defaults to -1.
            embed (Optional[str], optional): Embed additional information in the returned information. Only valid options are None or 'member'. Defaults to None.

        Raises:
            KeyError: _description_

        Returns:
            Union[Dict, List]: _description_
        """
        url_path = f'/api-keys?limit={limit}'
        if offset != 0:
            url_path += f'&offset={offset}'
        if account >= 0:
            url_path += f'&account={account}'
        if embed and embed in ['member']:
            url_path += f'&embed={embed}'
        elif embed:
            raise KeyError(embed)
        return self.__get(url_path)

    def get_api_by_id(self, id: int, embed: Optional[str] = None) -> Union[Dict, List]:
        """Returns API key information from a single account id.

        Args:
            id (int): ID of account in question
            embed (Optional[str], optional): Embed additional information. Can be either 'member' or None. Defaults to None.

        Raises:
            NotImplementedError: Endpoint returns a 404 and is seemingly broken at time of development.

        Returns:
            Union[Dict, List]
        """
        raise NotImplementedError(
            'Though documented, Fabman returns 404 not found on this endpoint.')

    def get_api_token_by_id(self, id: int) -> Union[Dict, List]:
        """Returns API token from a single account id.

        Args:
            id (int): ID of account in question
            embed (Optional[str], optional): Embed additional information. Can be either 'member' or None. Defaults to None.

        Raises:
            NotImplementedError: Endpoint returns a 404 and is seemingly broken at time of development.

        Returns:
            Union[Dict, List]
        """
        raise NotImplementedError(
            'Though documented, Fabman returns 404 not found on this endpoint.')
