#!/usr/bin/python3
"""Main file for the Fabman API library.
"""

#  TODO: Sanitize datetime inputs to ensure they are appropriate
#  TODO: Check 429 responses for retry-after headers
#  TODO: refactor accounts to not use **kwargs, instead giving all possible arguments as keyword arguments
#  TODO: better implement fields such as state which can be provided as a list and have multiple values
#  TODO: check automatic boolean values.
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

ORDERS = ['asc', 'desc']


class Fabman:
    """Main Fabman class. All interaction with the library should be done through this class.
    """

    
    def __init__(self, api_token: str) -> None:
        self.__api_token: str = api_token
        self.__base_url: str = 'https://fabman.io/api/v1'

    ##  Begin Helper Functions
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
        elif response.status_code == 403:
            raise Exception('Insufficient permissions')
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
        elif response.status_code == 403:
            raise Exception('Insufficient permissions')
        elif response.status_code == 404:
            raise Exception('Not found')
        elif response.status_code == 429:
            logger.warning("Rate limit exceeded. Retrying in 60 seconds.")
            # TODO: investigate 429 message from fabman to see if it includes a retry-after header
            time.sleep(60)
            return self.__post(path, data)
        return response.json()
    
    def __check_arg_array(self, provided: Union[List, str, int], valid: Union[List, list], arg_name: str) -> str:
        """Used to check array arguments which can have a combinatoric number of values.

        Args:
            provided (Union[List, str, int]): List of args to be checked
            valid (Union[List, list]): The valid possibilities for the argument
            arg_name (str): The argument name

        Returns:
            str: string to be appendeded onto the url path
        """
        out = ""
        if isinstance(provided, list):
            for item in provided:
                if item not in valid:
                    raise KeyError(f'{item} is not a valid value for {arg_name}')
            return f'&{arg_name}={"&{arg_name}=".join(provided)}'
        
        if isinstance(provided, str) and provided in valid:
            return f'&{arg_name}={provided}'
        else:
            raise KeyError(f'{provided} is not a valid value for {arg_name}')

    ##  End Helper Functions
    ##  Begin API GET Functions
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

    def get_accounts(self, limit: int = 50, offset: Optional[int] = None, embed: Optional[List[str]] = None, 
                     q: str = None, eq: str = None, trial: Optional[bool] = None, countryCode: Optional[str] = None, 
                     orderBy: str = 'name', order: str = 'asc', deleted: Optional[bool] = None) -> Union[Dict, List]:
        """Returns a list of accounts matching the query parameters.
        
        Args:
            limit (int, optional): Number of accounts to return. Defaults to 50.
            offset (Optional[int], optional): Offset of the page. Defaults to None.
            embed (Optional[List[str]], optional): Embed additional information in the returned information. Only valid
            argument is spaces. Defaults to None
            q (str, optional): Search string to search notes or other information on the account. Defaults to None.
            eq (str, optional): Extended search string to search notes or other information on the account. Includes 
            fields from Admin and Owner members. Defaults to None.
            trial: Return only accounts in trial or not in trial (omit for both). Defaults to None
            countryCode: Return only accounts in a specific country. Default is None
            orderBy (str, optional): How to order the return list. Valid options are id, name, plan, createdAt, or 
            trialEndDate. Defaults to 'name'.
            order (str, optional): Return list in descending or ascending order. Defaults to 'asc'.
            deleted (Optional[bool], optional): Return only deleted or not deleted accounts. Defaults to None.
            
        Returns
            Union[Dict, List]: _description_
        """
        embeds = ['spaces']
        if order not in ORDERS:
            raise KeyError(order)
        url_path = f'/accounts?limit={limit}&orderBy={orderBy}&order={order}'
        if offset:
            url_path += f'&offset={offset}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        if q:
            url_path += f'&q={q}'
        if eq:
            url_path += f'&eq={eq}'
        if trial is not None:
            url_path += f'&trial={str(trial).lower()}'
        if countryCode:
            url_path += f'&countryCode={countryCode}'
        if deleted is not None:
            url_path += f'&deleted={str(deleted).lower()}'
            
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
        states = ['pending', 'confirmed', 'cancelled']
        resolves = ['resource', 'member']
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        url_path = f'/bookings?order={order}&limit={limit}&offset={offset}&summary={summary}'
        if state:
            url_path += self.__check_arg_array(state, states, 'state')
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
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
        embeds = ['member', 'resource']
        url_path = f'/bookings/{id}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')

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
        states = ['pending', 'confirmed', 'cancelled']
        resolves = ['resource', 'member']
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        url_path = f'/bookings/export?order={order}'
        if state:
            url_path += self.__check_arg_array(state, states, 'state')
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
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
        return self.__get(url_path)

    def get_firmwares(self, limit: int = 50, offset: Optional[int] = None) -> Union[Dict, List]:
        """Returns a list of firmwares

        Args:
            limit (int, optional): Number of firmwares to return. Defaults to 50.
            offset (int, optional): Offset of the page. Defaults to 0.

        Returns:
            Union[Dict, List]: List of firmwares
        """
        
        url_path = f'/firmwares?limit={limit}'
        if offset and offset >= 0:
            url_path += f'&offset={offset}'
        elif offset:
            raise KeyError("Offset must be positive!")
        return self.__get(url_path)
    
    def get_firmware_by_id(self, id: int) -> Union[Dict, List]:
        """Return information about a single firmware

        Args:
            id (int): ID of the firmware being queried

        Returns:
            Union[Dict, List]: Dictionary of firmware information
        """
        
        url_path = f'/firmwares/{id}'
        return self.__get(url_path)
    
    def get_invoices(self, account: Optional[int] = None, member: Optional[int] = None, fromDate: Optional[str] = None, 
                     untilDate: Optional[str] = None, state: Optional[List[str]] = None, balanced: Optional[bool] = None, 
                     q: Optional[str] = None, resolve: Optional[List[str]] = None, orderBy: str = 'date', 
                     order: str = 'desc', limit: int = 50, offset: int = 0, summary: bool = False) -> Union[Dict, List]:
        """Returns a list of invoices matching the query.

        Args:
            account (Optional[int], optional): Account number issuing the invoices. Defaults to None.
            member (Optional[int], optional): Member id number who owes the invoice. Defaults to None.
            fromDate (Optional[str], optional): Start date of search. Defaults to None.
            untilDate (Optional[str], optional): End date of search. Defaults to None.
            state (Optional[List[str]], optional): State of the invoice, multiple values are possible. Should be a list 
            of of the following possible states: unpaid, pending, processing, paid, or cancelled. Defaults to None.
            balanced (Optional[bool], optional): Se to false to fetch only invoices where paid != totalPayable. Defaults to None.
            q (Optional[str], optional): Search string to search notes or other information on the invoice. Defaults to None.
            resolve (Optional[List[str]], optional): Return relationship details instead of just the id. Current only 
            valid value is member. Defaults to None.
            orderBy (str, optional): How to order the return list. Defaults to 'date'.
            order (str, optional): Return list in descending or ascending order. Defaults to 'desc'.
            limit (int, optional): Number of items returned in the list. Defaults to 50.
            offset (int, optional): Offset within the returned list. Defaults to 0.
            summary (bool, optional): Add headers with summary information about the found records. Defaults to False.

        Returns:
            Union[Dict, List]: List of invoice details matching the query.
        """
        states = ['unpaid', 'pending', 'processing', 'paid', 'cancelled']
        resolves = ['member']
        url_path = f'/invoices?limit={limit}&offset={offset}&orderBy={orderBy}&order={order}&summary={str(summary).lower()}'
        if account:
            url_path += f'&account={account}'
        if member:
            url_path += f'&member={member}'
        if fromDate:
            url_path += f'&fromDate={fromDate}'
        if untilDate:
            url_path += f'$untilDate={untilDate}'
        if state:
            url_path += self.__check_arg_array(state, states, 'state')
        if balanced is not None:
            url_path += f'&balanced={str(balanced).lower()}'
        if q:
            url_path += f'&q={q}'
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
        return self.__get(url_path)
    
    def get_invoice_by_id(self, id: int, embed: Optional[List[str]] = None) -> Union[Dict, List]:
        """Returns details about a specific invoice

        Args:
            id (int): Invoice ID to be queries
            embed (Optional[List[str]], optional): List which allows embedding related entities to reduce the number of 
            requests needed. Can be any combination of details, member, payments, and cancelledInvoice. Defaults to None.

        Returns:
            Union[Dict, List]: Dictionary of invoice.
        """
        embeds = ['details', 'member', 'payments', 'cancelledInvoice']
        url_path = f'/invoices/{id}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
            
        return self.__get(url_path)
                
    def get_invoice_details_by_id(self, id: int) -> Union[Dict, List]:
        """Returns details of particular invoice ID

        Args:
            id (int): Id of invoice to be queried

        Returns:
            Union[Dict, List]: Dictionary of invoice details
        """
        url_path = f'/invoices/{id}/details'
        return self.__get(url_path)
    
    def get_invoices_export(self, account: Optional[int] = None, member: Optional[int] = None, 
                            fromDate: Optional[str] = None, untilDate: Optional[str] = None, state: Optional[List[str]] = None, 
                            balanced: Optional[bool] = None, q: Optional[str] = None, resolve: Optional[List[str]] = None, 
                            orderBy: str = 'date', order: str = 'desc') -> Union[Dict, List]:
        """Returns a download link for invoice information matching the query in a CSV format.

        Args:
            account (Optional[int], optional): Account number issuing the invoices. Defaults to None.
            member (Optional[int], optional): Member id number who owes the invoice. Defaults to None.
            fromDate (Optional[str], optional): Start date of search. Defaults to None.
            untilDate (Optional[str], optional): End date of search. Defaults to None.
            state (Optional[List[str]], optional): State of the invoice, multiple values are possible. Should be a list 
            of of the following possible states: unpaid, pending, processing, paid, or cancelled. Defaults to None.
            balanced (Optional[bool], optional): Se to false to fetch only invoices where paid != totalPayable. Defaults to None.
            q (Optional[str], optional): Search string to search notes or other information on the invoice. Defaults to None.
            resolve (Optional[List[str]], optional): Return relationship details instead of just the id. Current only 
            valid value is member. Defaults to None.
            orderBy (str, optional): How to order the return list. Defaults to 'date'.
            order (str, optional): Return list in descending or ascending order. Defaults to 'desc'.

        Returns:
            Union[Dict, List]: Download link for CSV file
        """
        states = ['unpaid', 'pending', 'processing', 'paid', 'cancelled']
        resolves = ['member']
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        if orderBy not in ['number', 'date', 'totalWithFees', 'state']:
            raise KeyError(orderBy)
        url_path = f"/invoices/export?orderBy={orderBy}&order={order}"
        if account:
            url_path += f'&account={account}'
        if member:
            url_path += f'&member={member}'
        if fromDate:
            url_path += f'&fromDate={fromDate}'
        if untilDate:
            url_path += f'$untilDate={untilDate}'
        if state:
            url_path += self.__check_arg_array(state, states, 'state')
        if balanced is not None:
            url_path += f'&balanced={str(balanced).lower()}'
        if q:
            url_path += f'&q={q}'
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
        return self.__get(url_path)
        
    def get_jobs(self, limit: int = 50, offset: int = None, account: Optional[int] = None, type: Optional[str] = None, 
                 state: Optional[Union[List[str], str]] = None) -> Union[List, Dict]:
        """Returns list of jobs matching the query parameters.

        Args:
            limit (int, optional): Number of jobs to return. Defaults to 50.
            offset (int, optional): Offset within the returned list of jobs. Defaults to None.
            account (Optional[int], optional): Account number of the space. Defaults to None.
            type (Optional[str], optional): Type of job to be returned. Can be either 'invoices' or 'payments'. Defaults to None.
            state (Optional[List[str]], optional): State of jobs to be returned. Can be any combination of pending, done, or failed. Defaults to None.

        Returns:
            Union[List, Dict]: _description_
        """
        states = ['pending', 'done', 'failed']
        if type and type not in ['invoices', 'payments']:
            raise KeyError(type)
        if state and isinstance(state, list):
            for st in state:
                if st not in ['pending', 'done', 'failed']:
                    raise KeyError(st)
        elif state and isinstance(state, str):
            if state not in ['pending', 'done', 'failed']:
                raise KeyError(state)
        
        url_path = f'/jobs?limit={limit}'
        if offset:
            url_path += f'&offset={offset}'
        if account:
            url_path += f'&account={account}'
        if type:
            url_path += f'&type={type}'
        if state and isinstance(state, list):
            url_path += self.__check_arg_array(state, states, 'state')
        
        return self.__get(url_path)
        
    def get_job_by_id(self, id: int, wait: bool = False) -> Union[List, Dict]:
        """Returns information of a single job given an ID.

        Args:
            id (int): ID of the job to be queried
            wait (bool, optional): Wait for an update on the job before returning. Defaults to False.

        Returns:
            Union[List, Dict]: Information about a particular job
        """
        if not isinstance(wait, bool):
            raise TypeError(wait)
        url_path = f'/jobs/{id}?wait={wait}'
        return self.__get(url_path)
        
    def get_locales(self) -> Union[List, Dict]:
        """Returns a list of locales recognized by Fabman.
        """
        url_path = '/locales'
        return self.__get(url_path)
    
    def get_member_invitations(self, token: str) -> Union[List, Dict]:
        """Returns information about a member invitation given the invitation token string.

        Args:
            token (str): Token string of the invitation

        Returns:
            Union[List, Dict]: Information about the invitation
        """
        url_path = f"/member-invitations/{token}"
        return self.__get(url_path)
    
    def get_members(self, account: Optional[int] = None, keyType: Optional[str] = None, keyToken: Optional[str] = None, 
                    embed: Optional[List[str]] = None, packages: Optional[List[int]] = None, 
                    privileges: Optional[str] = None, trainingCourses: Optional[List[str]] = None, q: Optional[str] = None,
                    metadataKey: Optional[List[str]] = None, metadataValue: Optional[List[str]] = None, 
                    memberNumber: Optional[str] = None, paidForBy: Optional[int] = None, orderBy: str = 'name', 
                    order: str = 'asc', limit: int=50, offset: Optional[int] = None) -> Union[List, Dict]:
        """Returns list of members matching the query parameters.

        Args:
            account (Optional[int], optional): Account number that the member belongs. Defaults to None, indicating the account of the api key used.
            keyType (Optional[str], optional): String indicating the key type of the keyToken field. Must be one of em4102,
            nfca, nfcb, nfcf, iso15693, or hid. Defaults to None. Required if keyToken field is supplied
            keyToken (Optional[str], optional): Search for members via access key token. Must be between 4 and 18 bytes, 
            depending on the key type, as a hexadecimal string. Defaults to None.
            embed (Optional[List[str]], optional): Allows embedding of related entities to reduce the number of requests 
            needed. Can be any combination of memberPackages, activePackages, privileges, and trainings. Defaults to None.
            packages (Optional[List[int]], optional): Search for members who currently have all the given packages. Use 
            "none" to search for members without any active package and "any" to search for members with any active package. Defaults to None, which specifies "any".
            privileges (Optional[str], optional): Return members matching the given privilege. If specified, must be one 
            of member, admin, owner. Defaults to None.
            trainingCourses (Optional[List[str]], optional): Search for members who have participated in all of the given
            training courses by the training course ids. Defaults to None.
            q (Optional[str], optional): Search String. Defaults to None.
            metadataKey (Optional[List[str]], optional): Use with metadataValue to search for members who have that given 
            metadata key containing that value. Can be specified multiple times. Defaults to None.
            metadataValue (Optional[List[str]], optional): Use with metadataKey to search for members who have that given 
            metadata key containing that value. Can be specified multiple times. Defaults to None.
            memberNumber (Optional[str], optional): Search for member given a member number. Defaults to None.
            paidForBy (Optional[int], optional): Search for members who are paid for by a given entity. Defaults to None.
            orderBy (str, optional): Field to order by. Must be either name or memberNumber . Defaults to 'name'.
            order (str, optional): Order of results. Must be either 'asc' or 'desc'. Defaults to 'asc'.
            limit (int, optional): Number of results to return. Defaults to 50.
            offset (Optional[int], optional): Offset of start of returned values. Defaults to None.

        Returns:
            Union[List, Dict]: List of Member objects which match the query
            
        TODO: generate and return Member objects rather than raw data
        """
        
        embeds = ['memberPackages', 'activePackages', 'privileges', 'trainings']
        if order not in ['asc', 'desc']:
            raise KeyError(order)
        if orderBy not in ['name', 'memberNumber']:
            raise KeyError(order)
        if (keyType and keyToken is None) or (keyType is None and keyToken):
            raise KeyError("keyType and keyToken must be specified together")        
        if (metadataKey and metadataValue is None) or (metadataKey is None and metadataValue):
            raise KeyError("metadataKey and metadataValue must be specified together")
        elif len(metadataKey) != len(metadataValue):
            raise KeyError("metadataKey and metadataValue must be the same length")
        
        url_path = f'/members?limit={limit}&orderBy={orderBy}&order={order}'
        if account:
            url_path += f'&account={account}'
        if keyType and keyToken:
            url_path += f'&keyType={keyType}&keyToken={keyToken}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        if packages and isinstance(packages, list):
            for p in packages:
                url_path += f'&packages={p}'
        elif packages:
            url_path += f'&packages={packages}'
        if privileges and privileges in ['member', 'admin', 'owner']:
            url_path += f'&privileges={privileges}'
        elif privileges:
            raise KeyError(privileges)
        if trainingCourses and isinstance(trainingCourses, list):
            for t in trainingCourses:
                url_path += f'&trainingCourses={t}'
        elif trainingCourses:
            url_path += f'&trainingCourses={trainingCourses}'
        if q:
            url_path += f'&q={q}'
        if metadataKey and isinstance(metadataKey, list):
            for k, v in zip(metadataKey, metadataValue):
                url_path += f'&metadataKey={k}&metadataValue={v}'
        elif metadataKey:
            url_path += f'&metadataKey={metadataKey}&metadataValue={metadataValue}'
        if memberNumber:
            url_path += f'&memberNumber={memberNumber}'
        if paidForBy:
            url_path += f'paidForBy={paidForBy}'
        if offset:
            url_path += f'&offset={offset}'
        
        return self.__get(url_path)
            
    def get_member_by_id(self, id: int, embed: Optional[List[str]] = None, keyToken: bool=False) -> Union[List, Dict]:
        """Returns a specific member given an ID.

        Args:
            id (int): ID of the member in question
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. Must be any combination of memberPackages, trainings, privileges, key, device, and invitation. Defaults to None.
            keyToken (bool, optional): When embedding Keys: whether to also return the key's token. Defaults to False.

        Returns:
            Union[List, Dict]: Data dictionary of Member information
            
        """
        embeds = ['memberPackages', 'trainings', 'privileges', 'key', 'device', 'invitation']
        
        url_path = f'/members/{id}'
        
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        return self.__get(url_path)
            
    def get_member_balance_items(self, id: int) -> Union[List, Dict]:
        """Returns the balance items of the given member

        Args:
            id (_type_): ID of the member in question.

        Returns:
            Union[List, Dict]: List of balance items for the member
        """
        url_path = f'/members/{id}/balance-items'
        return self.__get(url_path)
    
    def get_member_changes(self, id: int, limit: int = 50, offset: Optional[int] = None, resolve: Optional[List[str]] = None) -> Union[List, Dict]:
        """Get list of changes for a given member

        Args:
            id (int): ID of the member in question
            limit (int, optional): Number of changes to return. Defaults to 50.
            offset (Optional[int], optional): Offset of the start of the returned list . Defaults to None.
            resolve (Optional[List[str]], optional): Return relationship details instead of just the id. Only acceptable
            value is updatedBy, though left as a List for future implementations.. Defaults to None.

        Returns:
            Union[List, Dict]: Returns list of changes
        """
        resolves = ['updatedBy']
        
        url_path = f'/members/{id}/changes?limit={limit}'
        if offset:
            url_path += f'&offset={offset}'
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')

        return self.__get(url_path)
    
    def get_member_credits(self, id: int, limit: int = 50, offset: Optional[int] = None, predict: bool = False, 
                           status: str = 'active') -> Union[List, Dict]:
        """Get list of credits for a given member

        Args:
            id (int): ID of member in question
            limit (int, optional): Number of credits to return. Defaults to 50.
            offset (Optional[int], optional): Offset inside of return lists. Defaults to None.
            predict (bool, optional): Undocumented in the Fabman API. Defaults to False.
            status (str, optional): Status of the credit. Must be either active, previous, or all. Defaults to 'active'.

        Returns:
            Union[List, Dict]: _description_
        """
        if status not in ['active', 'previous', 'all']:
            raise KeyError(status)
        
        url_path = f'/members/{id}/credits?limit={limit}&predict={str(predict).lower()}&status={status}'
        if offset:
            url_path += f'offset={offset}'
            
        return self.__get(url_path)
    
    def get_member_credits_by_credit_id(self, id: int, creditId: int, embed: Optional[List[str]] = None) -> Union[List, Dict]:
        """Get a information about a specific credit given a member ID and credit ID

        Args:
            id (int): ID of member in question.
            creditId (int): ID of credit in question.
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. Only acceptable value is currently memberPackage Defaults to None.

        Returns:
            Union[List, Dict]: returns information on the requested Credit
        """
        
        embeds = ['memberPackage']
        url_path = f"/members/{id}/credits/{creditId}"
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')

        return self.__get(url_path)
    
    def get_member_credit_uses_by_credit_id(self, id: int, creditId: int, limit: int = 50, offset: Optional[int] = None) -> Union[List, Dict]:
        """Returns a list of uses by member of a specific creditId

        Args:
            id (int): ID of the member in question
            creditId (int): ID of the credit in question
            limit (int, optional): Number of uses to be returned. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of returned items. Defaults to None.

        Returns:
            Union[List, Dict]: List of uses of the credit
        """
        url_path = f'/members/{id}/credits/{creditId}/uses?limit={limit}'
        if offset:
            url_path += f'&offset={offset}'
        return self.__get(url_path)
    
    def get_member_device(self, id: int, limit: int = 50, offset: Optional[int] = None) -> Union[List, Dict]:
        """Returns a device associated with a member

        Args:
            id (int): ID of the member in question

        Returns:
            Union[List, Dict]: List of devices associated with the member
        """
        url_path = f'/members/{id}/device?id={id}'
        return self.__get(url_path)
    
    def get_member_device_changes(self, id: int, limit: int = 50, since: Optional[str] = None, offset: Optional[int] = None) -> Union[List, Dict]:
        """Returns a list of changes to a given device associated with a user.

        Args:
            id (int): ID of the member in question
            limit (int, optional): Number of changes to be returned by the API. Defaults to 50.
            since (Optional[str], optional): Start date of the query. Will return all changes since given date. Defaults to None.
            offset (Optional[int], optional): Offset within the list of changes. Defaults to None.

        Returns:
            Union[List, Dict]: Returns list of changes 
            
        TODO: datetime checking on since
        """
        
        url_path = f'/members/{id}/device/changes?limit={limit}'
        if since:
            url_path += f'&since={since}'
        if offset:
            url_path += f'&offset={offset}'
        return self.__get(url_path)
    
    def get_member_export(self, id: int) -> Union[List, Dict]:
        """Exports all stored data for that user in a text/csv format

        Args:
            id (int): ID of member

        Returns:
            Union[List, Dict]: Download string for a csv file
        """
        url_path = f"/members/{id}/export"
        return self.__get(url_path)
    
    def get_member_invitation(self, id:int) -> Union[List, Dict]:
        """Get member invitation information for a given member

        Args:
            id (int): ID of the member in question.

        Returns:
            Union[List, Dict]: Information about the invitation.
        """
        url_path = f"/members/{id}/invitation"
        return self.__get(url_path)
    
    def get_member_key(self, id: int, keyToken: bool = False) -> Union[List, Dict]:
        """Return the member's key information

        Args:
            id (int): ID of the member in question
            keyToken (bool, optional): Whether to also return the key's token. Defaults to False.

        Returns:
            Union[List, Dict]: Key information for the member
        """
        
        url_path = f'/members/{id}/key?keyToken={str(keyToken).lower()}'
        return self.__get(url_path)
    
    #TODO: finish the minutia of get member api endpoints
    
    def get_payments(self, account: Optional[int] = None, member: Optional[int] = None, fromDate: Optional[str] = None, 
                    untilDate: Optional[str] = None, state: Optional[List[str]] = None, memberInitiated: bool = False,
                    resolve: Optional[List[str]] = None, orderBy: str = 'date', order: str = 'desc', limit: int = 50,
                    offset: Optional[int] = None, summary: bool = False) -> Union[List, Dict]:
        """Returns a list of payments matching the query parameters.

        Args:
            account (Optional[int], optional): Account number payments are rendered to. If unspecified, defaults to the holder of the API key. Defaults to None.
            member (Optional[int], optional): Refine search by member ID. Defaults to None.
            fromDate (Optional[str], optional): Start date of search. Defaults to None.
            untilDate (Optional[str], optional): End date of search. Defaults to None.
            state (Optional[List[str]], optional): State of the payment. Can be any combination of pending, processing, succeeded, and failed. Defaults to None.
            memberInitiated (bool, optional): Include member-initiated, but incomplete, payments. Defaults to False.
            resolve (Optional[List[str]], optional): Return relationship details instead of just the id. Only available option is member. Defaults to None.
            orderBy (str, optional): Ordering option of returned results. Can be one of date, total, or state. Defaults to 'date'.
            order (str, optional): Order of the returned results. Can be 'asc' or 'desc'. Defaults to 'desc'.
            limit (int, optional): Max number of results to be returned. Defaults to 50.
            offset (Optional[int], optional): Offset in the list of returns. Defaults to None.
            summary (bool, optional): add headers with summary information about the found records. Defaults to False.

        Returns:
            Union[List, Dict]: Returns a list of payments with their information
        """
        states = ['pending', 'processing', 'succeeded', 'failed']
        resolves = ['member']
        order_bys = ['date', 'total', 'state']
        if limit < 0:
            raise KeyError(limit)
        
        if order not in ORDERS:
            raise KeyError(order)
        if orderBy not in order_bys:
            raise KeyError(orderBy)
        
        url_path = f'/payments?limit={limit}&orderBy={orderBy}&order={order}&summary={str(summary).lower()}&memberInitiated={str(memberInitiated).lower()}'
        
        if account:
            url_path += f'&account={account}'
        if member:
            url_path += f'&member={member}'
        if fromDate:
            url_path += f'&fromDate={fromDate}'
        if untilDate:
            url_path += f'$untilDate={untilDate}'
        if state:
            url_path += self.__check_arg_array(state, states, 'state')
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
        if offset:
            url_path += f'&offset={offset}'
        
        return self.__get(url_path)
    
    def get_payment_by_id(self, id: int, embed: Optional[List[str]] = None, wait: bool = False) -> Union[List, Dict]:
        """Returns information about a particular payment given its ID.

        Args:
            id (int): ID of payment in question
            embed (Optional[List[str]], optional): Allows embedding of related entities to reduce the number of requests 
            needed. Only available option is invoices. Defaults to None.
            wait (bool, optional): Wait for an update on payment intent belonging to that payment before returning. Defaults to False.

        Returns:
            Union[List, Dict]: Information about a particular payment
        """
        
        embeds = ['invoices']
        url_path = f'/payments/{id}?wait={str(wait).lower()}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        
        return self.__get(url_path)
    
    def get_payments_by_token(self, token: str, embed: Optional[List[str]] = None, wait: bool = False) -> Union[List, Dict]:
        """Returns payment information given a token

        Args:
            token (str): Token for payment in question
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of requests needed. Can be any combination of invoices and account. Defaults to None.
            wait (bool, optional): Wait for an update on payment intent belonging to that payment before returning. Defaults to False.

        Returns:
            Union[List, Dict]: payment information
        """
        
        embeds = ['invoices', 'account']
        url_path = f'/payments/{token}?wait={str(wait).lower()}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        
        return self.__get(url_path)
    
    def get_qr(self, code: str) -> Union[List, Dict]:
        """Get information of a QR code given the code

        Args:
            code (str): Code of the QR in question

        Returns:
            Union[List, Dict]
        """
        url_path = f'/qr/{code}'
        return self.__get(url_path)
    
    def get_resource_logs(self, account: Optional[int] = None, space: Optional[int] = None, 
                          resource: Optional[int] = None, member: Optional[int] = None, _from: Optional[str] = None, 
                          until: Optional[str] = None, status: str = 'all', type: Optional[List[str]] = None, 
                          resolve: Optional[List[str]] = None, order: str = 'desc', limit: int = 50, 
                          offset: Optional[int] = None, summary: bool = False) -> Union[List, Dict]:
        """Return list of logs matching the query parameters.

        Args:
            account (Optional[int], optional): Account number in control of the logs. If not specified, defaults to the 
            account of the API token holder. Defaults to None.
            space (Optional[int], optional): ID of the space in questions. Defaults to None.
            resource (Optional[int], optional): ID of a particular resource in question. Defaults to None.
            member (Optional[int], optional): ID of a particular member in question. Defaults to None.
            _from (Optional[str], optional): Beginning date of the logs. Defaults to None.
            until (Optional[str], optional): End date of the logs. Defaults to None.
            status (Optional[str], optional): Status of the logs. Can be one of all, active, or complete. Defaults to 'all''.
            type (Optional[List[str]], optional): Type of log to be returned. Can be any combination of denied, allowed, 
            pairing, keyAssigned, checkIn, reboot, offline, resourceDisabled, or resourceEnabled. Defaults to None.
            resolve (Optional[List[str]], optional): Return relationship details instead of just the id. Can be any 
            combination of resource, member, or originalMember. Defaults to None.
            order (str, optional): Order of the returned list of logs. Defaults to 'desc'.
            limit (int, optional): Number of log items to be returned. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of returned logs.. Defaults to None.
            summary (bool, optional): Add headers with summary information about the found records. Defaults to False.

        Returns:
            Union[List, Dict]: List of resource log items
        """
        
        types = ['denied', 'allowed', 'pairing', 'keyAssigned', 'checkIn', 'reboot', 'offline', 'resourceDisabled', 'resourceEnabled']
        resolves = ['resource', 'member', 'originalMember']
        if order not in ORDERS:
            raise KeyError(order)
        
        url_path = f'/resource-logs?limit={limit}&order={order}&summary={str(summary).lower()}'
        if account:
            url_path += f'&account={account}'
        if space:
            url_path += f'&space={space}'
        if resource:
            url_path += f'&resource={resource}'
        if member:
            url_path += f'&member={member}'
        if _from:
            url_path += f'&from={_from}'
        if until:
            url_path += f'&until={until}'
        if status and status in ['all', 'active', 'complete']:
            url_path += f'&status={status}'
        elif status:
            raise KeyError(status)
        if type:
            url_path += self.__check_arg_array(type, types, 'type')
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
        if offset:
            url_path += f'&offset={offset}'
            
        return self.__get(url_path)
    
    def get_resource_logs_by_id(self, id: int, embed: Optional[List[str]] = None) -> Union[List, Dict]:
        """Return information about a particular resource log given an ID

        Args:
            id (int): ID of the resource log in question
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. Can be any combination of resource, member, originalMember, charges, or creditUses. Defaults to None.

        Returns:
            Union[List, Dict]: Resource log item specified by the ID
        """
        embeds = ['resource', 'member', 'originalMember', 'charges', 'creditUses']
        url_path = f'/resource-logs/{id}'
        
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
            
        return self.__get(url_path)
    
    def get_resource_logs_export(self, account: Optional[int] = None, space: Optional[int] = None, 
                                 resource: Optional[int] = None, member: Optional[int] = None, _from: Optional[str] = None,
                                 until: Optional[str] = None, status: str = 'all', type: Optional[List[str]] = None, 
                                 resolve: Optional[List[str]] = None, order: str = 'desc') -> Union[List, Dict]:
        """Returns a blob as 'text/csv' with all logs matching the query parameters.

        Args:
            account (Optional[int], optional): Account number in control of the logs. If not specified, defaults to the 
            account of the API token holder. Defaults to None.
            space (Optional[int], optional): ID of the space in questions. Defaults to None.
            resource (Optional[int], optional): ID of a particular resource in question. Defaults to None.
            member (Optional[int], optional): ID of a particular member in question. Defaults to None.
            _from (Optional[str], optional): Beginning date of the logs. Defaults to None.
            until (Optional[str], optional): End date of the logs. Defaults to None.
            status (Optional[str], optional): Status of the logs. Can be one of all, active, or complete. Defaults to 'all''.
            type (Optional[List[str]], optional): Type of log to be returned. Can be any combination of denied, allowed, 
            pairing, keyAssigned, checkIn, reboot, offline, resourceDisabled, or resourceEnabled. Defaults to None.
            resolve (Optional[List[str]], optional): Return relationship details instead of just the id. Can be any 
            combination of resource, member, or originalMember. Defaults to None.
            order (str, optional): Order of the returned list of logs. Defaults to 'desc'.

        Returns:
            Union[List, Dict]: _description_
        """
        
        types = ['denied', 'allowed', 'pairing', 'keyAssigned', 'checkIn', 'reboot', 'offline', 'resourceDisabled', 'resourceEnabled']
        resolves = ['resource', 'member', 'originalMember']
        if order not in ORDERS:
            raise KeyError(order)
        url_path = f'/resource-logs/export?order={order}'
        if account:
            url_path += f'&account={account}'
        if space:
            url_path += f'&space={space}'
        if resource:
            url_path += f'&resource={resource}'
        if member:
            url_path += f'&member={member}'
        if _from:
            url_path += f'&from={_from}'
        if until:
            url_path += f'&until={until}'
        if status and status in ['all', 'active', 'complete']:
            url_path += f'&status={status}'
        elif status:
            raise KeyError(status)
        if type:
            url_path += self.__check_arg_array(type, types, 'type')
        if resolve:
            url_path += self.__check_arg_array(resolve, resolves, 'resolve')
        
        return self.__get(url_path)
    
    def get_resource_types(self, account: Optional[int] = None, limit: int = 50, offset: Optional[int] = None) -> Union[List, Dict]:
        """List resource categories of a given account (previously simply called 'types')

        Args:
            account (Optional[int], optional): Account in question. If not specified, the account of the API token 
            holder is assumed. Defaults to None.
            limit (int, optional): Number of resource types to be returned. Defaults to 50.
            offset (Optional[int], optional): Offset in the list of types being returned. Defaults to None.

        Returns:
            Union[List, Dict]: list of resource types
        """
        
        url_path = f'/resource-types?limit={limit}'
        if account:
            url_path += f'&account={account}'
        if offset:
            url_path += f'&offset={offset}'
            
        return self.__get(url_path)
    
    def get_resources(self, limit: int = 50, offset: Optional[int] = None, account: Optional[int] = None, 
                      space: Optional[int] = None, type: Optional[int] = None, targetFirmware: Optional[List[int]] = None, 
                      exclusiveUsage: bool = False, embed: Optional[List[str]] = None, q: Optional[str] = None, 
                      eq: Optional[str] = None, orderBy: str = 'name', order: str = 'asc') -> Union[List, Dict]:
        """Return a list of resources given the query parameters

        Args:
            limit (int, optional): Number of resources to return. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of returned resources. Defaults to None.
            account (Optional[int], optional): Account in question. If not specified, the account of the API token 
            holder is assumed. Defaults to None.
            space (Optional[int], optional): Space containing the resources. Defaults to None.
            type (Optional[int], optional): Filter resources by container (requires resource type id). Defaults to None.
            targetFirmware (Optional[List[int]], optional): Filter resources by a specific firmware. Defaults to None.
            exclusiveUsage (bool, optional): Filter if the resource has exclusive Usage. Defaults to False.
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. Defaults to None.
            q (Optional[str], optional): Search string. Defaults to None.
            eq (Optional[str], optional): Extended search string (includes fields from Account and Bridge). Defaults to None.
            orderBy (str, optional): Which field to order the results. Can be one of name, type, or space . Defaults to 'name'.
            order (str, optional): Direction of the order. Defaults to 'asc'.

        Returns:
            Union[List, Dict]: List of resources
        """
        if order not in ORDERS:
            raise KeyError(order)
        embeds = ['bridge']
        url_path = f'/resources?limit={limit}&orderBy={orderBy}&order={order}&exclusiveUsage={str(exclusiveUsage).lower()}'
        if offset:
            url_path += f'&offset={offset}'
        if account:
            url_path += f'&account={account}'
        if space:
            url_path += f'&space={space}'
        if type:
            url_path += f'&type={type}'
        if targetFirmware and isinstance(targetFirmware, list):
            for tf in targetFirmware:
                url_path += f'&targetFirmware={tf}'
        elif targetFirmware:
            url_path += f'&targetFirmware={int(targetFirmware)}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        if q:
            url_path += f'&q={q}'
        if eq:
            url_path += f'&eq={eq}'
        
    def get_resource_by_id(self, id: int, embed: Optional[List[str]] = None) -> Union[List, Dict]:
        """Return information about a specific resource given its ID

        Args:
            id (int): ID of the resource in question
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. Can be any combination of bridge and trainingCourses. Defaults to None.

        Returns:
            Union[List, Dict]: Resource
        """
        embeds = ['bridge', 'trainingCourses']
        url_path = f'/resources/{id}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        
        return self.__get(url_path)
    
    def get_resource_bridge_by_id(self, id: int) -> Union[List, Dict]:
        """Return information about a specific bridge given its associated resource ID

        Args:
            id (int): ID of the resource in question

        Returns:
            Union[List, Dict]: Bridge
        """
        url_path = f'/resources/{id}/bridge'
        return self.__get(url_path)
    
    def get_resource_bridge_api_key_by_id(self, id: int) -> Union[List, Dict]:
        """Returns the api key of the bridge associated with the given resource

        Args:
            id (int): ID of the resource in question

        Returns:
            Union[List, Dict]: API key
        """
        url_path = f'/resources/{id}/bridge/api-key'
        return self.__get(url_path)
    
    def get_spaces(self, limit: int = 50, offset: Optional[int] = None, account: Optional[int] = None, 
                   embed: Optional[List[str]] = None) -> Union[List, Dict]:
        """Return a list of spaces given the query parameters

        Args:
            limit (int, optional): Number of spaces to be returned. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of results. Defaults to None.
            account (Optional[int], optional): Account in question. If not specified, the account of the API token 
            holder is assumed. Defaults to None.
            embed (Optional[List[str]], optional): Allows the embedding of entities to reduce the number of requests 
            needed. Can be any combination of openingHours and billingSettings. Defaults to None.

        Returns:
            Union[List, Dict]: List of Spaces
        """
        embeds = ['openingHours', 'billingSettings']
        url_path = f'/spaces?limit={limit}'
        if offset:
            url_path += f'&offset={offset}'
        if account:
            url_path += f'&account={account}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        return self.__get(url_path)
    
    def get_space_by_id(self, id: int, embed: Optional[List[str]] = None) -> Union[List, Dict]:
        """Return information of a specific space given its ID

        Args:
            id (int): ID of the space in question
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. can be any combination of openingHours, holidays, or billingSettings. Defaults to None.

        Returns:
            Union[List, Dict]: Information of the Space
        """
        embeds = ['openingHours', 'holidays', 'billingSettings']
        url_path = f'/spaces/{id}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        return self.__get(url_path)
    
    # TODO: finish the spaces minutia
    
    def get_training_courses(self, limit: int = 50, offset: Optional[int] = None, account: Optional[int] = None, 
                             resource: Optional[int] = None, archived: bool = False) -> Union[List, Dict]:
        """Return a list of training courses available to the account

        Args:
            limit (int, optional): Max number of training courses to return. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of returned training courses. Defaults to None.
            account (Optional[int], optional): Account in question. If not specified, the account of the API token 
            holder is assumed. Defaults to None.
            resource (Optional[int], optional): ID of a specific resource. Defaults to None.
            archived (bool, optional): Return archived training courses. Defaults to False.

        Returns:
            Union[List, Dict]: List of training courses
        """
        
        url_path = f'/training-courses?limit={limit}&archived={str(archived).lower()}'
        if offset:
            url_path += f'&offset={offset}'
        if account:
            url_path += f'&account={account}'
        if resource:
            url_path += f'&resource={resource}'
        
        return self.__get(url_path)
    
    def get_training_course_by_id(self, id:int) -> Union[List, Dict]:
        """Return information about a specific training course given its ID

        Args:
            id (int): ID of the training course in question

        Returns:
            Union[List, Dict]: Training course
        """
        url_path = f'/training-courses/{id}'
        retun self.__get(url_path)
    
    def get_current_user(self) -> Union[List, Dict]:
        """Returns information about the holder of the API token

        Returns:
            Union[List, Dict]: User information
        """
        url_path = self.__get('/user/me')
        return self.__get(url_path)
    
    def get_webhooks(self, limit: int = 50, offset: Optional[int] = None, account: Optional[int] = None) -> Union[List, Dict]:
        """Return a list of webhooks for the account

        Args:
            limit (int, optional): Max number of webhooks to return. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of returned webhooks. Defaults to None.
            account (Optional[int], optional): Account in question. If not specified, the account of the API token
            holder is assumed. Defaults to None.
            
        Returns:
            Union[List, Dict]: List of webhooks
        """
        url_path = f'/webhooks?limit={limit}'
        if offset:
            url_path += f'&offset={offset}'
        if account:
            url_path += f'&account={account}'
        
        return self.__get(url_path)
    
    def get_webhook_by_id(self, id: int, embed: Optional[List[str]] = None) -> Union[List, Dict]:
        """Return information about a specific webhook given its ID

        Args:
            id (int): ID of the webhook in question
            embed (Optional[List[str]], optional): Allows the embedding of related entities to reduce the number of 
            requests needed. Can be any combination of account and space. Defaults to None.

        Returns:
            Union[List, Dict]: Webhook
        """
        embeds = ['account', 'space']
        url_path = f'/webhooks/{id}'
        if embed:
            url_path += self.__check_arg_array(embed, embeds, 'embed')
        return self.__get(url_path)
    
    def get_webhook_events(self, id: int, limit: int = 50, offset: Optional[int] = None) -> Union[List, Dict]:
        """Return a list of events for a specific webhook
        
        Args:
            id (int): ID of the webhook in question
            limit (int, optional): Max number of events to return. Defaults to 50.
            offset (Optional[int], optional): Offset within the list of returned events. Defaults to None.
            
        Returns:
            Union[List, Dict]: List of events
        """
        url_path = f'/webhooks/{id}/events?limit={limit}'
        if offset:
            url_path += f'&offset={offset}'
        
        return self.__get(url_path)
    
    ## End GET methods
    ## Begin POST methods
    def create_api_key(self, label: str, member: int) -> Union[List, Dict]:
        """Creates a new API key for the member ID with a specified label. Returns information about the new API key. 
        The token can be retrieved by the `get_api_token()` method.

        Args:
            label (str): Label for the new api token
            member (int): Member ID who will be associated with the new token

        Returns:
            Union[List, Dict]: Information about the new api key.
        """
        data = {
            "label": label,
            "member": member
        }
        
        url_path = "/api-keys"
        return self.__post(url_path, data=data)
    
    def create_booking(self, resource: int, member: str, fromDateTime: str, untilDateTime: str, 
                       state: str = 'confirmed', ignoreMemberRestrictions: bool = False) -> Union[List, Dict]:
        """Creates a new booking for a member. Returns information about the new booking assuming the booking
        went through fine.

        Args:
            resource (int): Resource to be booked
            member (str): Member ID booking the resource
            fromDateTime (str): Start of the booking interval
            untilDateTime (str): End of the booking interval
            state (str, optional): State of the booking. Can be one of pending, confirmed, or cancelled. Defaults to 'confirmed'.
            ignoreMemberRestrictions (bool, optional): If you book as an admin for other members, you can opt to ignore 
            booking restrictions such as "this resource cannot be booked", booking windows, booking time limits, etc.
            Defaults to False.

        Returns:
            Union[List, Dict]: Confirmation information of the booking
        """
        if state not in ['confirmed', 'peding', 'cancelled']:
            raise KeyError(state)
        
        data = {
            "resource": resource,
            "member": member,
            "fromDateTime": fromDateTime,
            "untilDateTime": untilDateTime,
            "state": state,
            "ignoreMemberRestrictions": ignoreMemberRestrictions
        }
        url_path = "/bookings"
        return self.__post(url_path, data=data)
    
    # TODO: bridge endpoints? 
    def create_charges(self, member: int, description: str, price: float, dateTime: Optional[str] = None, 
                       details: Optional[str] = None, taxPercent: Optional[float] = None, resourceLog: Optional[int] = None, 
                       booking: Optional[int] = None) -> Union[List, Dict]:
        """Create a new charge for a member. Returns information about the new charge assuming the charge went through fine.

        Args:
            member (int): ID of the member to be charged
            description (str): brief description of the charge, limit to 255 characters
            price (float): Amount of the charge
            taxPercent (Optional[float]): Tax percentage of the charge.
            dateTime (Optional[str], optional): DateTime of the charge. Defaults to None.
            details (Optional[str], optional): Extended details of the charge, no limit on length. Defaults to None.
            resourceLog (Optional[int], optional): Resource Log id to be associated with the charge. Defaults to None.
            booking (Optional[int], optional): Booking ID to be associated with the charge. Defaults to None.

        Returns:
            Union[List, Dict]: Information about the new charge
        """
        
        if len(description) > 255:
            description = description[:255]
        
        data = {
            "member": member,
            "description": description,
            "price": price
        }
        
        if taxPercent:
            data['taxPercent'] = taxPercent
        if dateTime:
            data['dateTime'] = dateTime
        if details:
            data['details'] = details
        if resourceLog:
            data['resourceLog'] = resourceLog
        if booking:
            data['booking'] = booking
            
        url_path = "/charges"
        return self.__post(url_path, data=data)
    
    def create_invoice(self, member: int, date: str, number: Optional[str] = None, text: Optional[str] = None, 
                       charges: Optional[List[int]] = None, dueDate: Optional[str] = None, 
                       dunningFee: Optional[float] = None, discount: Optional[float] = None, notes: Optional[str] = None, 
                       applyOpenPayments: Optional[bool] = True) -> Union[List, Dict]:
        """Creates a New Invoice

        Args:
            member (int): ID for the member to be invoiced
            date (str): Date the invoice is published
            number (Optional[str], optional): Invoice number. Should be left empty to auto-generate the next invoice 
            number. Only provide a number if you want to bypass the automatic invoice number generator. Defaults to None.
            text (Optional[str], optional): Invoice Text. Defaults to None.
            charges (Optional[List[int]], optional): List of charges to be associated with the invoice. If provided, 
            must be a list of at least one item. Defaults to None.
            dueDate (Optional[str], optional): Due date of the invoice. Defaults to None.
            dunningFee (Optional[float], optional): Dunning Fee. Defaults to None.
            discount (Optional[float], optional): Any discoutn applied to the invoice. Defaults to None.
            notes (Optional[str], optional): Additional notes on the invoice. Defaults to None.
            applyOpenPayments (Optional[bool], optional): Apply any open payments from the member. Defaults to True on 
            the api if not supplied.

        Returns:
            Union[List, Dict]: Invoice information
        """
        
        url_path = "/invoices"
        data = {
            "member": member,
            "date": date,
            "applyOpenPayments": applyOpenPayments
        }
        if number:
            data['number'] = number
        if text:
            data['text'] = text
        if charges:
            data['charges'] = charges
        if dueDate:
            data['dueDate'] = dueDate
        if dunningFee:
            data['dunningFee'] = dunningFee
        if discount:
            data['discount'] = discount
        if notes:
            data['notes'] = notes
        
        return self.__post(url_path, data=data)
    
    def create_invoice_preview(self, member: int, charges: Optional[List[int]] = None) -> Union[List, Dict]:
        """Create an invoice preview for a given member

        Args:
            member (int): ID for member to create invoice
            charges (Optional[List[int]], optional): Optional list of charges to be included. If provided must be a list of at least size 1. Defaults to None.

        Returns:
            Union[List, Dict]: Returns an invoice preview
        """
        url_path = "/invoices/preview"
        data = {
            "member": member
        }
        if charges:
            data['charges'] = charges
        
        return self.__post(url_path, data=data)
    
    def create_key_assignments(self, member: int) -> Union[List, Dict]:
        """Creates a key assignment

        Args:
            member (int): ID for the member to assign a key

        Returns:
            Union[List, Dict]: Key assignment created upon success
        """
        
        url_path = "/key-assignments"
        data = {
            "member": member
        }
        
        return self.__post(url_path, data=data)
    
    def create_member(self, account: int, space: Optional[int] = None, memberNumber: Optional[int] = None, 
                      gender: Optional[str] = None, dateOfBirth: Optional[str] = None, emailAddress: Optional[str] = None,
                      company: Optional[str] = None, phone: Optional[str] = None, address: Optional[str] = None, 
                      address2: Optional[str] = None, city: Optional[str] = None, zip: Optional[str] = None, 
                      countryCode: Optional[str] = None, region: Optional[str] = None, notes: Optional[str] = None,
                      billingFirstName: Optional[str] = None, billingLastName: Optional[str] = None, billingCompany: Optional[str] = None,
                      billingAddress: Optional[str] = None, billingAddress2: Optional[str] = None, billingCity: Optional[str] = None,
                      billingZip: Optional[str] = None, billingCountryCode: Optional[str] = None, billingRegion: Optional[str] = None,
                      billingInvoiceText: Optional[str] = None, paidForBy: Optional[int] = None, 
                      metadata: Optional[Dict] = None, stripeCustomer: Optional[int] = None, language: Optional[str] = None, 
                      createdAt: Optional[str] = None, firstName: Optional[str] = None, lastName: Optional[str] = None,
                      state: Optional[str] = None, taxExempt: Optional[bool] = None, hasBillingAddress: bool = False, 
                      requireUpFrontPayment: bool = False, upFrontMinimumBalance: Optional[float] = None) -> Union[List, Dict]:
        """Creates a new member given the parameters.

        Args:
            account (int): Account for the member to belong to. This is required and not assumed from the API key in use.
            space (Optional[int], optional): Space the member is a part of. Required if the account has more than one space. Defaults to None.
            memberNumber (Optional[int], optional): Override member numbering system. Not recommended. Defaults to None.
            gender (Optional[str], optional): Member's gender. Can be one of male, female, or other. Defaults to None.
            dateOfBirth (Optional[str], optional): Date of birth of the user. Defaults to None.
            emailAddress (Optional[str], optional): Member's email address. Defaults to None.
            company (Optional[str], optional): Member's company. Defaults to None.
            phone (Optional[str], optional): Member's phone number. Defaults to None.
            address (Optional[str], optional): Member's address. Defaults to None.
            address2 (Optional[str], optional): Member's second address line for apartment, po box, etc. Defaults to None.
            city (Optional[str], optional): Member's City. Defaults to None.
            zip (Optional[str], optional): Member's Zip Code. Defaults to None.
            countryCode (Optional[str], optional): Member's Country Code. Use `get_country_codes()` for available country codes . Defaults to None.
            region (Optional[str], optional): Regional information. Defaults to None.
            notes (Optional[str], optional): Notes about the member. No space limitation. Defaults to None.
            billingFirstName (Optional[str], optional): Billing First name if different from the member name. Defaults to None.
            billingLastName (Optional[str], optional): Billing last name if different from member name. Defaults to None.
            billingCompany (Optional[str], optional): Billing company if different from the company. Defaults to None.
            billingAddress (Optional[str], optional): Billing address. Defaults to None.
            billingAddress2 (Optional[str], optional): Billing address second line. Defaults to None.
            billingCity (Optional[str], optional): Billing city. Defaults to None.
            billingZip (Optional[str], optional): Billing zip code. Defaults to None.
            billingCountryCode (Optional[str], optional): Billing country code. Defaults to None.
            billingRegion (Optional[str], optional): Billing region. Defaults to None.
            billingInvoiceText (Optional[str], optional): Text to be included on the billing invoice. Defaults to None.
            paidForBy (Optional[int], optional): Member ID of other member who pays for this member. Defaults to None.
            metadata (Optional[Dict], optional): Any JSON object with up to 2k of Data. Not checked by this interface. Defaults to None.
            stripeCustomer (Optional[int], optional): Stripe Customer ID. Defaults to None.
            language (Optional[str], optional): Member's native language. Defaults to None.
            createdAt (Optional[str], optional): Overrides the createdAt datetime. Not recommended. Defaults to None.
            firstName (Optional[str], optional): Member's First Name. Defaults to None.
            lastName (Optional[str], optional): Member's last name. Defaults to None.
            state (Optional[str], optional): State of the user's access. Must be one of active or locked. Defaults to 
            None, which fills in 'active' in the database
            taxExempt (Optional[bool], optional): Flag to declare the member tax exempt. Defaults to None.
            hasBillingAddress (bool, optional): Does the member have a billing address?. Defaults to False.
            requireUpFrontPayment (bool, optional): Required up front payment from Member. Defaults to False.
            upFrontMinimumBalance (Optional[float], optional): Establish a minimum balance for Member. Defaults to None.

        Returns:
            Union[List, Dict]: Newly created member object
        """
        
        args = locals()
        data = dict()
        for k, v in args.items():
            if k == 'gender' and v not in ['female', 'male', 'other', None]:
                raise KeyError("Gender must be one of female, male, or other. Or you could not specify it cause it doesn't matter.")
            if k == 'state' and v not in ['active', 'locked', None]:
                raise KeyError("State must be one of active or locked.")
            if v is not None:
                data[k] = v
        url_path = "/members"
        
        return self.__post(url_path, data=data)
    
    def create_member_credit(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_member_invitation(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_member_key(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_member_training(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_member_collections(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_member_by_impoty(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def convert_member_uninvoinced_charges_to_invoice(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_packages(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_package_credits(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_package_permissions(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_payment(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_payment_request(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_payment_intent(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_resource_log(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_resource_type(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_resource(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_resource_switch_on_event(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_space(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_space_holiday(self)
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_training_course(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_user_verification(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_user_login(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_user_logout(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_user_password_reset_email(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_user(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_webhook(self):
        raise NotImplementedError("This method is not yet implemented.")
    
    def create_webhook_test(self):
        raise NotImplementedError("This method is not yet implemented.")