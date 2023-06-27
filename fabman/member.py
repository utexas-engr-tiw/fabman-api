"""Defines and handles the Member object returned by the API"""
# pylint: disable=too-many-public-methods, line-too-long
from typing import Union

import requests

from fabman.fabman_object import FabmanObject
from fabman.paginated_list import PaginatedList


class MemberCredit(FabmanObject):
    """
    Simple Class to handle operations on MemberCredits
    """

    def __str__(self):
        return f"{self.id}: {self.scope} - {self.amount}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a credit from a user account. *WARNING: THIS CANNOT BE UNDONE.*

        Calls "DELETE /members/{member_id}/credits/{credit_id}"
        Documentation https://fabman.io/api/v1/documentation#/members/deleteMembersIdCreditsCreditId
        """
        response = self._requester.request(
            "DELETE", f"/members/{self.member_id}/credits/{self.id}", _kwargs=kwargs
        )

        return response.json()

    def get_uses(self, **kwargs) -> requests.Response:
        """
        Retrieves a list of uses of the credit.

        Calls "GET /members/{member_id}/credits/{credit_id}/uses"
        Documentation https://fabman.io/api/v1/documentation#/members/getMembersIdCreditsCreditidUses
        """
        response = self._requester.request(
            "GET", f"/members/{self.member_id}/credits/{self.id}/uses", _kwargs=kwargs
        )

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates an existing credit in place

        Calls "PUT /members/{id}/credits/{creditId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/putMembersIdCreditsCreditId
        """
        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request(
            "PUT", f"/members/{self.member_id}/credits/{self.id}", _kwargs=kwargs
        )

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class MemberKey(FabmanObject):
    """
    Manage a member keycard object
    """

    def __str__(self):
        return f"{self.member} - {self.type}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a member key

        Calls "DELETE /members/{self.member}/key"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdKey
        """
        response = self._requester.request(
            "DELETE", f"/members/{self.member}/key", _kwargs=kwargs
        )

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates a member key and updates the MemberKey object in place with new
        data from the API.

        Calls "PUT /member{self.member}/key"
        Documentation: https://fabman.io/api/v1/documentation#/members/putMembersIdKey
        """
        response = self._requester.request(
            "PUT", f"/members/{self.member}/key", _kwargs=kwargs
        )

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class MemberPackage(FabmanObject):
    """
    Simple class for managing member packages
    """

    def __str__(self):
        return f"{self.id} - {self.package}"

    def delete(self, **kwargs) -> requests.Response:
        """Removes the package from the current user account. *WARNING: THIS CANNOT BE UNDONE.*

        Calls "DELETE /members/{id}/packages/{memberPackageId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdPackagesMemberPackageId
        """

        response = self._requester.request(
            "DELETE", f"/members/{self.member_id}/packages/{self.id}", _kwargs=kwargs
        )

        return response.json()

    def get_package(self) -> None:
        """
        Gets information about the package

        Calls "GET /packages/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/packages/getPackagesId
        """
        raise NotImplementedError(
            "get_package_info not implemented yet. Awaiting Packages implementation"
        )


class Member(FabmanObject):
    """
    Member object returned by the API. Provides access to all API calls that operate on a single member.
    """

    def __str__(self):
        return f"{self.id}: {self.firstName} {self.lastName}"

    def create_credit(self, **kwargs) -> MemberCredit:
        """
        Creates a member credit
        calls "POST /members/{id}/credits"
        Documentation: https://fabman.io/api/v1/documentation#/members/postMembersIdCredits
        """

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request(
            "POST",
            f"/members/{self.id}/credits",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberCredit(self._requester, data)

    def create_key(self, **kwargs) -> MemberKey:
        """
        Creates a key for the member if one does not already exist. If member already has
        a key, use `update_key()`.

        Calls "POST /members/{id}/key"
        Documentation: https://fabman.io/api/v1/documentation#/members/postMembersIdKey
        """

        response = self._requester.request(
            "POST", f"/members/{self.id}/key", _kwargs=kwargs
        )

        return MemberKey(self._requester, response.json())

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a member
        calls "DELETE /members/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersId
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.id}",
            _kwargs=kwargs,
        )

    def delete_change(self, change_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member change given change ID
        calls "DELETE /members/{id}/changes/{changeId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdChangesChangeId
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.id}/changes/{change_id}",
            _kwargs=kwargs,
        )

    def delete_device_change(self, change_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member device change given change ID
        Calls "DELETE /members/{id}/device/changes/{changeId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdDeviceChangesChangeId
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.id}/device/changes/{change_id}",
            _kwargs=kwargs,
        )

    def delete_payment_method(self, **kwargs) -> requests.Response:
        """
        Deletes a member payment method
        Calls "DELETE /members/{id}/payment-method"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdPaymentMethod
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.id}/payment-method",
            _kwargs=kwargs,
        )

    def delete_training(self, training_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member training given training ID
        Calls "DELETE /members/{id}/trainings/{trainingId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdTrainingsTrainingId
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.id}/trainings/{training_id}",
            _kwargs=kwargs,
        )

    def get_balance_items(self, **kwargs) -> requests.Response:
        """
        Retrieves the balance items of a member
        calls "GET /members/{id}/balance-items"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdBalanceitems
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/balance-items",
            _kwargs=kwargs,
        )

        return response.json()

    def get_changes(self, **kwargs) -> requests.Response:
        """
        Retrieves the changes of a member
        calls "GET /members/{id}/changes"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdChanges
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/changes",
            _kwargs=kwargs,
        )

        return response.json()

    def get_credits(self, **kwargs) -> PaginatedList:
        """
        Retrieves the credits of a member
        calls "GET /members/{id}/credits"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdCredits
        """
        return PaginatedList(
            MemberCredit,
            self._requester,
            "GET",
            f"/members/{self.id}/credits",
            extra_attribs={"member_id": self.id},
            kwargs=kwargs,
        )

    def get_credit(self, credit_id: int, **kwargs) -> MemberCredit:
        """
        Retrieves a credit of a member
        calls "GET /members/{id}/credits/{creditId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdCreditsCreditId
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/credits/{credit_id}",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberCredit(self._requester, data)

    def get_device(self, **kwargs) -> requests.Response:
        """
        Retrieves the device of a member used to authenticate on a bridge.
        calls "GET /members/{id}/devices"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdDevice
        """
        if "device" in self._embedded:
            return self._embedded["device"]

        response = self._requester.request(
            "GET",
            f"/members/{self.id}/device",
            _kwargs=kwargs,
        )

        return response.json()

    def get_device_changes(self, **kwargs) -> requests.Response:
        """
        Retrieves the device changes of a member
        calls "GET /members/{id}/device/changes"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdDeviceChanges
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/device/changes",
            _kwargs=kwargs,
        )

        return response.json()

    def get_device_change(self, change_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a device change of a member given the change ID
        calls "GET /members/{id}/device/changes/{changeId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdDeviceChangesChangeId
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/device/changes/{change_id}",
            _kwargs=kwargs,
        )

        return response.json()

    def get_export(self, **kwargs) -> requests.Response:
        """
        Retrieves the export of a member
        calls "GET /members/{id}/export"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdExport
        """
        raise NotImplementedError("get_export not implemented yet")

    def get_invitation(self, **kwargs) -> requests.Response:
        """
        Retrieves the invitation status of a member
        calls "GET /members/{id}/invitations"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdInvitation
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/invitation",
            _kwargs=kwargs,
        )

        return response.json()

    def get_key(self, **kwargs):
        """
        Retrieves the keycard number of a member
        calls "GET /members/{id}/key"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdKey
        """
        if "key" in self._embedded:
            return self._embedded["key"]

        response = self._requester.request(
            "GET",
            f"/members/{self.id}/key",
            _kwargs=kwargs,
        )

        return response.json()

    def get_packages(self, **kwargs) -> Union[list, PaginatedList]:
        """
        Retrieves the packages of a member

        calls "GET /members/{id}/packages"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPackages
        """
        if "memberPackages" in self._embedded:
            out = []
            for package in self._embedded["memberPackages"]:
                package.update({"member_id": self.id})
                out.append(MemberPackage(self._requester, package))
            return out

        return PaginatedList(
            MemberPackage,
            self._requester,
            "GET",
            f"/members/{self.id}/packages",
            extra_attribs={"member_id": self.id},
            kwargs=kwargs,
        )

    def get_package(self, member_package_id: int, **kwargs) -> MemberPackage:
        """
        Retrieves a package of a member
        calls "GET /members/{id}/packages/{memberPackageId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPackagesMemberPackageId
        """
        if "memberPackages" in self._embedded:
            for package in self._embedded["memberPackages"]:
                if package["id"] == member_package_id:
                    return package

        response = self._requester.request(
            "GET",
            f"/members/{self.id}/packages/{member_package_id}",
            _kwargs=kwargs,
        )

        return MemberPackage(self._requester, response.json())

    def get_payment_account(self, **kwargs) -> requests.Response:
        """
        Retrieves the payment account of a member
        calls "GET /members/{id}/payment-account"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentAccount
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/payment-account",
            _kwargs=kwargs,
        )

        return response.json()

    def get_payment_method(self, **kwargs) -> requests.Response:
        """
        Retrieves the payment method of a member
        calls "GET /members/{id}/payment-method"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentMethod
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/payment-method",
            _kwargs=kwargs,
        )

        return response.json()

    def get_payment_method_mandate_preview(self, **kwargs) -> requests.Response:
        """
        Retrieves the payment method mandate preview of a member
        calls "GET /members/{id}/payment-method-mandate-preview"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentMethodMandatePreview
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/payment-method-mandate-preview",
            _kwargs=kwargs,
        )

        return response.json()

    def get_privileges(self, **kwargs) -> requests.Response:
        """
        Retrieves the privileges of a member
        calls "GET /members/{id}/privileges"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPrivileges
        """
        if "privileges" in self._embedded:
            return self._embedded["privileges"]

        response = self._requester.request(
            "GET",
            f"/members/{self.id}/privileges",
            _kwargs=kwargs,
        )

        return response.json()

    def get_trained_resources(self, **kwargs) -> requests.Response:
        """
        Retrieves the trained resources of a member
        calls "GET /members/{id}/trained-resources"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdTrainedResources
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/trained-resources",
            _kwargs=kwargs,
        )

        return response.json()

    def get_trainings(self, **kwargs) -> requests.Response:
        """
        Retrieves the trainings of a member
        calls "GET /members/{id}/trainings"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdTrainings
        """
        if "trainings" in self._embedded:
            return self._embedded["trainings"]

        response = self._requester.request(
            "GET",
            f"/members/{self.id}/trainings",
            _kwargs=kwargs,
        )

        return response.json()

    def get_training(self, training_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a training of a member
        calls "GET /members/{id}/trainings/{trainingId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdTrainingsTrainingId
        """
        if "trainings" in self._embedded:
            for training in self._embedded["trainings"]:
                if training["id"] == training_id:
                    return training

        response = self._requester.request(
            "GET",
            f"/members/{self.id}/trainings/{training_id}",
            _kwargs=kwargs,
        )

        return response.json()

    def refresh(self) -> None:
        """
        Updates the objects with more recent data from the API. Needs to be called
        when update() fails for lockVersioning.

        Calls "GET /members/{id}"
        Documentation https://fabman.io/api/v1/documentation#/members/getMembersId
        """

        response = self._requester.request("GET", f"/members/{self.id}")

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)

    def update(self, **kwargs) -> None:
        """
        Updates the member object and sets the modified attributes based on what
        is returned by the server.  Member object is updated in place.

        calls "PUT /members/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/members/putMembersId
        """

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request(
            "PUT",
            f"/members/{self.id}",
            _kwargs=kwargs,
        )

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
