#!/usr/bin/python3
"""Main file for the Fabman API library.
"""

#  TODO: Sanitize datetime inputs to ensure they are appropriate
#  TODO: Check 429 responses for retry-after headers
#  TODO: refactor accounts to not use **kwargs, instead giving all possible arguments as keyword arguments
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
            orderBy (str, optional): Field to order by. Can be 'name', 'id', 'plan', 'createdAt', 'trialEndDate'. 
            Defaults to 'name'.
            order (str, optional): Order ascending or descending. Defaults to 'asc'.
            **kwargs: Additional arguments to filter the results. Valid arguments are 'offset', 'embed', 'q', 'eq', 
            'trial', 'countryCode', 'deleted'. Refer to the fabman API documentation for more information.

        Raises:
            KeyError: Raised when an incorrect value has been passed to one of the keyword arguments.
        Returns:
            List of Dict: List of accounts matching the query.
        """
        if order not in ['asc', 'desc']:
            raise KeyError(order)
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
            embed (Optional[str], optional): Embed additional information in the returned information. Only valid 
            options are None or 'member'. Defaults to None.

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
            embed (Optional[str], optional): Embed additional information. Can be either 'member' or None. Defaults to 
            None.

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
            embed (Optional[str], optional): Embed additional information. Can be either 'member' or None. Defaults to
            None.

        Raises:
            NotImplementedError: Endpoint returns a 404 and is seemingly broken at time of development.

        Returns:
            Union[Dict, List]
        """
        raise NotImplementedError(
            'Though documented, Fabman returns 404 not found on this endpoint.')

    def get_bookings(self, account: Optional[str] = None, space: Optional[str] = None, resource: Optional[str] = None,
                     member: Optional[str] = None, fromDateTime: Optional[str] = None,
                     untilDateTime: Optional[str] = None, state: Optional[str] = None, resolve: Optional[str] = None,
                     order='desc', limit: int = 50, offset: int = 0, summary: bool = False) -> Union[Dict, List]:
        """Returns a list of bookings matching the query.

        Args:
            account (Optional[str], optional): Account id to inspect. Defaults to None.
            space (Optional[str], optional): The space which will hold the bookings. Defaults to None.
            resource (Optional[str], optional): The resource which is booked. Defaults to None.
            member (Optional[str], optional): The member ID of the member holding the bookings. Defaults to None.
            fromDateTime (Optional[str], optional): Beginning DateTime. Defaults to None.
            untilDateTime (Optional[str], optional): Ending DateTime. Defaults to None.
            state (Optional[str], optional): One of 'pending,' 'confirmed,' or 'cancelled'. Defaults to None.
            resolve (Optional[str], optional): Return relationship details instead of just the id. Can be either 
            'resource' or 'member'. Defaults to None.  
            order (str, optional): Either 'asc' or 'desc'. Defaults to 'desc'.
            limit (int, optional): Number of entries to return. Defaults to 50.
            offset (int, optional): Offset of entries. Can be used for pagination. Defaults to 0.
            summary (bool, optional): Add headers with summary information about found records. Defaults to False.

        Returns:
            Union[Dict, List]: _description_
        """
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        url_path = f'/bookings?order={order}&limit={limit}&offset={offset}&summary={summary}'
        if state and state in ['pending', 'confirmed', 'cancelled']:
            url_path += f'&state={state}'
        elif state:
            raise KeyError(state)
        if resolve and resolve in ['resource', 'member']:
            url_path += f'&resolve={resolve}'
        elif resolve:
            raise KeyError(resolve)
        if account:
            url_path += f'&account={account}'
        if space:
            url_path += f'&space={space}'
        if resource:
            url_path += f'&resource={resource}'
        if member:
            url_path += f'&member={member}'
        if fromDateTime:
            url_path += f'&fromDateTime={fromDateTime}'
        if untilDateTime:
            url_path += f'&untilDateTime={untilDateTime}'
        return self.__get(url_path)

    def get_bookings_by_id(self, id: int, embed: Optional[str] = None) -> Union[Dict, List]:
        """Get the booking information for a single booking id.

        Args:
            id (int): ID of the booking in question
            embed (Optional[str], optional): Allows you to embed related entities to reduce the number of requests 
            needed Can be either 'member' or 'resource'. Defaults to None.

        Returns:
            Union[Dict, List]: Dictionary containing information of the booking.
        """
        url_path = f'/bookings/{id}'
        if embed and embed in ['member', 'resource']:
            url_path += f'?embed={embed}'
        elif embed:
            raise KeyError(embed)

        return self.__get(url_path)

    def get_bookings_export(self, account: Optional[str] = None, space: Optional[str] = None, 
                            resource: Optional[str] = None, member: Optional[str] = None, 
                            fromDateTime: Optional[str] = None, untilDateTime: Optional[str] = None, 
                            state: Optional[str] = None, resolve: Optional[str] = None, 
                            order: str = 'desc') -> Union[Dict, List, str]:
        """Returns a download link for a CSV document containing the information of _all_ bookings matching the query.

        Args:
            account (Optional[str], optional): Account id to inspect. Defaults to None.
            space (Optional[str], optional): The space which will hold the bookings. Defaults to None.
            resource (Optional[str], optional): The resource which is booked. Defaults to None.
            member (Optional[str], optional): The member ID of the member holding the bookings. Defaults to None.
            fromDateTime (Optional[str], optional): Beginning DateTime. Defaults to None.
            untilDateTime (Optional[str], optional): Ending DateTime. Defaults to None.
            state (Optional[str], optional): One of 'pending,' 'confirmed,' or 'cancelled'. Defaults to None.
            resolve (Optional[str], optional): Return relationship details instead of just the id. Can be either 
            'resource' or 'member'. Defaults to None.  
            order (str, optional): Either 'asc' or 'desc'. Defaults to 'desc'.

        Returns:
            Union[Dict, List]: _description_
        """
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        url_path = f'/bookings/export?order={order}'
        if state and state in ['pending', 'confirmed', 'cancelled']:
            url_path += f'&state={state}'
        elif state:
            raise KeyError(state)
        if resolve and resolve in ['resource', 'member']:
            url_path += f'&resolve={resolve}'
        elif resolve:
            raise KeyError(resolve)
        if account:
            url_path += f'&account={account}'
        if space:
            url_path += f'&space={space}'
        if resource:
            url_path += f'&resource={resource}'
        if member:
            url_path += f'&member={member}'
        if fromDateTime:
            url_path += f'&fromDateTime={fromDateTime}'
        if untilDateTime:
            url_path += f'&untilDateTime={untilDateTime}'
        return self.__get(url_path)
    
    def get_bridge_commands(self, id: int, wait: bool = False) -> Union[Dict, List]:
        """Get a list of bridge commands for the provided ID.

        Args:
            id (int): ID of the bridge to query
            wait (bool, optional): Wait for an update on the command before returning. Defaults to False.

        Returns:
            Union[Dict, List]: Returns a list of commands for the bridge
        """
        url_path = f'/bridge-commands/{id}&wait={wait}'
        return self.__get(url_path)
    
    def get_charges(self, account: Optional[str] = None, member: Optional[str] = None, limit: int = 50, offset: int = 0, 
                    resourceLog: Optional[int] = None, booking: Optional[int] = None, onlyInvoiced: bool = True, 
                    fromDateTime: Optional[str] = None, untilDateTime: Optional[str] = None, 
                    order: str = 'asc') -> Union[Dict, List]:
        """Get a list of charges from the Fabman API.

        Args:
            account (Optional[str], optional): Account number to be queried. Defaults to None.
            member (Optional[str], optional): Member number who is being charged. Defaults to None.
            limit (int, optional): number of charges to be returned. Defaults to 50.
            offset (int, optional): Offset of the page. Can be used for pagination, but consumers should use the next 
            page link provided by the API. Defaults to 0.
            resourceLog (Optional[int], optional): ResourceLog to be queried. Defaults to None.
            booking (Optional[int], optional): ID of booking to be charged. Defaults to None.
            onlyInvoiced (bool, optional): Only return charges which have been invoiced. Defaults to True.
            fromDateTime (Optional[str], optional): Start datetime of query. Defaults to None.
            untilDateTime (Optional[str], optional): End datetime of query. Defaults to None.
            order (str, optional): Order of results. Defaults to 'asc'.

        Returns:
            Union[Dict, List]: List of charges matching the query
        """
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        url_path = f'/charges?limit={limit}&offset={offset}&order={order}&onlyInvoiced={onlyInvoiced}'
        if account:
            url_path += f'&account={account}'
        if member:
            url_path += f'&member={member}'
        if resourceLog:
            url_path += f'&resourceLog={resourceLog}'
        if booking:
            url_path += f'&booking={booking}'
        if fromDateTime: 
            url_path += f'&fromDateTime={fromDateTime}'
        if untilDateTime:
            url_path += f'&untilDateTime={untilDateTime}'
        return self.__get(url_path)
        
    def get_charge_by_id(self, id: int) -> Union[Dict, List]:
        """Returns a single charge given an ID

        Args:
            id (int): ID of the charge to be queried

        Returns:
            Union[Dict, List]: Object describing the queried charge
        """
        url_path = f'/charges/{id}'
        return self.__get(url_path)
    
    def get_countries(self) -> Union[Dict, List]:
        """Returns list of country codes and appropriate VAT settings where applicable.
        """
        url_path = '/countries'
        return self.__get(url_path)
    
    def get_currencies(self) -> Union[Dict, List]:
        """Returns List of currency abbreviations, names, and symbols for countries around the world.
        """
        url_path = '/currencies'
        return self.get(url_path)