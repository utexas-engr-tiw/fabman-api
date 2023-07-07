"""Defines and handles the Member object returned by the API"""
# pylint: disable=too-many-public-methods, line-too-long
from typing import List, Optional, Union

import requests

from fabman.embedded_list import EmbeddedList
from fabman.fabman_object import FabmanObject
from fabman.package import Package
from fabman.paginated_list import PaginatedList


class MemberBalanceItems(FabmanObject):
    """Simple Class to handle Member Balance Items"""


class MemberChange(FabmanObject):
    """Simple class to hold Member Changes"""

    def __str__(self):
        return f"Change #{self.id} for member #{self.member_id}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a member change given change ID
        
        :calls: "DELETE /members/{id}/changes/{changeId}" \
        <https://fabman.io/api/v1/documentation#/members/deleteMembersIdChangesChangeid>
        
        :return: Response information of delete call
        :rtype: requests.Response
        """

        return self._requester.request(
            "DELETE", f"/members/{self.member_id}/changes/{self.id}", _kwargs=kwargs
        )


class MemberCreditUse(FabmanObject):
    """
    Simple class to hold Credit Use
    """

    def __str__(self):
        # TODO: Test this method. No current way of applying credits with account available to developers
        return f"{self.id}: {self.amount} - {self.description}"


class MemberCredit(FabmanObject):
    """
    Simple Class to handle operations on MemberCredits
    """

    def __str__(self):
        return f"{self.id}: {self.scope} - {self.amount}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a credit from a user account. **WARNING: THIS CANNOT BE UNDONE.**

        :calls: "DELETE /members/{member_id}/credits/{credit_id}" \
		<https://fabman.io/api/v1/documentation#/members/deleteMembersIdCreditsCreditid>

        :returns: An empty dict if successful.
        :rtype: dict
        """
        response = self._requester.request(
            "DELETE", f"/members/{self.member_id}/credits/{self.id}", _kwargs=kwargs
        )

        return response

    def get_uses(self, **kwargs) -> List[MemberCreditUse]:
        """
        Retrieves a list of uses of the credit.

        :calls: "GET /members/{member_id}/credits/{credit_id}/uses" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdCreditsCreditidUses>
  
        :return: A list of uses of the credit.
        :rtype: list
        """
        response = self._requester.request(
            "GET", f"/members/{self.member_id}/credits/{self.id}/uses", _kwargs=kwargs
        )

        data = response.json()
        return [MemberCreditUse(self._requester, use) for use in data]

    def update(self, **kwargs) -> None:
        """
        Updates an existing credit in place

        :calls: "PUT /members/{id}/credits/{creditId}" \
		<https://fabman.io/api/v1/documentation#/members/putMembersIdCreditsCreditid>
  
        :returns: None
        :rtype: None
        """
        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request(
            "PUT", f"/members/{self.member_id}/credits/{self.id}", _kwargs=kwargs
        )

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class MemberDevice(FabmanObject):
    """Simple Class to represent a Member Device"""

    def __str__(self):
        return f"Device: {self.name}"


class MemberDeviceChange(FabmanObject):
    """Simple class to represent a Member Device Change"""

    def __str__(self) -> str:
        return f"DeviceChange #{self.id} for member #{self.member_id}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a member device change given change ID
        
        :calls: "DELETE /members/{id}/device/changes/{changeId}" \
        <https://fabman.io/api/v1/documentation#/members/deleteMembersIdDeviceChangesChangeid>
        
        :returns: Response information of delete call
        :rtype: requests.Response
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.member_id}/device/changes/{self.id}",
            _kwargs=kwargs,
        )


class MemberInvitation(FabmanObject):
    """Simple class to represent a MemberInvitation"""


class MemberKey(FabmanObject):
    """
    Manage a member keycard object
    """

    def __str__(self):
        return f"{self.member} - {self.type}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a member key. **WARNING: THIS CANNOT BE UNDONE.**

        :calls: "DELETE /members/{self.member}/key" \
		<https://fabman.io/api/v1/documentation#/members/deleteMembersIdKey>
  
        :returns: Response information of delete call
        :rtype: requests.Response
        """
        response = self._requester.request(
            "DELETE", f"/members/{self.member}/key", _kwargs=kwargs
        )

        return response

    def update(self, **kwargs) -> None:
        """
        Updates a member key and updates the MemberKey object in place with new
        data from the API.

        :calls: "PUT /member{self.member}/key" \
		<https://fabman.io/api/v1/documentation#/members/putMembersIdKey>
  
        :returns: None
        :rtype: None
        """

        kwargs.update({"lockVersion": self.lockVersion})

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

        :calls: "DELETE /members/{id}/packages/{memberPackageId}" \
		<https://fabman.io/api/v1/documentation#/members/deleteMembersIdPackagesMemberpackageid>

        :returns: Response information of delete call
        :rtype: requests.Response
        """

        response = self._requester.request(
            "DELETE", f"/members/{self.member_id}/packages/{self.id}", _kwargs=kwargs
        )

        return response

    def get_package(self, **kwargs) -> Package:
        """
        Gets information about the package

        :calls: "GET /packages/{id}" \
		<https://fabman.io/api/v1/documentation#/packages/getPackagesId>
        
        :returns: :code:`fabman.package.Package` object with Package details
        :rtype: fabman.package.Package
        """
        if "package" in self._embedded:
            data = self._embedded["package"]
        else:
            response = self._requester.request(
                "GET", f"/packages/{self.package}", _kwargs=kwargs
            )
            data = response.json()

        return Package(self._requester, data)

    def update(self, **kwargs) -> None:
        """
        Updates a member package and updates the MemberPackage object in place with new
        data from the API

        :calls: "PUT /members/{id}/packages/{memberPackageId}" \
		<https://fabman.io/api/v1/documentation#/members/putMembersIdPackagesMemberpackageid>
  
        :returns: None
        :rtype: None
        """
        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request(
            "PUT", f"/members/{self.member_id}/packages/{self.id}", _kwargs=kwargs
        )

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class MemberPaymentAccount(FabmanObject):
    """Simple object to hold Member Payment Accounts"""


class MemberPaymentMethod(FabmanObject):
    """Simple object to hold Member Payment Methods"""

    def __str__(self):
        return f"Member #{self.member_id} has a {self.type} payment method"

    def delete(self, **kwargs):
        """Deletes a member payment method
        
        :calls: "DELETE /members/{id}/payment-method" \
        <https://fabman.io/api/v1/documentation#/members/deleteMembersIdPaymentmethod>
        
        :return: Response information of the delete call
        :rtype: requests.Response
        """

        return self._requester.request(
            "DELETE", f"/members/{self.member_id}/payment-method", _kwargs=kwargs
        )


class MemberPaymentMethodMandatePreview(FabmanObject):
    """Simple object to hold Member Payment Method Mandate Previews"""


class MemberPrivileges(FabmanObject):
    """Simple object to hold Member Privileges"""

    def __str__(self):
        return f"Member #{self.member_id} is {self.privileges}"


class MemberTrainedResources(FabmanObject):
    """Simple object to hold Member Trained Resources"""

    def __str__(self):
        return f"Member #{self.member_id} is trained on {len(self.resources)} resources"


class MemberTraining(FabmanObject):
    """Simple object to handle Member Trainings"""

    def __str__(self):
        return f"MemberTraining #{self.id} for member #{self.member_id}"

    def delete(self, **kwargs):
        """Deletes a member training

        :calls: "DELETE /members/{id}/trainings/{trainingId}" \
        <https://fabman.io/api/v1/documentation#/members/deleteMembersIdTrainingsTrainingid>
        
        :return: Response Information of delete call
        :rtype: requests.Response
        """

        return self._requester.request(
            "DELETE", f"/members/{self.member_id}/trainings/{self.id}", _kwargs=kwargs
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
        
        :calls: "POST /members/{id}/credits" \
		<https://fabman.io/api/v1/documentation#/members/postMembersIdCredits>

        :returns: :code:`fabman.member.MemberCredit` object with credit details
        :rtype: fabman.member.MemberCredit
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

        :calls: "POST /members/{id}/key" \
		<https://fabman.io/api/v1/documentation#/members/postMembersIdKey>
  
        :returns: :code:`fabman.member.MemberKey` object with key details
        :rtype: fabman.member.MemberKey
        """

        response = self._requester.request(
            "POST", f"/members/{self.id}/key", _kwargs=kwargs
        )

        return MemberKey(self._requester, response.json())

    def create_training(self, **kwargs) -> MemberTraining:
        """Creates a Training object which links a member to a training course.

        :return: MemberTraining object
        :rtype: MemberTraining
        """

        response = self._requester.request(
            "POST", f"/members/{self.id}/trainings", _kwargs=kwargs
        )

        return MemberTraining(self._requester, response.json())

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a member
        
        :calls: "DELETE /members/{id}" \
		<https://fabman.io/api/v1/documentation#/members/deleteMembersId>
  
        :returns: Response information of delete call
        :rtype: requests.Response
        """
        return self._requester.request(
            "DELETE",
            f"/members/{self.id}",
            _kwargs=kwargs,
        )

    def get_balance_items(self, **kwargs) -> MemberBalanceItems:
        """
        Retrieves the balance items of a member
        
        :calls: "GET /members/{id}/balance-items" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdBalanceitems>
  
        :returns: Response information of get call
        :rtype: MemberBalanceItems
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/balance-items",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberBalanceItems(self._requester, data)

    def get_changes(self, **kwargs) -> List[MemberChange]:
        """
        Retrieves the changes of a member
        
        :calls: "GET /members/{id}/changes" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdChanges>
  
        :returns: List of changes of a member
        :rtype: list[MemberChange]
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/changes",
            _kwargs=kwargs,
        )
        data = response.json()
        for change in data:
            change.update({"member_id": self.id})

        return [MemberChange(self._requester, x) for x in data]

    def get_credits(self, **kwargs) -> PaginatedList:
        """
        Retrieves the credits of a member
        :calls: "GET /members/{id}/credits" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdCredits>
  
        :returns: List of credits of a member
        :rtype: fabman.paginated_list.PaginatedList
        """
        return PaginatedList(
            MemberCredit,
            self._requester,
            "GET",
            f"/members/{self.id}/credits",
            extra_attribs={"member_id": self.id},
            **kwargs,
        )

    def get_credit(self, credit_id: int, **kwargs) -> MemberCredit:
        """
        Retrieves a credit of a member
        
        :calls: "GET /members/{id}/credits/{creditId}" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdCreditsCreditid>
  
        :param credit_id: ID of the credit to retrieve
        :type credit_id: int
        :returns: :code:`fabman.member.MemberCredit` object with credit details
        :rtype: fabman.member.MemberCredit
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/credits/{credit_id}",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberCredit(self._requester, data)

    def get_device(self, **kwargs) -> MemberDevice:
        """
        Retrieves the device of a member used to authenticate on a bridge.
        
        :calls: "GET /members/{id}/devices" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdDevice>
  
        :returns: Device information
        :rtype: dict
        """
        if "device" in self._embedded:
            data = self._embedded["device"]
        else:
            response = self._requester.request(
                "GET",
                f"/members/{self.id}/device",
                _kwargs=kwargs,
            )

            data = response.json()
        data.update({"member_id": self.id})

        return MemberDevice(self._requester, data)

    def get_device_changes(self, **kwargs) -> List[MemberDeviceChange]:
        """
        Retrieves the device changes of a member
        
        :calls: "GET /members/{id}/device/changes" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdDeviceChanges>

        :returns: List of device changes of a member
        :rtype: list[MemberDeviceChange]
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/device/changes",
            _kwargs=kwargs,
        )
        data = response.json()
        for el in data:
            el.update({"member_id": self.id})

        return [MemberDeviceChange(self._requester, change) for change in data]

    def get_device_change(self, change_id: int, **kwargs) -> MemberDeviceChange:
        """
        Retrieves a device change of a member given the change ID
        
        :calls: "GET /members/{id}/device/changes/{changeId}" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdDeviceChangesChangeId>
  
        :param change_id: ID of the change to retrieve
        :type change_id: int
        :returns: Device change information
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/device/changes/{change_id}",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberDeviceChange(self._requester, data)

    def get_export(self, **kwargs) -> requests.Response:
        """
        Retrieves the export of a member. This is a placeholder for future functionality.
        
        :calls: "GET /members/{id}/export" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdExport>
  
        :raises: NotImplementedError
        """
        raise NotImplementedError("get_export not implemented yet")

    def get_invitation(self, **kwargs) -> MemberInvitation:
        """
        Retrieves the invitation status of a member
        
        :calls: "GET /members/{id}/invitations" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdInvitation>
  
        :returns: Invitation status of a member
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/invitation",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberInvitation(self._requester, data)

    def get_key(self, **kwargs) -> MemberKey:
        """
        Retrieves the keycard number of a member
        
        :calls: "GET /members/{id}/key" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdKey>
  
        :returns: :code:`fabman.member.MemberKey` object with key details
        :rtype: fabman.member.MemberKey
        """
        if "key" in self._embedded:
            data = self._embedded["key"]
        else:
            response = self._requester.request(
                "GET",
                f"/members/{self.id}/key",
                _kwargs=kwargs,
            )
            data = response.json()
        data.update({"member_id": self.id})

        return MemberKey(self._requester, data)

    def get_packages(self, **kwargs) -> Union[EmbeddedList, PaginatedList]:
        """
        Retrieves the packages of a member

        :calls: "GET /members/{id}/packages" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdPackages>
  
        :returns: List of packages of a member
        :rtype: fabman.paginated_list.PaginatedList
        """
        if "memberPackages" in self._embedded:
            return EmbeddedList(
                MemberPackage,
                self._embedded["memberPackages"],
                self._requester,
                "GET",
                f"/members/{self.id}/packages",
                extra_attribs={"member_id": self.id},
            )

        return PaginatedList(
            MemberPackage,
            self._requester,
            "GET",
            f"/members/{self.id}/packages",
            extra_attribs={"member_id": self.id},
            **kwargs,
        )

    def get_package(self, member_package_id: int, **kwargs) -> MemberPackage:
        """
        Retrieves a package of a member
        
        :calls: "GET /members/{id}/packages/{memberPackageId}" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdPackagesMemberpackageid>
  
        :param member_package_id: ID of the package to retrieve
        :type member_package_id: int
        :returns: :code:`fabman.member.MemberPackage` object with package details
        :rtype: fabman.member.MemberPackage
        """
        data = dict()
        if "memberPackages" in self._embedded:
            for package in self._embedded["memberPackages"]:
                if package["id"] == member_package_id:
                    data = package
        if len(data) == 0:
            response = self._requester.request(
                "GET",
                f"/members/{self.id}/packages/{member_package_id}",
                _kwargs=kwargs,
            )

            data = response.json()
        data.update({"member_id": self.id})

        return MemberPackage(self._requester, data)

    def get_payment_account(self, **kwargs) -> MemberPaymentAccount:
        """
        Retrieves the payment account of a member
        
        :calls: "GET /members/{id}/payment-account" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentaccount>
  
        :returns: Payment account information
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/payment-account",
            _kwargs=kwargs,
        )

        data = {"payments": response.json()}
        data.update({"member_id": self.id})

        return MemberPaymentAccount(self._requester, data)

    def get_payment_method(self, **kwargs) -> MemberPaymentMethod:
        """
        Retrieves the payment method of a member
        :calls: "GET /members/{id}/payment-method" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentmethod>
  
        :returns: Payment method information
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/payment-method",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberPaymentMethod(self._requester, data)

    def get_payment_method_mandate_preview(
        self, **kwargs
    ) -> MemberPaymentMethodMandatePreview:
        """
        Retrieves the payment method mandate preview of a member
        
        :calls: "GET /members/{id}/payment-method-mandate-preview" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentmethodmandatepreview>
  
        :returns: Payment method mandate preview information
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/payment-method-mandate-preview",
            _kwargs=kwargs,
        )

        data = response.json()
        data.update({"member_id": self.id})

        return MemberPaymentMethodMandatePreview(self._requester, data)

    def get_privileges(self, **kwargs) -> MemberPrivileges:
        """
        Retrieves the privileges of a member
        :calls: "GET /members/{id}/privileges" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdPrivileges>
  
        :returns: privileges of a member
        :rtype: dict
        """
        if "privileges" in self._embedded:
            data = self._embedded["privileges"]
        else:
            response = self._requester.request(
                "GET",
                f"/members/{self.id}/privileges",
                _kwargs=kwargs,
            )

            data = response.json()
        data.update({"member_id": self.id})

        return MemberPrivileges(self._requester, data)

    def get_trained_resources(self, **kwargs) -> MemberTrainedResources:
        """
        Retrieves the trained resources of a member
        :calls: "GET /members/{id}/trained-resources" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdTrainedResources>
  
        :return: Trained resources of a member
        :rtype: list
        """
        response = self._requester.request(
            "GET",
            f"/members/{self.id}/trained-resources",
            _kwargs=kwargs,
        )

        data = {"resources": response.json()}
        data.update({"member_id": self.id})

        return MemberTrainedResources(self._requester, data)

    def get_trainings(
        self, ignore_embeds: Optional[bool] = False, **kwargs
    ) -> Union[PaginatedList, EmbeddedList]:
        """
        
        Retrieves the trainings of a member
        :calls: "GET /members/{id}/trainings" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdTrainings>

        :return: List of trainings of a member
        :rtype: Union[PaginatedList, EmbeddedList]
        """
        if "trainings" in self._embedded and not ignore_embeds:
            return EmbeddedList(
                MemberTraining,
                self._embedded["trainings"],
                self._requester,
                "GET",
                f"/members/{self.id}/trainings",
                extra_attribs={"member_id": self.id},
            )

        return PaginatedList(
            MemberTraining,
            self._requester,
            "GET",
            f"/members/{self.id}/trainings",
            extra_attribs={"member_id": self.id},
        )

    def get_training(self, training_id: int, **kwargs) -> MemberTraining:
        """
        Retrieves a training of a member
        :calls: "GET /members/{id}/trainings/{trainingId}" \
		<https://fabman.io/api/v1/documentation#/members/getMembersIdTrainingstrainingid>
        
        :param training_id: ID of the training to retrieve
        :type training_id: int
        :return: Training information
        :rtype: dict
        """
        data = {}
        if "trainings" in self._embedded:
            for training in self._embedded["trainings"]:
                if training["id"] == training_id:
                    data = training
        if len(data) == 0:
            response = self._requester.request(
                "GET",
                f"/members/{self.id}/trainings/{training_id}",
                _kwargs=kwargs,
            )

            data = response.json()
        data.update({"member_id": self.id})

        return MemberTraining(self._requester, data)

    def refresh(self) -> None:
        """
        Updates the objects with more recent data from the API. Needs to be called
        when update() fails for lockVersioning.

        :calls: "GET /members/{id}" \
		<https://fabman.io/api/v1/documentation#/members/getMembersId>
  
        :returns: None -- updates attributes of the current object
        :rtype: None
        """

        response = self._requester.request("GET", f"/members/{self.id}")

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)

    def update(self, **kwargs) -> None:
        """
        Updates the member object and sets the modified attributes based on what
        is returned by the server.  Member object is updated in place.

        :calls: "PUT /members/{id}" \
		<https://fabman.io/api/v1/documentation#/members/putMembersId>
  
        :returns: None -- updates attributes of the current object
        :rtype: None
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
