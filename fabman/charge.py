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

        :calls: "DELETE /charges/{id}" \
		<https://fabman.io/api/v1/documentation#/charges/deleteChargesId>
  
        :returns: Response from the API with status code 204 (No Content) if successful
        :rlist: requests.Response
        """

        response = self._requester.request(
            "DELETE", f"/charges/{self.id}", _kwargs=kwargs
        )

        return response

    def update(self, **kwargs) -> None:
        """
        Update the charge object on the server. Updates all information in place
        with returned data from the server.

        :calls: "PUT /charges/{id}" \
		<https://fabman.io/api/v1/documentation#/charges/putChargesId>
  
        :returns: None
        :rlist: None
        """

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", f"/charges/{self.id}", _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
