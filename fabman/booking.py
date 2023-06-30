"""Defines the Booking object"""

import requests

from fabman.fabman_object import FabmanObject


class Booking(FabmanObject):
    """
    Booking object as described in the Fabman API:
    https://fabman.io/api/v1/documentation#/bookings
    """

    def __str__(self):
        return f"Booking #{self.id}: {self.fromDateTime} - {self.untilDateTime}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes the booking. *WARNING: THIS CANNOT BE UNDONE.*

        :calls: "DELETE /bookings/{id}" \
		<https://fabman.io/api/v1/documentation#/bookings/deleteBookingsId>
  
        :returns: Response from the API with status code 204 (No Content) if successful
        :rtype: requests.Response
        """

        uri = f"/bookings/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Update the booking object on the server. Returns the updated booking object.
        Updates all information in place.

        :calls: "PUT /bookings/{id}" \
		<https://fabman.io/api/v1/documentation#/bookings/putBookingsId>

        :returns: None
        :rtype: None
        """

        uri = f"/bookings/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
