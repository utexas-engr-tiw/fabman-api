"""Defines the Package class"""

import requests

from fabman.fabman_object import FabmanObject
from fabman.paginated_list import PaginatedList


class PackageCredit(FabmanObject):
    """Simple Class to handle PackageCredits"""

    def __str__(self):
        return f"PackageCredit #{self.id}, Package #{self.package_id}: {self.scope}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a credit from a package. *WARNING: This is irreversible.*

        :calls: "DELETE /packages/{packageId}/credits/{creditId}" \
		<https://fabman.io/api/v1/documentation#/packages/deletePackagesIdCreditsCreditid>
  
        :returns: response information of call
        :rtype: requests.Response
        """

        uri = f"/packages/{self.package_id}/credits/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the credit. Attributes are updated in place with new information.

        :calls: "PUT /packages/{packageId}/credits/{creditId}" \
		<https://fabman.io/api/v1/documentation#/packages/putPackagesIdCreditsCreditid>

        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/packages/{self.package_id}/credits/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class PackagePermission(FabmanObject):
    """Simple Class to handle PackagePermissions"""

    def __str__(self):
        return f"PackagePermission #{self.id}, Package #{self.package_id}: {self.type}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a permission from a package. *WARNING: This is irreversible.*

        :calls: "DELETE /packages/{packageId}/permissions/{permissionId}" \
		<https://fabman.io/api/v1/documentation#/packages/deletePackagesIdPermissionsPermissionid>

        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/packages/{self.package_id}/permissions/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the permission. Attributes are updated in place with new information.

        :calls: "PUT /packages/{packageId}/permissions/{permissionId}" \
		<https://fabman.io/api/v1/documentation#/packages/putPackagesIdPermissionsPermissionid>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/packages/{self.package_id}/permissions/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class Package(FabmanObject):
    """Handles all interaction with Package objects on the Fabman API"""

    def __str__(self):
        return f"Package #{self.id}: {self.name}"

    def create_credit(self, **kwargs) -> PackageCredit:
        """
        Create a credit for this package. Takes no arguments.

        :calls: "POST /packages/{id}/credits" \
		<https://fabman.io/api/v1/documentation#/packages/postPackagesIdCredits>

        :return: Object with information and methods of the new credit
        :rtype: fabman.package.PackageCredit
        """

        uri = f"/packages/{self.id}/credits"
        response = self._requester.request("POST", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackageCredit(self._requester, data)

    def create_permission(self, **kwargs) -> PackagePermission:
        """
        Create a new permission for this package. Gives new abilities to package hodlers.

        :calls: "POST /packages/{id}/permissions" \
		<https://fabman.io/api/v1/documentation#/packages/postPackagesIdPermissions>
  
        :return: Object with information and methods of the new permission
        :rtype: fabman.package.PackagePermission
        """

        uri = f"/packages/{self.id}/permissions"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackagePermission(self._requester, data)

    def get_credit(self, credit_id, **kwargs) -> PackageCredit:
        """
        Return a credit for this package given a credit_id.

        :calls: "GET /packages/{id}/credits/{creditId}" \
		<https://fabman.io/api/v1/documentation#/packages/getPackagesIdCreditsCreditid>

        :param credit_id: ID of the credit to retrieve
        :type credit_id: int
        :return: Object with information and methods of the credit
        :rtype: fabman.package.PackageCredit
        """

        uri = f"/packages/{self.id}/credits/{credit_id}"
        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackageCredit(self._requester, data)

    def get_credits(self, **kwargs) -> PaginatedList:
        """
        Return a PaginatedList of credits for this package

        Calls: "GET /packages/{id}/credits"
        Documentation: https://fabman.io/api/v1/documentation#/packages/getPackagesIdCredits

        :return: List of credits for this package
        :rtype: fabman.paginated_list.PaginatedList
        """

        return PaginatedList(
            PackageCredit,
            self._requester,
            "GET",
            f"/packages/{self.id}/credits",
            extra_attribs={"package_id": self.id},
            kwargs=kwargs,
        )

    def get_permission(self, permission_id, **kwargs) -> PackagePermission:
        """
        Return a permission for this package given a permission_id.

        :calls: "GET /packages/{id}/permissions/{permissionId}" \
		<https://fabman.io/api/v1/documentation#/packages/getPackagesIdPermissionsPermissionid>
  
        :returns: Object with information and methods of the permission
        :rtype: fabman.package.PackagePermission
        """
        uri = f"/packages/{self.id}/permissions/{permission_id}"
        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackagePermission(self._requester, data)

    def get_permissions(self, **kwargs) -> PaginatedList:
        """
        Return a PaginatedList of permissions for the package.

        :calls: "GET /packages/{id}/permissions" \
		<https://fabman.io/api/v1/documentation#/packages/getPackagesIdPermissions>

        :returns: List of permissions for the package
        :rtype: fabman.paginated_list.PaginatedList
        """

        return PaginatedList(
            PackagePermission,
            self._requester,
            "GET",
            f"/packages/{self.id}/permissions",
            extra_attribs={"packageId": self.id},
            kwargs=kwargs,
        )

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes the package. Takes no arguments. **WARNINGL: This is irreversible.**

        :calls: "DELETE /packages/{id}" \
		<https://fabman.io/api/v1/documentation#/packages/deletePackagesId>
  
        :returns: response information of call
        :rtype: requests.Response
        """

        uri = f"/packages/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Update information on the package. Note that many fields may be unalterable
        by the API key holder.

        :calls: "PUT /packages/{id}" \
		<https://fabman.io/api/v1/documentation#/packages/putPackagesId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/packages/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
