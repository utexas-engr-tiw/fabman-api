"""Define the Invoice Object"""

import requests

from fabman.fabman_object import FabmanObject


class Invoice(FabmanObject):
    """Simple Class to handle Invoices"""

    def __str__(self):
        return f"Invoice #{self.id}: {self.total} {self.state}"

    def cancel(self) -> requests.Response:
        """
        Cancels an invoice. Takes no arguments.

        :calls: "POST /invoices/{id}/cancel" \
		<https://fabman.io/api/v1/documentation#/invoices/postInvoicesIdCancel>
  
        :returns: An empty dict if successful.
        :type: dict
        """

        data = {"lockVersion": self.lockVersion}

        uri = f"/invoices/{self.id}/cancel"
        response = self._requester.request("POST", uri, _kwargs=data)

        return response.json()

    def details(self, **kwargs) -> requests.Response:
        """
        Returns details about the invoice. Takes no arguments.

        :calls: "GET /invoices/{id}/details" \
		<https://fabman.io/api/v1/documentation>
  
        :returns: A dict containing details about the invoice.
        :rtype: dict
        """

        if "details" in self._embedded:
            return self._embedded["details"]

        uri = f"/invoices/{self.id}/details"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        self._embedded["details"] = response.json()

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates the invoice. Attributes are updated in place with new information
        provided by the API

        :calls: "PUT /invoices/{id}" \
		<https://fabman.io/api/v1/documentation#/invoices/putInvoicesId>
  
        :returns: None -- updates attributes of the current object
        :rtype: None
        """

        kwargs.update({"lockVersion": self.lockVersion})

        uri = f"/invoices/{self.id}"
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()
        for attr, val in data.items():
            setattr(self, attr, val)
