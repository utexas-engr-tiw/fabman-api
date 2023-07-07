"""Defines and handles the Resource object returned by the API."""
import requests

from fabman.fabman_object import FabmanObject


class ResourceBridge(FabmanObject):
    """Simple class to hold Bridge information for a Bridge connected to a resource.
    Further used to issue commands to the bridge
    """

    def __str__(self):
        return f"Resource #{self.resource_id}: {self.serialNumber}"

    def update(self, **kwargs) -> None:
        """
        Update the bridge object on the server. Returns the updated bridge object.
        Updates all information in place.

        :calls: "PUT /resources/{resource_id}/bridge" \
		<https://fabman.io/api/v1/documentation#/resources/putResourcesIdBridge>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """
        uri = f"/resources/{self.resource_id}/bridge"

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class ResourceBridgeApiKey(FabmanObject):
    """Simple class to hold Bridge API key information"""

    def __str__(self):
        return f"Resource #{self.resource_id}: {self.apiKey}"


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

        :calls: "DELETE /resources/{id}/bridge" \
		<https://fabman.io/api/v1/documentation#/resources/deleteResourcesIdBridge>
  
        :return: response information of call
        :rtype: requests.Response
        """
        uri = f"/resources/{self.id}/bridge"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes the resource. *WARNING: THIS CANNOT BE UNDONE.* All future API
        calls from this resource will fail.

        :calls: "DELETE /resources/{id}" \
		<https://fabman.io/api/v1/documentation#/resources/deleteResourcesId>
  
        :return: response information of call
        :rtype: requests.Response
        """
        uri = f"/resources/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def get_bridge(self, **kwargs) -> ResourceBridge:
        """
        Get the bridge that is currently connected to this resource. If no bridge is
        connected, this will return an empty list.

        :calls: "GET /resources/{id}/bridge" \
		<https://fabman.io/api/v1/documentation#/resources/getResourcesIdBridge>
  
        :return: ResourceBridge object with information on the bridge
        :rtype: fabman.resource.ResourceBridge
        
        """
        uri = f"/resources/{self.id}/bridge"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"resource_id": self.id})

        return ResourceBridge(self._requester, data)

    def get_bridge_api_key(self, **kwargs) -> ResourceBridgeApiKey:
        """
        Get the API key for the bridge that is currently connected to this resource.
        For most users, this will return a 204 code with an empty body. Only superusers
        or users who have created a custom bridge should be able to access this endpoint.

        :calls: "GET /resources/{id}/bridge/api-key" \
		<https://fabman.io/api/v1/documentation#/resources/getResourcesIdBridgeApikey>

        :return: response information of call
        :rtype: ResourceBridgeApiKey
        """
        uri = f"/resources/{self.id}/bridge/api-key"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"resource_id": self.id})

        return ResourceBridgeApiKey(self._requester, data)

    def switch_on(self, **kwargs) -> requests.Response:
        """
        Switch on the resource. Requires "code" field to be in the data packet.
        Does not seem to work without the proper code, which is undocumented.

        :calls: "POST /resources/{id}/switch-on" \
		<https://fabman.io/api/v1/documentation#/resources/postResourcesIdBridgeSwitchon>
  
        :return: response information of call
        :rtype: requests.Response
        """
        uri = f"/resources/{self.id}/switch-on"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Update the resource.

        :calls: "PUT /resources/{id}" \
		<https://fabman.io/api/v1/documentation#/resources/putResourcesId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """
        uri = f"/resources/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
