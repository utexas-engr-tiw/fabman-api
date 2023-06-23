"""Defines and handles the Member object returned by the API"""
# pylint: disable=too-many-public-methods, line-too-long
import requests
from fabman.fabman_object import FabmanObject
from fabman.util import combine_kwargs


class Member(FabmanObject):
    """ 
    Member object returned by the API. Provides access to all API calls that operate on a single member.
    """

    def __str__(self):
        return f"{self.id}: {self.firstName} {self.lastName}"

    def create_credit(self, **kwargs) -> requests.Response:
        """
        Creates a member credit
        calls "POST /members/{id}/credits"
        Documentation: https://fabman.io/api/v1/documentation#/members/postMembersIdCredits
        """
        return self.__requester.request(
            "POST", f"/members/{self.id}/credits",
            _kwargs=combine_kwargs(**kwargs),
            json=True
        )

    def delete_member(self, **kwargs) -> requests.Response:
        """
        Deletes a member
        calls "DELETE /members/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersId
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_change(self, change_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member change given change ID
        calls "DELETE /members/{id}/changes/{changeId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdChangesChangeId
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/changes/{change_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_credit(self, credit_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member credit given credit ID
        calls "DELETE /members/{id}/credits/{creditId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdCreditsCreditId
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/credits/{credit_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_device_change(self, change_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member device change given change ID
        Calls "DELETE /members/{id}/device/changes/{changeId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdDeviceChangesChangeId
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/device/changes/{change_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_key(self, **kwargs) -> requests.Response:
        """
        Deletes a member key
        calls "DELETE /members/{id}/key"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdKey
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/key",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_package(self, member_package_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member package given package ID
        Calls "DELETE /members/{id}/packages/{memberPackageId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdPackagesMemberPackageId
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/packages/{member_package_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_payment_method(self, **kwargs) -> requests.Response:
        """
        Deletes a member payment method
        Calls "DELETE /members/{id}/payment-method"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdPaymentMethod
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/payment-method",
            _kwargs=combine_kwargs(**kwargs),
        )

    def delete_training(self, training_id: int, **kwargs) -> requests.Response:
        """
        Deletes a member training given training ID
        Calls "DELETE /members/{id}/trainings/{trainingId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/deleteMembersIdTrainingsTrainingId
        """
        return self.__requester.request(
            "DELETE", f"/members/{self.id}/trainings/{training_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_balance_items(self, **kwargs) -> requests.Response:
        """
        Retrieves the balance items of a member
        calls "GET /members/{id}/balance-items"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdBalanceitems
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/balance-items",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_changes(self, **kwargs) -> requests.Response:
        """
        Retrieves the changes of a member
        calls "GET /members/{id}/changes"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdChanges
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/changes",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_credits(self, **kwargs) -> requests.Response:
        """
        Retrieves the credits of a member
        calls "GET /members/{id}/credits"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdCredits
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/credits",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_credit_by_id(self, credit_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a credit of a member
        calls "GET /members/{id}/credits/{creditId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdCreditsCreditId
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/credits/{credit_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_credit_uses_by_id(self, credit_id: int, **kwargs) -> requests.Response:
        """
        Retrieves the credit uses of a member
        calls "GET /members/{id}/credits/{creditId}/uses"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdCreditsCreditIdUses
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/credits/{credit_id}/uses",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_device(self, **kwargs) -> requests.Response:
        """
        Retrieves the devices of a member
        calls "GET /members/{id}/devices"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdDevice
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/device",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_device_changes(self, **kwargs) -> requests.Response:
        """
        Retrieves the device changes of a member
        calls "GET /members/{id}/device-changes"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdDeviceChanges
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/device/changes",
            _kwargs=combine_kwargs(**kwargs),
        )

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
        return self.__requester.request(
            "GET", f"/members/{self.id}/invitation",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_key(self, **kwargs):
        """
        Retrieves the key of a member
        calls "GET /members/{id}/key"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdKey
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/key",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_packages(self, **kwargs):
        """
        Retrieves the packages of a member
        calls "GET /members/{id}/packages"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPackages
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/packages",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_package(self, member_package_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a package of a member
        calls "GET /members/{id}/packages/{memberPackageId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPackagesMemberPackageId
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/packages/{member_package_id}",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_payment_account(self, **kwargs) -> requests.Response:
        """
        Retrieves the payment account of a member
        calls "GET /members/{id}/payment-account"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentAccount
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/payment-account",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_payment_method(self, **kwargs) -> requests.Response:
        """
        Retrieves the payment method of a member
        calls "GET /members/{id}/payment-method"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentMethod
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/payment-method",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_payment_method_mandate_preview(self, **kwargs) -> requests.Response:
        """
        Retrieves the payment method mandate preview of a member
        calls "GET /members/{id}/payment-method-mandate-preview"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPaymentMethodMandatePreview
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/payment-method-mandate-preview",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_privileges(self, **kwargs) -> requests.Response:
        """
        Retrieves the privileges of a member
        calls "GET /members/{id}/privileges"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdPrivileges
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/privileges",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_trained_resources(self, **kwargs) -> requests.Response:
        """
        Retrieves the trained resources of a member
        calls "GET /members/{id}/trained-resources"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdTrainedResources
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/trained-resources",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_trainings(self, **kwargs) -> requests.Response:
        """
        Retrieves the trainings of a member
        calls "GET /members/{id}/trainings"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdTrainings
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/trainings",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_training(self, training_id: int, **kwargs) -> requests.Response:
        """
        Retrieves a training of a member
        calls "GET /members/{id}/trainings/{trainingId}"
        Documentation: https://fabman.io/api/v1/documentation#/members/getMembersIdTrainingsTrainingId
        """
        return self.__requester.request(
            "GET", f"/members/{self.id}/trainings/{training_id}",
            _kwargs=combine_kwargs(**kwargs),
        )
