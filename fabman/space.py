"""Defines the Space class and other Space-related classes"""

import requests
from typing import Union

from fabman.fabman_object import FabmanObject
from fabman.paginated_list import PaginatedList


class SpaceBillingSettings(FabmanObject):
    """Class for interacting with the space-billing-settings endpoint on the Fabman API"""

    def __str__(self):
        return f"SpaceBillingSettings #{self.id}: {self.space}"

    def delete_stripe(self, **kwargs) -> requests.Response:
        """
        Deletes Stripe information from a space. *WARNING: This is irreversible.*

        Calls "DELETE /space/{id]/billing-settings/stripe"
        #/spaces/deleteSpacesIdBillingsettingsStripe
        Documentation https://fabman.io/api/v1/documentation
        """

        uri = f'/space/{self.space_id}/billing-settings/stripe'

        response = self._requester.request('DELETE', uri, _kwargs=kwargs)

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates the space-billing-settings. Attributes are updated in place with new information
        retrieved from the API.

        Calls "PUT /space-billing-settings/{spaceBillingSettingsId}"
        #/space-billing-settings/putSpaceBillingSettingsSpaceBillingSettingsId
        Documentation https://fabman.io/api/v1/documentation
        """

        uri = f'/space-billing-settings/{self.id}'

        kwargs.update({'lockVersion': self.lockVersion})

        response = self._requester.request('PUT', uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)

    def update_stripe(self, **kwargs) -> None:
        """
        Updates the space-billing-settings. Attributes are updated in place with new information
        retrieved from the API.

        Calls "PUT /space-billing-settings/{spaceBillingSettingsId}"
        Documentation https://fabman.io/api/v1/documentation
        """

        raise NotImplementedError("This method is not yet implemented.")


class SpaceHoliday(FabmanObject):
    """Class for interacting with the space/{id}/holidays endpoints on the Fabman API"""

    def __str__(self):
        return f"SpaceHoliday #{self.id}: {self.space}"

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a space holiday. *WARNING: This is irreversible.*

        Calls "DELETE /space/{spaceId}/holidays/{holidayId}"
        #/spaces/deleteSpacesIdHolidaysHolidayid
        Documentation https://fabman.io/api/v1/documentation
        """

        uri = f'/space/{self.space_id}/holidays/{self.id}'

        response = self._requester.request('DELETE', uri, _kwargs=kwargs)

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates the space holiday. Attributes are updated in place with new information
        retrieved from the API.

        Calls "PUT /space/{spaceId}/holidays/{holidayId}"
        #/spaces/putSpacesIdHolidaysHolidayid
        Documentation https://fabman.io/api/v1/documentation
        """

        uri = f'/space/{self.space_id}/holidays/{self.id}'

        kwargs.update({'lockVersion': self.lockVersion})

        response = self._requester.request('PUT', uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)


class Space(FabmanObject):
    """Class for interacting with the Space endpoint on the Fabman API"""

    def __str__(self):
        return f"Space #{self.id}: {self.name}"

    def create_holiday(self, **kwargs) -> SpaceHoliday:
        """
        Creates a new holiday for the space.

        Calls "POST /spaces/{spaceId}/holidays"
        Documentation https://fabman.io/api/v1/documentation#/spaces/postSpacesIdHolidays
        """

        uri = f'/spaces/{self.id}/holidays'

        response = self._requester.request('POST', uri, _kwargs=kwargs)

        return SpaceHoliday(self._requester, response.json())

    def delete(self, **kwargs) -> requests.Response:
        """
        Deletes a space. *WARNING: This is irreversible.*

        Calls "DELETE /spaces/{spaceId}"
        Documentation https://fabman.io/api/v1/documentation#/spaces/deleteSpacesId
        """

        uri = f'/spaces/{self.id}'

        response = self._requester.request('DELETE', uri, _kwargs=kwargs)

        return response.json()

    def delete_calendar_token(self, **kwargs) -> requests.Response:
        """
        Deletes a space calendar token. *WARNING: This is irreversible.*

        Calls "DELETE /spaces/{spaceId}/calendar-token"
        Documentation https://fabman.io/api/v1/documentation#/spaces/deleteSpacesIdCalendartoken
        """

        uri = f'/spaces/{self.id}/calendar-token'

        response = self._requester.request('DELETE', uri, _kwargs=kwargs)

        return response.json()

    def get_billing_settings(self, **kwargs) -> SpaceBillingSettings:
        """
        Returns the billing settings for the space.

        Calls "GET /spaces/{spaceId}/billing-settings"
        Documentation https://fabman.io/api/v1/documentation#/spaces/getSpacesIdBillingsettings
        """
        if 'billingSettings' in self._embedded:
            settings = self._embedded['billingSettings']
            settings.update({'space_id': self.id})
            return SpaceBillingSettings(self._requester, settings)

        uri = f'/spaces/{self.id}/billing-settings'

        response = self._requester.request('GET', uri, _kwargs=kwargs)

        data = response.json()
        data.update({'space_id': self.id})

        return SpaceBillingSettings(self._requester, data)

    def get_holiday(self, holiday_id, **kwargs) -> SpaceHoliday:
        """
        Returns a specific holiday for the space given a holiday_id.

        Calls "GET /spaces/{spaceId}/holidays/{holidayId}"
        Documentation https://fabman.io/api/v1/documentation#/spaces/getSpacesIdHolidaysHolidayid
        """

        uri = f'/spaces/{self.id}/holidays/{holiday_id}'

        response = self._requester.request('GET', uri, _kwargs=kwargs)

        data = response.json()
        data.update({'space_id': self.id})

        return SpaceHoliday(self._requester, data)

    def get_holidays(self, **kwargs) -> Union[list, PaginatedList]:
        """
        Returns a list of holidays for the space.

        Calls "GET /spaces/{spaceId}/holidays"
        Documentation https://fabman.io/api/v1/documentation#/spaces/getSpacesIdHolidays
        """
        if 'holidays' in self._embedded:
            out = []
            for holiday in self._embedded['holiday']:
                setattr(holiday, 'space_id', self.id)
                out.append(SpaceHoliday(self._requester, holiday))

        return PaginatedList(
            SpaceHoliday,
            self._requester,
            "GET",
            f'/spaces/{self.id}/holidays',
            extra_attribs={'space_id': self.id},
            kwargs=kwargs
        )

    def get_opening_hours(self, **kwargs) -> requests.Response:
        """
        Get the opening hours for the space.

        Calls "GET /spaces/{spaceId}/opening-hours"
        Documentation https://fabman.io/api/v1/documentation#/spaces/getSpacesIdOpeninghours
        """

        if 'openingHours' in self._embedded:
            return self._embedded['openingHours']

        uri = f'/spaces/{self.id}/opening-hours'

        response = self._requester.request('GET', uri, _kwargs=kwargs)

        return response.json()

    def update_calendar_token(self, **kwargs) -> requests.Response:
        """
        Updates the space calendar token and returns a link to the new calendar ics
        file. Calendar Token attribute is updated in place with new information.

        Calls "PUT /spaces/{spaceId}/calendar-token"
        Documentation https://fabman.io/api/v1/documentation#/spaces/putSpacesIdCalendartoken
        """

        uri = f'/spaces/{self.id}/calendar-token'

        kwargs.update({'lockVersion': self.lockVersion})

        response = self._requester.request('PUT', uri, _kwargs=kwargs)

        data = response.json()

        token = data['calendarUrl'].split('/')[-1].split('.')[0]
        setattr(self, 'calendarToken', token)
        setattr(self, 'calendarUrl', data['calendarUrl'])

        return response.json()

    def update_opening_hours(self, **kwargs) -> requests.Response:
        """
        Updates the opening hours of a space. If the the openingHours key is 
        present in the _embedded attribute, the opening hours are updated in
        place with information returned by the api.

        calls "PUT /spaces/{spaceId}/opening-hours"
        Documentation https://fabman.io/api/v1/documentation#/spaces/putSpacesIdOpeninghours
        """

        uri = f'/spaces/{self.id}/opening-hours'

        response = self._requester.request('PUT', uri, _kwargs=kwargs)

        if 'openingHours' in self._embedded:
            self._embedded['openingHours'] = self.get_opening_hours()

        return response.json()
