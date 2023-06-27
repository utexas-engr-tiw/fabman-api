"""Defines the Booking object"""

import requests

from fabman.fabman_object import FabmanObject


class Booking(FabmanObject):
    """
    Booking object as described in the Fabman API:
    https://fabman.io/api/v1/documentation#/bookings
    """

    def __str__(self):
        return f"Booking #{self.id}: {self.fromDateTime} - {self.toDateTime}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes the booking. *WARNING: THIS CANNOT BE UNDONE.*

        Calls "DELETE /bookings/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/bookings/deleteBookingsId
        """

        uri = f"/bookings/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Update the booking object on the server. Returns the updated booking object.
        Updates all information in place.

        Calls "PUT /bookings/{id}"
        Documentation: https://fabman.io/api/v1/documentation#/bookings/putBookingsId
        """

        uri = f"/bookings/{self.id}"

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
