"""Defines the ResourceLog class"""

import requests

from fabman.fabman_object import FabmanObject


class ResourceLog(FabmanObject):
    """Class for interacting with the resource-logs endpoint on the Fabman API"""

    def __str__(self):
        return f"ResourceLog #{self.id}, Resource #{self.resource} - {self.type}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a resource-log. *WARNING: This is irreversible.*

        :calls: "DELETE /resource-logs/{resourceLogId}" \
		<https://fabman.io/api/v1/documentation#/resource-logs/deleteResourcelogsId>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/resource-logs/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the resource-log. Attributes are updated in place with new information
        retrieved from the API.

        :calls: "PUT /resource-logs/{resourceLogId}" \
		<https://fabman.io/api/v1/documentation#/resource-logs/putResourcelogsId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/resource-logs/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
