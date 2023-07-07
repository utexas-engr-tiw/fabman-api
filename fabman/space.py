"""Defines the Space class and other Space-related classes"""

from typing import Union

import requests

from fabman.fabman_object import FabmanObject
from fabman.paginated_list import PaginatedList


class SpaceBillingSettings(FabmanObject):
    """Class for interacting with the space-billing-settings endpoint on the Fabman API"""

    def __str__(self):
        return f"SpaceBillingSettings for space #{self.space}"

    def delete_stripe(self, **kwargs) -> requests.Response:
        """
        Deletes Stripe information from a space. *WARNING: This is irreversible.*

        :calls: "DELETE /space/{id]/billing-settings/stripe" \
		<https://fabman.io/api/v1/documentation#/spaces/deleteSpacesIdBillingsettingsStripe>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/spaces/{self.space_id}/billing-settings/stripe"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the space-billing-settings. Attributes are updated in place with new information
        retrieved from the API.

        :calls: "PUT /space-billing-settings/{spaceBillingSettingsId}" \
		<https://fabman.io/api/v1/documentation#/space-billing-settings/putSpaceBillingSettingsSpaceBillingSettingsId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/spaces/{self.space_id}/billing-settings"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)

    def update_stripe(self, **kwargs) -> None:
        """
        Updates the space-billing-settings. Attributes are updated in place with new information
        retrieved from the API. Placeholder for future implementation

        :calls: "PUT /space-billing-settings/{spaceBillingSettingsId}" \
		<https://fabman.io/api/v1/documentation>
  
        :raises: NotImplementedError
        """

        raise NotImplementedError("This method is not yet implemented.")


class SpaceHoliday(FabmanObject):
    """Class for interacting with the space/{id}/holidays endpoints on the Fabman API"""

    def __str__(self):
        return f"SpaceHoliday #{self.id}: {self.title}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a space holiday. *WARNING: This is irreversible.*

        :calls: "DELETE /space/{spaceId}/holidays/{holidayId}" \
		<https://fabman.io/api/v1/documentation#/spaces/deleteSpacesIdHolidaysHolidayid>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/spaces/{self.space_id}/holidays/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the space holiday. Attributes are updated in place with new information
        retrieved from the API.

        :calls: "PUT /space/{spaceId}/holidays/{holidayId}" \
		<https://fabman.io/api/v1/documentation#/spaces/putSpacesIdHolidaysHolidayid>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/spaces/{self.space_id}/holidays/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class SpaceOpeningHours(FabmanObject):
    """Class for holding Opening Hours requests"""

    def __str__(self):
        out = f"Space #{self.space_id} Opening Hours:\n"
        out += "+-----------------+-----------------+\n"
        for day in self.days:
            out += f"{day['dayOfWeek']}: {day['fromTime']} - {day['untilTime']}\n"

        return out


class Space(FabmanObject):
    """Class for interacting with the Space endpoint on the Fabman API"""

    def __str__(self):
        return f"Space #{self.id}: {self.name}"

    def create_holiday(self, **kwargs) -> SpaceHoliday:
        """
        Creates a new holiday for the space.

        :calls: "POST /spaces/{spaceId}/holidays" \
		<https://fabman.io/api/v1/documentation#/spaces/postSpacesIdHolidays>
  
        :return: Object with new holiday information
        :rtype: fabman.space.SpaceHoliday
        """

        uri = f"/spaces/{self.id}/holidays"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        return SpaceHoliday(self._requester, response.json())

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a space. *WARNING: This is irreversible.*

        :calls: "DELETE /spaces/{spaceId}" \
		<https://fabman.io/api/v1/documentation#/spaces/deleteSpacesId>

        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/spaces/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def delete_calendar_token(self, **kwargs) -> requests.Response:
        """
        Deletes a space calendar token. *WARNING: This is irreversible.*

        :calls: "DELETE /spaces/{spaceId}/calendar-token" \
		<https://fabman.io/api/v1/documentation#/spaces/deleteSpacesIdCalendartoken>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/spaces/{self.id}/calendar-token"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def get_billing_settings(self, **kwargs) -> SpaceBillingSettings:
        """
        Returns the billing settings for the space.

        :calls: "GET /spaces/{spaceId}/billing-settings" \
		<https://fabman.io/api/v1/documentation#/spaces/getSpacesIdBillingsettings>
  
        :return: Object with billing settings information
        :rtype: fabman.space.SpaceBillingSettings
        """
        if "billingSettings" in self._embedded:
            settings = self._embedded["billingSettings"]
            settings.update({"space_id": self.id})
            return SpaceBillingSettings(self._requester, settings)

        uri = f"/spaces/{self.id}/billing-settings"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"space_id": self.id})

        return SpaceBillingSettings(self._requester, data)

    def get_holiday(self, holiday_id, **kwargs) -> SpaceHoliday:
        """
        Returns a specific holiday for the space given a holiday_id.

        :calls: "GET /spaces/{spaceId}/holidays/{holidayId}" \
		<https://fabman.io/api/v1/documentation#/spaces/getSpacesIdHolidaysHolidayid>
        
        :param holiday_id: ID of the holiday to retrieve
        :type holiday_id: int
        :return: Object with holiday information
        :rtype: fabman.space.SpaceHoliday
        """

        uri = f"/spaces/{self.id}/holidays/{holiday_id}"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        data = response.json()
        data.update({"space_id": self.id})

        return SpaceHoliday(self._requester, data)

    def get_holidays(self, **kwargs) -> Union[list, PaginatedList]:
        """
        Returns a list of holidays for the space. If the information is cached from an embedded call, 
        a list of SpaceHoliday objects is returned. Otherwise, a PaginatedList will be returned.

        :calls: "GET /spaces/{spaceId}/holidays" \
		<https://fabman.io/api/v1/documentation#/spaces/getSpacesIdHolidays>
  
        :return: List of SpaceHoliday Objects
        :rtype: list[fabman.space.SpaceHoliday] or fabman.paginated_list.PaginatedList
        """
        if "holidays" in self._embedded:
            out = []
            for holiday in self._embedded["holidays"]:
                holiday.update({"space_id": self.id})
                out.append(SpaceHoliday(self._requester, holiday))
            return out

        return PaginatedList(
            SpaceHoliday,
            self._requester,
            "GET",
            f"/spaces/{self.id}/holidays",
            extra_attribs={"space_id": self.id},
            kwargs=kwargs,
        )

    def get_opening_hours(self, **kwargs) -> Union[list, requests.Response]:
        """
        Get the opening hours for the space.

        :calls: "GET /spaces/{spaceId}/opening-hours" \
		<https://fabman.io/api/v1/documentation#/spaces/getSpacesIdOpeninghours>

        :return: List of opening hours
        :rtype: list
        """

        if "openingHours" in self._embedded:
            return self._embedded["openingHours"]

        uri = f"/spaces/{self.id}/opening-hours"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the space. Attributes are updated in place with new information
        from the API.

        :calls: "PUT /spaces/{spaceId}" \
		<https://fabman.io/api/v1/documentation#/spaces/putSpacesId>

        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/spaces/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)

    def update_calendar_token(self, **kwargs) -> requests.Response:
        """
        Updates the space calendar token and returns a link to the new calendar ics
        file. Calendar Token attribute is updated in place with new information.

        :calls: "PUT /spaces/{spaceId}/calendar-token" \
		<https://fabman.io/api/v1/documentation#/spaces/putSpacesIdCalendartoken>

        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/spaces/{self.id}/calendar-token"

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        token = data["calendarUrl"].split("/")[-1].split(".")[0]
        setattr(self, "calendarToken", token)
        setattr(self, "calendarUrl", data["calendarUrl"])

        return response

    def update_opening_hours(self, **kwargs) -> SpaceOpeningHours:
        """
        Updates the opening hours of a space. If the the openingHours key is
        present in the _embedded attribute, the opening hours are updated in
        place with information returned by the api.

        :calls: "PUT /spaces/{spaceId}/opening-hours" \
		<https://fabman.io/api/v1/documentation#/spaces/putSpacesIdOpeninghours>
  
        :return: response information of call
        :rtype: SpaceOpeningHours
        """

        uri = f"/spaces/{self.id}/opening-hours"

        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        if "openingHours" in self._embedded:
            self._embedded["openingHours"] = self.get_opening_hours()

        data = response.json()
        out = {"days": data}
        out.update({"space_id": self.id})

        return SpaceOpeningHours(self._requester, out)
