"""Defines the Webhook class"""

import requests

from fabman.fabman_object import FabmanObject


class Webhook(FabmanObject):
    """
    Class for interacting with the webhooks endpoint on the Fabman API
    """

    def __str__(self):
        return f"Webhook #{self.id}: {self.label} ({self.url})"

    def delete(self, **kwargs):
        """
        Deletes a webhook. *WARNING: This is irreversible.*

        Calls "DELETE /webhooks/{webhookId}"
        Documentation https://fabman.io/api/v1/documentation#/webhooks/deleteWebhooksId
        """

        uri = f"/webhooks/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response.json()

    def get_events(self, **kwargs) -> requests.Response:
        """
        Returns the events for a webhook.

        Calls "GET /webhooks/{webhookId}/events"
        Documentation https://fabman.io/api/v1/documentation#/webhooks/getWebhooksIdEvents
        """

        if "events" in self._embedded:
            return self._embedded["events"]

        uri = f"/webhooks/{self.id}/events"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        return response.json()

    def send_test_event(self, **kwargs) -> requests.Response:
        """
        Sends a test event to the webhook.

        Calls "POST /webhooks/{webhookId}/events"
        Documentation https://fabman.io/api/v1/documentation#/webhooks/postWebhooksIdTest
        """

        uri = f"/webhooks/{self.id}/test"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        return response.json()

    def update(self, **kwargs) -> None:
        """
        Updates the webhook. Attributes are updated in place with new information

        Calls "PUT /webhooks/{webhookId}"
        Documentation https://fabman.io/api/v1/documentation#/webhooks/putWebhooksId
        """

        uri = f"/webhooks/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data:
            setattr(self, attr, val)
