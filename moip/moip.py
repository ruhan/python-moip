import requests
import base64
from models import ProtectedSaleOrder, ListOrdersFilters
# NOTE: Uncomment to make log active
#import log_all_requests


class Moip():
    url_sandbox = 'https://sandbox.moip.com.br/v2/'
    url_production = 'https://api.moip.com.br/v2/'

    def __init__(self, token, key):
        self.token = token
        self.key = key
        self.sandbox()

    @property
    def _auth(self):
        authcode = base64.b64encode('%s:%s' % (self.token, self.key))
        return {'headers': {'Authorization': 'Basic %s' % authcode}}

    @property
    def _url(self):
        if self._production:
            return self.url_production
        else:
            return self.url_sandbox

    def production(self):
        self._production = True

    def sandbox(self):
        self._production = False

    # cliente
    def list_customers(self):
        response = requests.get('%scustomers' % self._url, **self._auth)
        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            return response.json()

    # pedido
    def get_order(self, id):
        response = requests.get('%sorders/%s' % (self._url, id),
                                **self._auth)
        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            return response.json()

    def list_orders(self, filters=None):
        if filters:
            assert isinstance(filters, ListOrdersFilters)
            params = filters.to_json()
        else:
            params = {}

        response = requests.get('%sorders' % self._url, params=params,
                                **self._auth)
        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            return response.json()

    def create_protected_sale_order(self, protected_sale_order):
        assert isinstance(protected_sale_order, ProtectedSaleOrder)

        response = requests.post(
            '%sorders' % self._url, json=protected_sale_order.to_json(),
            **self._auth
        )

        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            return response.json()

    def create_webhook(self, events, target_url):
        """
            events: a list of events in the following way:
                [
                    "ORDER.*",
                    "PAYMENT.AUTHORIZED",
                ]

            target_url: url where the webhook will act on.
        """
        assert isinstance(events, list)

        response = requests.post(
            '%spreferences/notifications' % self._url, json={
                'events': events,
                'target': target_url,
                'media': "WEBHOOK"
            },
            **self._auth
        )

        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            return response.json()

    def resend_webhook(self, resource_id, event):
        """
        Send a webhook again (good for testing).
            resource_id: id of the resource on moip
            event: "ORDER.*"
        """
        assert isinstance(resource_id, str)
        assert isinstance(event, str)

        response = requests.post(
            '%swebhooks/' % self._url, json={
                'resourceId': resource_id,
                'event': event,
            },
            **self._auth
        )

        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            return response.json()

    def delete_webhook(self, notification_id):
        """
        Delete a webhook.
            resource_id: id of the webhook on moip
        """
        assert isinstance(notification_id, str)

        response = requests.delete(
            '%spreferences/notifications/%s' % (self._url, notification_id),
            **self._auth
        )

        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        elif response.status_code == 204:
            return True
        else:
            return response.json()

    def list_webhooks(self):
        """
        List all registered webhooks
        """
        response = requests.get(
            '%spreferences/notifications' % self._url,
            **self._auth
        )

        if response.status_code == 401:
            raise MoipAuthorizationException(response.json())
        else:
            pretty_print(response.json())
            return response.json()


class MoipAuthorizationException(Exception):
    pass


def pretty_print(data):
    import pprint
    print pprint.pformat(data)
