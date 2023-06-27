"""Defines the ApiKey class"""

import requests

from fabman.fabman_object import FabmanObject


class ApiKey(FabmanObject):
    """Class for interacting with the api-keys endpoints on the Fabman API"""

    def __str__(self):
        return f"ApiKey #{self.id}: {self.label}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes an api-key. *WARNING: This is irreversible.*

        Calls "DELETE /api-keys/{apiKeyId}"
        Documentation https://fabman.io/api/v1/documentation#/api-keys/deleteApiKeysId
        """

        uri = f"/api-keys/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response.json()

    def get_token(self, **kwargs) -> requests.Response:
        """
        Returns the token for an api-key. Must be called with a valid api-key.

        Calls "GET /api-keys/{apiKeyId}/token"
        Documentation https://fabman.io/api/v1/documentation#/api-keys/getApiKeysIdToken
        """

        uri = f"/api-keys/{self.id}/token"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates the api-key. Attributes are updated in place with new information
        returned by the API.

        Calls "PUT /api-keys/{apiKeyId}"
        Documentation https://fabman.io/api/v1/documentation#/api-keys/putApiKeysId
        """

        uri = f"/api-keys/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
