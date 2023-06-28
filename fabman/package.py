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

        Calls "DELETE /packages/{packageId}/credits/{creditId}"
        Documentation https://fabman.io/api/v1/documentation#/packages/deletePackagesPackageIdCreditsCreditId
        """

        uri = f"/packages/{self.package_id}/credits/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the credit. Attributes are updated in place with new information.

        Calls "PUT /packages/{packageId}/credits/{creditId}"
        Documentation https://fabman.io/api/v1/documentation#/packages/putPackagesPackageIdCreditsCreditId
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

        Calls "DELETE /packages/{packageId}/permissions/{permissionId}"
        Documentation https://fabman.io/api/v1/documentation#/packages/deletePackagesPackageIdPermissionsPermissionId
        """

        uri = f"/packages/{self.package_id}/permissions/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the permission. Attributes are updated in place with new information.

        Calls "PUT /packages/{packageId}/permissions/{permissionId}"
        Documentation https://fabman.io/api/v1/documentation#/packages/putPackagesPackageIdPermissionsPermissionId
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

        Calls "POST /packages/{id}/credits"
        Documentation: https://fabman.io/api/v1/documentation#/packages/postPackagesIdCredits
        """

        uri = f"/packages/{self.id}/credits"
        response = self._requester.request("POST", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackageCredit(self._requester, data)

    def create_permission(self, **kwargs) -> PackagePermission:
        """
        Create a new permission for this package. Gives new abilities to package hodlers.

        Calls "POST /packages/{id}/permissions"
        Documentation: https://fabman.io/api/v1/documentation#/packages/postPackagesIdPermissions
        """

        uri = f"/packages/{self.id}/permissions"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackagePermission(self._requester, data)

    def get_credit(self, credit_id, **kwargs) -> PackageCredit:
        """
        Return a credit for this package given a credit_id.

        Calls "GET /packages/{id}/credits/{creditId}"
        Documentation: https://fabman.io/api/v1/documentation#/packages/getPackagesIdCreditsCreditId
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

        Calls "GET /packages/{id}/permissions/{permissionId}"
        Documentation: https://fabman.io/api/v1/documentation#/packages/getPackagesIdPermissionsPermissionId
        """
        uri = f"/packages/{self.id}/permissions/{permission_id}"
        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"package_id": self.id})

        return PackagePermission(self._requester, data)

    def get_permissions(self, **kwargs) -> PaginatedList:
        """
        Return a PaginatedList of permissions for the package.

        Calls "GET /packages/{id}/permissions"
        Documentation: https://fabman.io/api/v1/documentation#/packages/getPackagesIdPermissions
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

        Calls "DELETE /packages/{id}"
        Documentation https://fabman.io/api/v1/documentation#/packages/deletePackagesId
        """

        uri = f"/packages/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Update information on the package. Note that many fields may be unalterable
        by the API key holder.

        Calls "PUT /packages/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/packages/putPackagesId
        """

        uri = f"/packages/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
