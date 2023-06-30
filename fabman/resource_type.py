"""Defines the ResourceType class"""

import requests

from fabman.fabman_object import FabmanObject


class ResourceType(FabmanObject):
    """Class for interacting with the resource-types endpoint in the Fabman API"""

    def __str__(self):
        return f"ResourceType #{self.id}: {self.name}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a resource-type. *WARNING: This is irreversible and may have
        unintended consequences.* Resource Types are used to group resources and
        are therefore tied to all resources of that type. Be sure you know
        what you are doing when using this endpoint. There is no confirmation.

        :calls: "DELETE /resource-types/{resourceTypeId}" \
		<https://fabman.io/api/v1/documentation#/resource-types/deleteResourcetypesId>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/resource-types/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the resource-type. Attributes are updated in place with new information
        retrieved from the API.

        :calls: "PUT /resource-types/{resourceTypeId}" \
		<https://fabman.io/api/v1/documentation#/resource-types/putResourcetypesId>

        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/resource-types/{self.id}"

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
