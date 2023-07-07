"""Defines the Account object"""

from fabman.fabman_object import FabmanObject


class PaymentInfo(FabmanObject):
    """Holds PaymentInfo as returned from the accounts endpoint."""

    def __str__(self):
        return f"PaymentInfo for Account #{self.account_id}: {self.paymentMethod}"


class Account(FabmanObject):
    """Handles Account objects from the Fabman API. In most cases, this only
    returns information about the API key holders account. Since most API endpoints
    in this object require superuser privileges, they are not implemented.
    """

    def __str__(self):
        return f"Account #{self.id}: {self.name}"

    def update(self, **kwargs) -> None:
        """
        Update information on the account. Note that many fields may be unalterable
        by the API key holder.

        :calls: "PUT /accounts/{id}" \
		<https://fabman.io/api/v1/documentation#/account/putAccountsId>

        :returns: None
        :rtype: None
        """
        uri = f"/accounts/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)

    def get_payment_info(self, **kwargs) -> PaymentInfo:
        """
        Get information about the payment plan of the account.

        :calls: "GET /accounts/{id}/payment-info" \
        <https://fabman.io/api/v1/documentation#/accounts/getAccountsIdPaymentinfo>
        
        :returns: Information about the payment plan of the account.
        :rtype: fabman.account.PaymentInfo
        """
        uri = f"/accounts/{self.id}/payment-info"

        response = self._requester.request("GET", uri, _kwargs=kwargs)
        data = response.json()
        data.update({"account_id": self.id})

        return PaymentInfo(self._requester, data)
