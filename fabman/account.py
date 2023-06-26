"""Defines the Account object"""

import requests
from fabman.fabman_object import FabmanObject


class Account(FabmanObject):
    """Handles Account objects from the Fabman API. In most cases, this only
    returns information about the API key holders account. Since most API endpoints
    in this object require superuser privileges, they are not implemented.
    """

    def __str__(self):
        return f"Account #{self.id}: {self.name}"

    def update_account(self, **kwargs) -> requests.Response:
        """
        Update information on the account. Note that many fields may be unalterable
        by the API key holder.

        Calls "PUT /accounts/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/account/putAccountsId
        """
        uri = f"/accounts/{self.id}"

        response = self._requester.request(
            "PUT", uri, _kwargs=kwargs
        )

        return response.json()

    def get_payment_info(self, **kwargs) -> requests.Response:
        """
        Get information about the payment plan of the account.

        Calls "GET /accounts/{id}/payment-info"
        """
        uri = f"/accounts/{self.id}/payment-info"

        response = self._requester.request(
            "GET", uri, _kwargs=kwargs
        )

        return response.json()
