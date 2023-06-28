"""Handles the Charge Object for managing fabman charges"""

import requests

from fabman.fabman_object import FabmanObject


class Charge(FabmanObject):
    """Charge object handles management of charges in fabman"""

    def __str__(self):
        return f"Charge #{self.id}: {self.price} {self.description}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes the charge. *WARNING: THIS CANNOT BE UNDONE.*

        Calls "DELETE /charges/{id}"
        Documentation: https://fabman.io/api/v1/documentation
        """

        response = self._requester.request(
            "DELETE", f"/charges/{self.id}", _kwargs=kwargs
        )

        return response

    def update(self, **kwargs) -> None:
        """
        Update the charge object on the server. Updates all information in place
        with returned data from the server.

        Calls "PUT /charges/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/charges/putChargesId
        """

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", f"/charges/{self.id}", _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
