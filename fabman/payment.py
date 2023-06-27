"""Defines the Payment object"""

import requests

from fabman.fabman_object import FabmanObject


class Payment(FabmanObject):
    """Defines the Payment object for interacting with payments on the Fabman API"""

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a payment. *WARNING: This is irreversible.*

        Calls "DELETE /payments/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/payments/deletePaymentsId
        """
        uri = f"/payments/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response.json()

    def request_payment(self, **kwargs) -> requests.Response:
        """
        Requests a payment from the customer.

        Calls "POST /payments/{id}/request-payment"
        Documentation: https://fabman.io/api/v1/documentation#/payments/postPaymentsIdRequestPayment
        """
        uri = f"/payments/{self.id}/request-payment"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates a payment. Attributes are modified in place using updated information
        from the API.

        Calls "PUT /payments/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/payments/putPaymentsId
        """

        uri = f"/payments/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
