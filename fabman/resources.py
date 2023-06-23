"""Defines and handles the Resource object returned by the API."""
import requests
from fabman.fabman_object import FabmanObject


class ResourceBridge(FabmanObject):
    """Simple class to hold Bridge information for a Bridge connected to a resource. 
    Further used to issue commands to the bridge
    """

    def __str__(self):
        return f"Resource #{self.serialNumber}: {self.inUse}, {self.updatedAt}"


class Resource(FabmanObject):
    """
    Resource object returned by the API. Provides access to all API calls that 
    operate on a single Resource.
    """

    def __str__(self):
        return f"Resource #{self.id}: {self.name}"

    def delete_bridge(self, **kwargs) -> requests.Response:
        """
        Delete the bridge that is currently connected to this resource. If no bridge
        is currently connected, this will do nothing.

        Calls "DELETE /resources/{id}/bridge"
        Documentation: https://fabman.io/api/v1/documentation#/resources/deleteResourcesIdBridge
        """
        uri = f"/resources/{self.id}/bridge"

        response = self._requester.request(
            "DELETE", uri, _kwargs=kwargs
        )

        return response.json()

    def delete_resource(self, **kwargs) -> requests.Response:
        """
        Deletes the resource. *WARNING: THIS CANNOT BE UNDONE.* All future API
        calls from this resource will fail.

        Calls "DELETE /resources/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/resources/deleteResourcesId
        """
        uri = f"/resources/{self.id}"

        response = self._requester.request(
            "DELETE", uri, _kwargs=kwargs
        )

        return response.json()

    def get_bridge(self, **kwargs) -> ResourceBridge:
        """
        Get the bridge that is currently connected to this resource. If no bridge is
        connected, this will return an empty list.

        Calls "GET /resources/{id}/bridge"
        Documentation: https://fabman.io/api/v1/documentation#/resources/getResourcesIdBridge
        """
        uri = f"/resources/{self.id}/bridge"

        response = self._requester.request(
            "GET", uri, _kwargs=kwargs
        )

        return ResourceBridge(self._requester, response.json())

    def get_bridge_api_key(self, **kwargs) -> requests.Response:
        """
        Get the API key for the bridge that is currently connected to this resource.
        For most users, this will return a 204 code with an empty body. Only superusers 
        or users who have created a custom bridge should be able to access this endpoint.

        Calls "GET /resources/{id}/bridge/api-key"
        Documentation: https://fabman.io/api/v1/documentation#/resources/getResourcesIdBridgeApiKey
        """
        uri = f"/resources/{self.id}/bridge/api-key"

        response = self._requester.request(
            "GET", uri, _kwargs=kwargs
        )

        return response.json()

    def switch_on(self, **kwargs) -> requests.Response:
        """
        Switch on the resource. Requires "code" field to be in the data packet.
        Does not seem to work without the proper code, which is undocumented.

        Calls "POST /resources/{id}/switch-on"
        Documentation: https://fabman.io/api/v1/documentation#/resources/postResourcesIdSwitchOn
        """
        uri = f"/resources/{self.id}/switch-on"

        response = self._requester.request(
            "POST", uri, _kwargs=kwargs
        )

        return response.json()

    def update_bridge(self, **kwargs) -> requests.Response:
        """
        Update the bridge that is currently connected to this resource. If no bridge
        is currently connected, this will attach a new bridge to the resource.

        Calls "PUT /resources/{id}/bridge"
        Documentation: https://fabman.io/api/v1/documentation#/resources/putResourcesIdBridge
        """
        uri = f"/resources/{self.id}/bridge"

        response = self._requester.request(
            "PUT", uri, _kwargs=kwargs
        )

        return response.json()

    def update_resource(self, **kwargs) -> requests.Response:
        """
        Update the resource.

        Calls "PUT /resources/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/resources/putResourcesId
        """
        uri = f"/resources/{self.id}"

        response = self._requester.request(
            "PUT", uri, _kwargs=kwargs
        )

        return response.json()
