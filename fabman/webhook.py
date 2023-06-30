"""Defines the Webhook class"""

import requests

from fabman.fabman_object import FabmanObject


class Webhook(FabmanObject):
    """
    Class for interacting with the webhooks endpoint on the Fabman API
    """

    def __str__(self):
        return f"Webhook #{self.id}: {self.label}"

    def delete(self, **kwargs):
        """
        Deletes a webhook. *WARNING: This is irreversible.*

        :calls: "DELETE /webhooks/{webhookId}" \
		<https://fabman.io/api/v1/documentation#/webhooks/deleteWebhooksId>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/webhooks/{self.id}"

        response = self._requester.request("DELETE", uri, _kwargs=kwargs)

        return response

    def get_events(self, **kwargs) -> requests.Response:
        """
        Returns the events for a webhook.

        :calls: "GET /webhooks/{webhookId}/events" \
		<https://fabman.io/api/v1/documentation#/webhooks/getWebhooksIdEvents>
  
        :return: response information of call
        :rtype: requests.Response
        """

        if "events" in self._embedded:
            return self._embedded["events"]

        uri = f"/webhooks/{self.id}/events"

        response = self._requester.request("GET", uri, _kwargs=kwargs)

        return response

    def send_test_event(self, **kwargs) -> requests.Response:
        """
        Sends a test event to the webhook.

        :calls: "POST /webhooks/{webhookId}/events" \
		<https://fabman.io/api/v1/documentation#/webhooks/postWebhooksIdTest>
  
        :return: response information of call
        :rtype: requests.Response
        """

        uri = f"/webhooks/{self.id}/test"

        response = self._requester.request("POST", uri, _kwargs=kwargs)

        return response

    def update(self, **kwargs) -> None:
        """
        Updates the webhook. Attributes are updated in place with new information

        :calls: "PUT /webhooks/{webhookId}" \
		<https://fabman.io/api/v1/documentation#/webhooks/putWebhooksId>
  
        :return: None -- attributes are updated in place
        :rtype: None
        """

        uri = f"/webhooks/{self.id}"

        kwargs.update({"lockVersion": self.lockVersion})
        response = self._requester.request("PUT", uri, _kwargs=kwargs)

        data = response.json()

        for attr, val in data.items():
            setattr(self, attr, val)
