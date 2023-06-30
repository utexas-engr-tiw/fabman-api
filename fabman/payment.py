"""Defines the Payment object"""

import requests

from fabman.fabman_object import FabmanObject


class Payment(FabmanObject):
    """Defines the Payment object for interacting with payments on the Fabman API"""

    def __str__(self) -> str:
        return f"Payment #{self.id}: {self.notes}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a payment. *WARNING: This is irreversible.*

        :calls: "DELETE /payments/{id}" \
		<https://fabman.io/api/v1/documentation#/payments/deletePaymentsId>

        :returns: response information of call
        :rtype: requests.Response
        """
        uri = f"/payments/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def request_payment(self, **kwargs) -> requests.Response:
        """
        Requests a payment from the customer.

        :calls: "POST /payments/{id}/request-payment" \
		<https://fabman.io/api/v1/documentation#/payments/postPaymentsIdRequestpayment>
        
        :return: response information of the call
        :rtype: requests.Response
        """
        uri = f"/payments/{self.id}/request-payment"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates a payment. Attributes are modified in place using updated information
        from the API.

        :calls: "PUT /payments/{id}" \
		<https://fabman.io/api/v1/documentation#/payments/putPaymentsId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/payments/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
